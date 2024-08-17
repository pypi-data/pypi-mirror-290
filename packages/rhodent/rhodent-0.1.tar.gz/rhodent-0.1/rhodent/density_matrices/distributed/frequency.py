from __future__ import annotations

from typing import Generator
import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

from .base import BaseDistributor, RhoIndices
from .time import TimeDistributor
from .utils import fast_pad
from ..buffer import DensityMatrixBuffer
from ...utils import Logger, get_array_filter, safe_fill_larger
from ...typing import Communicator


class FourierTransformer(BaseDistributor):

    """ Iteratively take the Fourier transform of density matrices

    Parameters
    ----------
    rho_nn_reader
        Object that can iteratively read density matrices in the time domain,
        distributed such that different ranks have different chunks of the density
        matrix, but each ranks has all times for the
        same chunk.
    filter_frequencies
        After Fourier transformation keep only these frequencies (or the frequencies
        closest to them). In atomic units
    result_on_ranks
        List of ranks among which the resulting arrays will be distributed.
        Empty list (default) to distribute among all ranks.
    """

    def __init__(self,
                 rho_nn_reader: TimeDistributor,
                 filter_frequencies: list[float] | NDArray[np.float64] | None = None,
                 result_on_ranks: list[int] = []):
        self.rho_nn_reader = rho_nn_reader
        self._flt_w = get_array_filter(self._omega_w, filter_frequencies)
        nnshape = (self.rho_nn_reader._parameters.n1size, self.rho_nn_reader._parameters.n2size)
        xshape = (self.nw, )

        if len(result_on_ranks) == 0:
            self._result_on_ranks = set(range(self.comm.size))
        else:
            assert all(isinstance(rank, int) and rank >= 0 and rank < self.comm.size
                       for rank in result_on_ranks), result_on_ranks
            self._result_on_ranks = set(result_on_ranks)

        self._dist_buffer: DensityMatrixBuffer | None = None
        super().__init__(nnshape, xshape, complex, 'FFT', derivative_order_s=[0])

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
        return self.rho_nn_reader.time_t

    @property
    def nchunks(self) -> int:
        """ Count the number of chunks (number of source ranks doing work) """
        for chunks_r in self.work_loop_by_ranks():
            nchunks = len([chunk for chunk in chunks_r if chunk is not None])
            return nchunks

        raise RuntimeError

    @property
    def nw(self) -> int:
        return len(self.freq_w)

    @property
    def nlocalw(self) -> int:
        return (self.nw + self.nranks_result - 1) // self.nranks_result

    @property
    def result_on_ranks(self) -> list[int]:
        """ Set of ranks among which the result will be distributed """
        return sorted(self._result_on_ranks)

    @property
    def nranks_result(self) -> int:
        """ Number of ranks that the resulting arrays will be distributed among """
        return len(self._result_on_ranks)

    @property
    def nt(self) -> int:
        return len(self.time_t)

    @property
    def padnt(self) -> int:
        return fast_pad(self.nt)

    @property
    def dt(self) -> float:
        time_t = self.time_t
        return time_t[1] - time_t[0]

    @property
    def freq_w(self) -> NDArray[np.float64]:
        return self._omega_w[self.flt_w]

    @property
    def _omega_w(self) -> NDArray[np.float64]:
        time_t = self.time_t
        dt = self.dt

        assert np.allclose(time_t[1:] - dt, time_t[:-1]), 'Variable time step'
        omega_w = 2 * np.pi * np.fft.rfftfreq(self.padnt, dt)
        return omega_w

    @property
    def flt_w(self) -> slice | NDArray[np.bool_]:
        return self._flt_w

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
        padnt = self.padnt

        dm_buffer = DensityMatrixBuffer(self.rho_nn_reader._parameters.nnshape,
                                        (self.nw, ),
                                        np.complex64)
        if self.yield_re:
            dm_buffer.zeros(True, 0)
        if self.yield_im:
            dm_buffer.zeros(False, 0)

        for read_buffer in self.rho_nn_reader:
            for data_nnt, buffer_nnw in zip(read_buffer._iter_buffers(), dm_buffer._iter_buffers()):
                data_nnw = np.fft.rfft(data_nnt, n=padnt, axis=-1)[..., self.flt_w] * self.dt
                buffer_nnw[:] = data_nnw

            yield dm_buffer.copy()

    def gather_on_root(self) -> Generator[DensityMatrixBuffer | None, None, None]:
        self.rho_nn_reader.C0S_sknM   # Make sure to read this synchronously
        yield from super().gather_on_root()

    def distributed_work(self) -> list[list[int]]:
        freqw_r = self.comm.size * [[]]
        for r, rank in enumerate(self.result_on_ranks):
            freqw_r[rank] = list(range(r, self.nw, self.nranks_result))

        return freqw_r

    def my_work(self) -> list[int]:
        freqw_r = self.distributed_work()
        return freqw_r[self.comm.rank]

    def create_out_buffer(self) -> DensityMatrixBuffer:
        """ Create the DensityMatrixBuffer to hold the temporary density matrix after each redistribution """
        parameters = self.rho_nn_reader._parameters
        nlocalw = self.nlocalw if self.comm.rank in self.result_on_ranks else 0
        out_dm = DensityMatrixBuffer(nnshape=parameters.nnshape,
                                     xshape=(self.nchunks, nlocalw),
                                     dtype=np.complex64)
        out_dm.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        return out_dm

    def create_result_buffer(self) -> DensityMatrixBuffer:
        """ Create the DensityMatrixBuffer to hold the resulting density matrix """
        parameters = self.rho_nn_reader._parameters
        nnshape = parameters.full_nnshape
        full_dm = DensityMatrixBuffer(nnshape=nnshape,
                                      xshape=(len(self.my_work()), ),
                                      dtype=np.complex64)
        full_dm.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        return full_dm

    def redistribute(self) -> DensityMatrixBuffer:
        """ Perform the Fourier transform and redistribute the data

        When the Fourier transform is performed, the data is distributed such that each rank
        stores the entire time/frequency series for one chunk of the density matrices, i.e. indices n1, n2.

        This function then performs a redistribution of the data such that each rank stores full
        density matrices, for certain frequencies.

        If the density matrices are split into more chunks than there are ranks, then the
        chunks are read, Fourier transformed and distributed in a loop several times until all
        data has been processed.

        Returns
        -------
        Density matrix buffer with x-dimensions (Number of local frequencies, )
        where the Number of local frequencies variers between the ranks.
        """
        local_work = iter(self)
        parameters = self.rho_nn_reader._parameters
        log = self.log
        self.rho_nn_reader.rho_wfs_reader.lcao_rho_reader.striden == 0, \
            'n stride must be 0 (index all) for redistribute'

        # Frequency indices of result on each rank
        freqw_r = self.distributed_work()
        niters = len(list(self.work_loop_by_ranks()))

        out_dm = self.create_out_buffer()
        full_dm = self.create_result_buffer()

        _exhausted = object()

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
                # This rank has data to send. Compute the Fourier transform and store the result
                dm_buffer = next(local_work)
            else:
                # This rank has no data to send
                assert next(local_work, _exhausted) is _exhausted
                # Still, we need to create a dummy buffer
                dm_buffer = DensityMatrixBuffer(nnshape=parameters.nnshape,
                                                xshape=(0, ), dtype=np.complex64)
                dm_buffer.zero_buffers(real=self.yield_re, imag=self.yield_im,
                                       derivative_order_s=self.derivative_order_s)

            log.start('alltoallv')

            # Redistribute the data:
            # - dm_buffer stores single chunks of density matrices, for all frequencies.
            # - out_dm will store several chunks, for a few frequencies.
            # source_indices_r describes which slices of dm_buffer should be sent to which rank
            # target_indices_r describes to which positions of the out_dm buffer should be received
            # from which rank
            source_indices_r = [None if len(w) == 0 else w for w in freqw_r]
            target_indices_r = [r if r < ntargets else None for r in range(self.comm.size)]
            dm_buffer.redistribute(out_dm,
                                   comm=self.comm,
                                   source_indices_r=source_indices_r,
                                   target_indices_r=target_indices_r,
                                   log=log)

            if self.comm.rank == 0:
                log(f'Chunk {chunki+1}/{niters}: distributed frequency response in '
                    f'{log.elapsed("alltoallv"):.1f}s', flush=True)

            for array_nnrw, full_array_nnw in zip(out_dm._iter_buffers(), full_dm._iter_buffers()):
                for r, nn_indices in enumerate(chunks_by_rank):
                    safe_fill_larger(full_array_nnw[nn_indices], array_nnrw[:, :, r])

        assert next(local_work, _exhausted) is _exhausted

        return full_dm
