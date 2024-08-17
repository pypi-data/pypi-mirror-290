from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Collection, Generator
import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.laser import Laser, create_laser

from .base import BaseDistributor, RhoIndices
from .time import TimeDistributor
from .utils import fast_pad
from ..buffer import DensityMatrixBuffer
from ...utils import Logger, get_array_filter, safe_fill_larger
from ...typing import Communicator


def create_perturbation(perturbation: Perturbation | dict):
    if isinstance(perturbation, Perturbation):
        return Perturbation

    assert isinstance(perturbation, dict)
    if perturbation['name'] == 'deltakick':
        return DeltaKick(strength=perturbation['strength'])
    pulse = create_laser(perturbation)
    return PulsePerturbation(pulse)


class Perturbation(ABC):

    """ Perturbation that density matrices are a response to """

    def timestep(self,
                 times: NDArray[np.float64]):
        dt = times[1] - times[0]
        assert np.allclose(times[1:] - dt, times[:-1]), 'Variable time step'
        return dt

    @abstractmethod
    def fourier(self,
                times: NDArray[np.float64],
                padnt: int) -> NDArray[np.complex64]:
        """
        Fourier transform of perturbation

        Parameters
        ----------
        times
            Time grid in atomic units
        padnt
            Length of zero-padded time grid
        """
        raise NotImplementedError


class DeltaKick(Perturbation):

    """ Delta-kick perturbation

    Parameters
    ----------
    strength
        Strength of the perturbation
    """

    def __init__(self,
                 strength: float):
        self.strength = strength

    def fourier(self,
                times: NDArray[np.float64],
                padnt: int) -> NDArray[np.complex64]:
        # The strength is specified in the frequency domain, hence no multiplication by timestep
        norm = self.strength
        return np.array([norm])


class PulsePerturbation(Perturbation):

    """ Perturbation as a time-dependent function

    Parameters
    ----------
    pulse
        Object representing the pulse
    """

    def __init__(self,
                 pulse: Laser | dict):
        self.pulse = create_laser(pulse)

    def fourier(self,
                times: NDArray[np.float64],
                padnt: int) -> NDArray[np.complex64]:
        pulse_t = self.pulse.strength(times)
        return np.fft.rfft(pulse_t, n=padnt) * self.timestep(times)


class PulseConvolver(BaseDistributor):
    """ Iteratively convolve density matrices with pulses

    By the convolution theorem, a convolution of two quantities in the time domain
    is equivalent to Fourier transform of the two quantities, multiplication in
    frequency space, and inverse Fourier transform of the product to time domain.

    This class performs the FFT -> multiplication -> IFFT.

    The arrays to be convoluted must be real.

    Parameters
    ----------
    rho_nn_reader
        Object that can iteratively read density matrices in the time domain,
        distributed such that different ranks have different chunks of the density
        matrix, but each ranks has all times for the
        same chunk.
    perturbation
        The perturbation which the density matrices are a response to
    pulses
        List of laser pulses. The laser pulse objects must return the (real!) laser
        amplitude when given an array of times
    derivative_order_s
        Orders of derivatives to compute
    filter_times
        After convolution keep only these times (or the times closest to them). In
        atomic units
    result_on_ranks
        List of ranks among which the resulting arrays will be distributed.
        Empty list (default) to distribute among all ranks.
    """

    def __init__(self,
                 rho_nn_reader: TimeDistributor,
                 perturbation: Perturbation | dict,
                 pulses: Collection[Laser],
                 derivative_order_s: list[int] = [0],
                 filter_times: list[float] | NDArray[np.float64] | None = None,
                 result_on_ranks: list[int] = []):
        self.rho_nn_reader = rho_nn_reader
        self._flt_t = get_array_filter(self.rho_nn_reader.time_t, filter_times)
        self.pulses = pulses
        self.perturbation = create_perturbation(perturbation)

        if len(result_on_ranks) == 0:
            self._result_on_ranks = set(range(self.comm.size))
        else:
            assert all(isinstance(rank, int) and rank >= 0 and rank < self.comm.size
                       for rank in result_on_ranks), result_on_ranks
            self._result_on_ranks = set(result_on_ranks)

        nnshape = (self.rho_nn_reader._parameters.n1size, self.rho_nn_reader._parameters.n2size)
        xshape = (len(self.pulses), self.nt)

        self._dist_buffer: DensityMatrixBuffer | None = None
        super().__init__(nnshape, xshape, float, 'convolution', derivative_order_s)

        times = self.rho_nn_reader.time_t
        dt = times[1] - times[0]
        assert np.allclose(times[1:] - dt, times[:-1]), 'Variable time step'

    @property
    def ksd(self) -> KohnShamDecomposition:
        """ Kohn-Sham decomposition object """
        return self.rho_nn_reader.ksd

    @property
    def comm(self) -> Communicator:
        return self.rho_nn_reader.comm

    @property
    def yield_re(self) -> bool:
        return self.rho_nn_reader.yield_re

    @property
    def yield_im(self) -> bool:
        return self.rho_nn_reader.yield_im

    @property
    def log(self) -> Logger:
        return self.rho_nn_reader.log

    @property
    def time_t(self) -> NDArray[np.float64]:
        return self.rho_nn_reader.time_t[self._flt_t]

    @property
    def nchunks(self) -> int:
        """ Count the number of chunks (number of source ranks doing work) """
        for chunks_r in self.work_loop_by_ranks():
            nchunks = len([chunk for chunk in chunks_r if chunk is not None])
            return nchunks

        raise RuntimeError

    @property
    def nt(self) -> int:
        return len(self.time_t)

    @property
    def nlocalt(self) -> int:
        return (self.nt + self.nranks_result - 1) // self.nranks_result

    @property
    def result_on_ranks(self) -> list[int]:
        """ Set of ranks among which the result will be distributed """
        return sorted(self._result_on_ranks)

    @property
    def nranks_result(self) -> int:
        """ Number of ranks that the resulting arrays will be distributed among """
        return len(self._result_on_ranks)

    @property
    def dt(self) -> float:
        time_t = self.time_t
        return time_t[1] - time_t[0]

    @property
    def _omega_w(self) -> NDArray[np.float64]:
        """ Frequency grid in atomic units """
        time_t = self.rho_nn_reader.time_t
        padnt = fast_pad(self.rho_nn_reader.nt)
        dt = self.rho_nn_reader.dt

        assert np.allclose(time_t[1:] - dt, time_t[:-1]), 'Variable time step'
        omega_w = 2 * np.pi * np.fft.rfftfreq(padnt, dt)
        return omega_w

    @property
    def pulse_pt(self) -> NDArray[np.float64]:
        pulse_pt = np.array([pulse.strength(self.rho_nn_reader.time_t) for pulse in self.pulses])
        assert pulse_pt.dtype == float
        return pulse_pt

    @property
    def pulse_pw(self) -> NDArray[np.complex64]:
        padnt = fast_pad(self.rho_nn_reader.nt)
        return np.fft.rfft(self.pulse_pt, axis=-1, n=padnt)

    def _freq_domain_derivative(self,
                                order: int) -> NDArray[np.complex64 | np.float64]:
        r""" Take derivative in frequency space by multiplying by .. math:

        (i \omega)^n

        Parameters
        ----------
        order
            Order :math:`n` of the derivative
        """
        if order == 0:
            return np.array([1])
        if order == 1:
            return 1.0j * self._omega_w
        if order == 2:
            return - self._omega_w ** 2
        raise ValueError(f'Order {order} not supported')

    @property
    def dist_buffer(self) -> DensityMatrixBuffer:
        """ Buffer of denisty matrices on this rank after redistribution """
        if self._dist_buffer is None:
            self._dist_buffer = self.redistribute()
        return self._dist_buffer

    def work_loop_by_ranks(self) -> Generator[list[RhoIndices | None], None, None]:
        """ Like work_loop but for all ranks
        """
        yield from self.rho_nn_reader.work_loop_by_ranks()

    def __iter__(self) -> Generator[DensityMatrixBuffer, None, None]:
        nt = len(self.rho_nn_reader.time_t)  # Pad with zeros
        padnt = fast_pad(nt)
        flt_t = self._flt_t

        dm_buffer = DensityMatrixBuffer(self.rho_nn_reader._parameters.nnshape,
                                        (len(self.pulses), self.nt),
                                        np.float64)
        dm_buffer.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        for read_buffer in self.rho_nn_reader:
            x = []
            if self.yield_re:
                x.append((read_buffer._re_buffers[0], dm_buffer._re_buffers))
            if self.yield_im:
                x.append((read_buffer._im_buffers[0], dm_buffer._im_buffers))
            for data_nnt, buffers in x:
                # Fourier transform real or imaginary data
                data_nnw = np.fft.rfft(data_nnt, axis=-1, n=padnt)

                # Loop over the desired outputs (and which derivative orders they are)
                for derivative, buffer_nnpt in buffers.items():
                    deriv_w = self._freq_domain_derivative(derivative)
                    for p, pulse_w in enumerate(self.pulse_pw):
                        # Multiply with correct scaling factors and pulse
                        # All dt's cancel when taking fft->ifft so remove the one from the perturbation
                        perturb_w = self.perturbation.fourier(self.rho_nn_reader.time_t, padnt)
                        perturb_w /= self.perturbation.timestep(self.rho_nn_reader.time_t)
                        _data_nnw = data_nnw * (deriv_w / perturb_w * pulse_w)[None, None, :]
                        # Inverse Fourier transform
                        conv_nnt = np.fft.irfft(_data_nnw, n=padnt, axis=-1)
                        buffer_nnpt[..., p, :] = conv_nnt[..., :nt][..., flt_t]

            yield dm_buffer.copy()

    def gather_on_root(self):
        self.rho_nn_reader.C0S_sknM   # Make sure to read this synchronously
        yield from super().gather_on_root()

    def print_description(self):
        if self.comm.rank != 0:
            return

        self.rho_nn_reader.print_description()

        parameters = self.rho_nn_reader._parameters

        # Maximum number of ranks participating in reading of chunks
        for chunks_r in self.work_loop_by_ranks():
            maxnchunks = sum(1 for chunk in chunks_r if chunk is not None)
            break

        narrays = (2 if self.yield_re and self.yield_im else 1) * len(self.derivative_order_s)
        temp_shape = parameters.nnshape + (maxnchunks, len(self.pulses), self.nlocalt)
        result_shape = parameters.full_nnshape + (len(self.pulses), self.nlocalt)
        total_temp_size = np.prod(parameters.nnshape +
                                  (maxnchunks, len(self.pulses), self.nlocalt * self.nranks_result),
                                  dtype=int) * narrays
        total_result_size = np.prod(parameters.full_nnshape +
                                    (len(self.pulses), self.nt),
                                    dtype=int) * narrays
        temp_MiB = total_temp_size * np.dtype(float).itemsize / (1024 ** 2)
        result_MiB = total_result_size * np.dtype(float).itemsize / (1024 ** 2)

        msg = (f'Pulse convolver:\n'
               '=================================\n'
               f'Density matrix buffers:\n'
               f'  Buffers hold {narrays} arrays ({self.describe_reim()}, {self.describe_derivatives()})\n'
               f'  Temporary buffer - {temp_shape}\n'
               f'  for a size of {temp_MiB:.1f}MiB on {maxnchunks} ranks\n'
               f'  After parallel redistribution  - {result_shape}\n'
               f'  for a size of {result_MiB:.1f}MiB on {self.nranks_result} ranks\n'
               f''
               )
        self.log.log(msg, flush=True)

    def distributed_work(self) -> list[list[int]]:
        # Empty list for ranks that will not have any part of the result
        timet_r = self.comm.size * [[]]
        for r, rank in enumerate(self.result_on_ranks):
            timet_r[rank] = list(range(r, self.nt, self.nranks_result))

        return timet_r

    def my_work(self) -> list[int]:
        timet_r = self.distributed_work()
        return timet_r[self.comm.rank]

    def create_out_buffer(self) -> DensityMatrixBuffer:
        """ Create the DensityMatrixBuffer to hold the temporary density matrix after each redistribution """
        parameters = self.rho_nn_reader._parameters
        nlocalt = self.nlocalt if self.comm.rank in self.result_on_ranks else 0
        out_dm = DensityMatrixBuffer(nnshape=parameters.nnshape,
                                     xshape=(self.nchunks, len(self.pulses), nlocalt),
                                     dtype=np.float64)
        out_dm.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        return out_dm

    def create_result_buffer(self) -> DensityMatrixBuffer:
        """ Create the DensityMatrixBuffer to hold the resulting density matrix """
        parameters = self.rho_nn_reader._parameters
        nnshape = parameters.full_nnshape
        full_dm = DensityMatrixBuffer(nnshape=nnshape,
                                      xshape=(len(self.pulses), len(self.my_work())),
                                      dtype=np.float64)
        full_dm.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        return full_dm

    def redistribute(self) -> DensityMatrixBuffer:
        """ Perform the pulse convolution and redistribute the data

        When the pulse convolution is performed, the data is distributed such that each rank
        stores the entire time series for one chunk of the density matrices, i.e. indices n1, n2.

        This function then performs a redistribution of the data such that each rank stores full
        density matrices, for certain times.

        If the density matrices are split into more chunks than there are ranks, then the
        chunks are read, convoluted with pulses and distributed in a loop several times until all
        data has been processed.

        Returns
        -------
        Density matrix buffer with x-dimensions (Number of pulses, Number of local times)
        where the Number of local times variers between the ranks.
        """
        local_work = iter(self)
        parameters = self.rho_nn_reader._parameters
        log = self.log
        self.rho_nn_reader.rho_wfs_reader.lcao_rho_reader.striden == 0, \
            'n stride must be 0 (index all) for redistribute'

        # Time indices of result on each rank
        timet_r = self.distributed_work()

        out_dm = self.create_out_buffer()
        full_dm = self.create_result_buffer()

        _exhausted = object()

        niters = len(list(self.work_loop_by_ranks()))
        # Loop over the chunks of the density matrix
        for chunki, indices_r in enumerate(self.work_loop_by_ranks()):
            # At this point, each rank stores one unique chunk of the density matrix.
            # All ranks have the entire time series of data for their own chunk.
            # If there are more chunks than ranks, then this loop will run
            # for several iterations. If the number of chunks is not divisible by the number of
            # ranks then, during the last iteration, some of the chunks are None (meaning the rank
            # currently has no data).

            # List of chunks that each rank currently stores, where element r of the list
            # contains the chunk that rank r works with. Ranks higher than the length of the list
            # currently store no chunks.
            # The list itself is identical on all ranks.
            chunks_by_rank = [indices[2:] for indices in indices_r if indices is not None]

            ntargets = len(chunks_by_rank)

            if self.comm.rank < ntargets:
                # This rank has data to send. Compute the pulse convolution and store the result
                dm_buffer = next(local_work)
            else:
                # This rank has no data to send
                assert next(local_work, _exhausted) is _exhausted
                # Still, we need to create a dummy buffer
                dm_buffer = DensityMatrixBuffer(nnshape=parameters.nnshape,
                                                xshape=(0, 0), dtype=np.float64)
                dm_buffer.zero_buffers(real=self.yield_re, imag=self.yield_im,
                                       derivative_order_s=self.derivative_order_s)

            log.start('alltoallv')

            # Redistribute the data:
            # - dm_buffer stores single chunks of density matrices, for all times and pulses.
            # - out_dm will store several chunks, for a few times
            # source_indices_r describes which slices of dm_buffer should be sent to which rank
            # target_indices_r describes to which positions of the out_dm buffer should be received
            # from which rank
            source_indices_r = [None if len(t) == 0 else (slice(None), t) for t in timet_r]
            target_indices_r = [r if r < ntargets else None for r in range(self.comm.size)]
            dm_buffer.redistribute(out_dm,
                                   comm=self.comm,
                                   source_indices_r=source_indices_r,
                                   target_indices_r=target_indices_r,
                                   log=log)

            if self.comm.rank == 0:
                log(f'Chunk {chunki+1}/{niters}: distributed convoluted response in '
                    f'{log.elapsed("alltoallv"):.1f}s', flush=True)

            # Copy the redistributed data into the aggregated results buffer
            for array_nnrpt, full_array_nnpt in zip(out_dm._iter_buffers(), full_dm._iter_buffers()):
                for r, nn_indices in enumerate(chunks_by_rank):
                    safe_fill_larger(full_array_nnpt[nn_indices], array_nnrpt[:, :, r])

        assert next(local_work, _exhausted) is _exhausted

        return full_dm
