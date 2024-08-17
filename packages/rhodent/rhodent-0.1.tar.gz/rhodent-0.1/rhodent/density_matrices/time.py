from __future__ import annotations

from typing import Generator, Collection

import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.laser import GaussianPulse
from gpaw.tddft.units import as_to_au, au_to_as, au_to_eV, au_to_fs, eV_to_au, fs_to_au
from gpaw.mpi import world

from .distributed import create_density_matrix_reader, create_pulse_convolver
from .distributed.pulse import Perturbation
from .density_matrix import DensityMatrix
from .base import BaseDensityMatrices, WorkMetadata
from .frequency import FrequencyDensityMatricesFromDisk
from ..utils import Logger, two_communicator_sizes


class TimeDensityMatrixMetadata(WorkMetadata):
    """ Metadata to the density matrices """
    density_matrices: TimeDensityMatrices
    globalt: int
    localt: int

    def __new__(cls,
                density_matrices: TimeDensityMatrices,
                globalt: int,
                localt: int):
        self = WorkMetadata.__new__(cls, density_matrices=density_matrices)
        self.globalt = globalt
        self.localt = localt
        return self

    @property
    def global_indices(self):
        return (self.globalt, )

    @property
    def time(self) -> float:
        """ Simulation time in as """
        return self.density_matrices.times[self.globalt]

    @property
    def desc(self) -> str:
        return f'{self.time:.1f}as'


class ConvolutionDensityMatrixMetadata(WorkMetadata):
    """ Metadata to the density matrices """
    density_matrices: ConvolutionDensityMatrices
    globalt: int
    globalp: int
    localt: int
    localp: int

    def __new__(cls,
                density_matrices: ConvolutionDensityMatrices,
                globalt: int,
                globalp: int,
                localt: int,
                localp: int):
        self = WorkMetadata.__new__(cls, density_matrices=density_matrices)
        self.globalt = globalt
        self.globalp = globalp
        self.localt = localt
        self.localp = localp
        return self

    @property
    def global_indices(self):
        return (self.globalp, self.globalt)

    @property
    def time(self) -> float:
        """ Simulation time in as """
        return self.density_matrices.times[self.globalt]

    @property
    def pulse(self) -> GaussianPulse:
        return self.density_matrices.pulses[self.globalp]

    @property
    def desc(self) -> str:
        from gpaw.tddft.units import au_to_eV

        return f'{self.time:.1f}as @ Pulse {self.pulse.omega0 * au_to_eV:.1f}eV'


class TimeDensityMatrices(BaseDensityMatrices[TimeDensityMatrixMetadata]):

    """
    Collection of density matrices in the Kohn-Sham basis for different times.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    times
        Compute density matrices for these times (or as close to them as possible). In as
    real
        Calculate the real part of density matrices
    imag
        Calculate the imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 times: list[float] | NDArray[np.float64],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1,
                 log: Logger | None = None):
        self._time_t = np.array(times)
        super().__init__(ksd=ksd,
                         derivative_order_s=[0],
                         real=real, imag=imag,
                         calc_size=calc_size)

    def __str__(self) -> str:
        nt = len(self.times)
        assert nt > 0
        timesstr = f'{len(self.times)} times from {self.times[0]:.1f} to {self.times[-1]:.1f}as'
        return f'{self.__class__.__name__} with {timesstr}'

    def work_loop(self,
                  rank: int) -> Generator[TimeDensityMatrixMetadata | None, None, None]:
        if not hasattr(self, 'rho_nn_direct'):
            return
        for localt, globalt in enumerate(self.rho_nn_direct.work_loop(rank)):
            if globalt is not None:
                yield TimeDensityMatrixMetadata(density_matrices=self, globalt=globalt, localt=localt)
            else:
                yield None

    @property
    def times(self) -> NDArray[np.float64]:
        """ Simulation time in as """
        return self._time_t

    @property
    def nt(self) -> int:
        """ Number of times """
        return len(self.times)


class ConvolutionDensityMatrices(BaseDensityMatrices[ConvolutionDensityMatrixMetadata]):

    """
    Collection of density matrices in the Kohn-Sham basis for different times,
    after convolution with various pulses.

    Plain density matrices and/or derivatives thereof may be represented.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    pulses
        Convolute the density matrices with these pulses
    times
        Compute density matrices for these times (or as close to them as possible). In as
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate the real part of density matrices
    imag
        Calculate the imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 pulses: Collection[GaussianPulse],
                 times: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1,
                 log: Logger | None = None):
        self._time_t = np.array(times)
        self._pulses = list(pulses)
        super().__init__(ksd=ksd,
                         derivative_order_s=derivative_order_s,
                         real=real, imag=imag,
                         calc_size=calc_size)

    @property
    def times(self) -> NDArray[np.float64]:
        """ Simulation time in as """
        return self._time_t

    @property
    def nt(self) -> int:
        """ Number of times """
        return len(self.times)

    @property
    def pulses(self) -> list[GaussianPulse]:
        """ Pulses with which density matrices are convoluted """
        return self._pulses

    def work_loop(self,
                  rank: int) -> Generator[ConvolutionDensityMatrixMetadata | None, None, None]:
        nt = len(self.times)
        ntperrank = (nt + self.loop_comm.size - 1) // self.loop_comm.size

        # Do convolution pulse-by-pulse, time-by-time
        for p, pulse in enumerate(self.pulses):
            # Determine which times to compute on this loop_comm rank for good load balancing
            shift = (p * nt + rank) % self.loop_comm.size
            for localt in range(ntperrank):
                globalt = shift + localt * self.loop_comm.size
                if globalt < nt:
                    yield ConvolutionDensityMatrixMetadata(density_matrices=self, globalt=globalt,
                                                           localt=localt, globalp=p, localp=p)
                else:
                    yield None


class TimeDensityMatricesFromWaveFunctions(TimeDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis for different times,
    obtained by reading the wave functions dump file.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    wfs_fname
        Filename of the GPAW wave functions dump file
    times
        Compute density matrices for these times (or as close to them as possible). In as
    real
        Calculate the real part of density matrices
    imag
        Calculate the imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    stride_opts
        Options passed to the GPAW wave functions reader
    stridet
        Skip this many steps when reading wave function dump file
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 wfs_fname: str,
                 times: list[float] | NDArray[np.float64],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1,
                 stride_opts=None,
                 stridet: int = 1):
        rho_nn_direct = create_density_matrix_reader(wfs_fname, ksd,
                                                     yield_re=real, yield_im=imag,
                                                     filter_times=np.array(times) * as_to_au,
                                                     stridet=stridet)
        self.rho_nn_direct = rho_nn_direct
        assert rho_nn_direct.lcao_rho_reader.striden == 0

        super().__init__(ksd=rho_nn_direct.ksd,
                         times=rho_nn_direct.time_t * au_to_as,
                         calc_size=1,
                         log=rho_nn_direct.log)

        imin, imax, amin, amax = self.ksd.ialims()
        if stride_opts is None:
            stride_opts = dict()

        striden1 = stride_opts.pop('striden1', 0)
        striden2 = stride_opts.pop('striden2', 0)
        assert striden1 == 0, striden1
        assert striden2 == 0, striden2

        # Read density matrices corresponding to ksd ialims
        self._n1slice = slice(imin, imax + 1)
        self._n2slice = slice(amin, amax + 1)

    def __iter__(self) -> Generator[tuple[TimeDensityMatrixMetadata, DensityMatrix], None, None]:
        assert self.calc_comm.size == 1  # TODO

        for work, dm_buffer in zip(self.work_loop(self.loop_comm.rank),
                                   self.rho_nn_direct.iread(0, 0, self._n1slice, self._n2slice)):
            assert work is not None
            rho_ia = dm_buffer.real + 1j * dm_buffer.imag
            matrices = {0: rho_ia}
            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm

    def parallel_prepare(self):
        self.rho_nn_direct.parallel_prepare()


class ConvolutionDensityMatricesFromDisk(ConvolutionDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis after convolution with
    one or several pulses, for different times. Read from disk

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    pulserho_fmt:
        The pulserho_fmt is a formatting string for the density matrices
        saved to disk. Example:

        pulserho_fmt =  'pulserho/t{time:09.1f}{tag}.npy'
    pulses
        Convolute the density matrices with these pulses
    times
        Compute density matrices for these times (or as close to them as possible). In as
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate real part of density matrices
    imag
        Calculate imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 pulserho_fmt: str,
                 pulses: Collection[GaussianPulse],
                 times: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1):
        super().__init__(ksd=ksd, pulses=pulses, times=times,
                         derivative_order_s=derivative_order_s, calc_size=calc_size)
        self.pulserho_fmt = pulserho_fmt

    def __iter__(self) -> Generator[tuple[ConvolutionDensityMatrixMetadata, DensityMatrix], None, None]:
        tag_s = ['', '-Iomega', '-omega2']

        for work in self.local_work_plan:
            self.log.start('read')
            matrices: dict[int, NDArray[np.complex64] | None] = dict()
            for derivative in self.derivative_order_s:
                if self.calc_comm.rank > 0:
                    # Don't read on non calc comm root ranks
                    matrices[derivative] = None
                    continue

                fname_kw = dict(time=work.time, tag=tag_s[derivative],
                                pulsefreq=work.pulse.omega0 * au_to_eV,
                                pulsefwhm=1 / work.pulse.sigma * au_to_fs * (2 * np.sqrt(2 * np.log(2))))
                fname = self.pulserho_fmt.format(**fname_kw)

                f = np.load(fname)
                if isinstance(f, np.lib.npyio.NpzFile):
                    # Read npz file
                    rho = f['rho_p']
                    f.close()
                else:
                    # Read npy file
                    assert isinstance(f, np.ndarray)
                    rho = f

                matrices[derivative] = rho

            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=True)

            yield work, dm


class ConvolutionDensityMatricesFromFrequency(ConvolutionDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis after convolution with
    one or several pulses, for different times. Obtained from the the density
    matrices in frequency space, which are read from disk.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    frho_fmt
        The pulserho_fmt is a formatting string for the density matrices
        in frequency space saved to disk. Example:

        frho_fmt = 'frho/w{freq:05.2f}-{reim}.npy'

        Should accept variables {freq} and {reim}
    pulses
        Convolute the density matrices with these pulses
    times
        Compute density matrices for these times (or as close to them as possible). In as
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate real part of density matrices
    imag
        Calculate imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 frho_fmt: str,
                 pulses: Collection[GaussianPulse],
                 times: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1):
        super().__init__(ksd=ksd, pulses=pulses, times=times,
                         derivative_order_s=derivative_order_s, calc_size=calc_size)

        # Frequency grid for convolution
        full_freq_w = convolution_freq_w_many(self.pulses)

        freq_density_matrices = FrequencyDensityMatricesFromDisk(
            ksd=self.ksd, frho_fmt=frho_fmt, frequencies=full_freq_w,
            real=real, imag=imag,
            derivative_order_s=derivative_order_s, calc_size=calc_size)
        self.freq_density_matrices = freq_density_matrices

        # Currently, both objects are creating their own communicators
        assert self.loop_comm.rank == freq_density_matrices.loop_comm.rank
        assert self.loop_comm.size == freq_density_matrices.loop_comm.size
        assert self.calc_comm.rank == freq_density_matrices.calc_comm.rank
        assert self.calc_comm.size == freq_density_matrices.calc_comm.size

    def __iter__(self) -> Generator[tuple[ConvolutionDensityMatrixMetadata, DensityMatrix], None, None]:
        """
        First dimension: frequency (corresponding to the frequencies in freq_w)
        Second dimension: Plain density matrix, first derivative, second derivative,
                          in this order, but by omitting an index from s_included this
                          data can be skipped. Example

                          s_inlcuded = [0, 2]

                          rho_wsrq second dimension has size 2 and contains plain density matrix
                          and second derivative
        Third dimension: Size 2. First element is Fourier tranform of real part of density matrix
                                 second element Fourier transform of imaginary part of density matrix
        Fourth dimension: Compound index of electron-hole pair, distributed over calc_comm
        """
        import gc

        # Begin by reading the full matrix of all frequency density matrices on all ranks

        # Distribute the ksd over the calc_comm
        self.freq_density_matrices.ksd.distribute(self.calc_comm)
        self.ksd.distribute(self.calc_comm)

        # Read density matrix
        wsrq_shape = (len(self.freq_density_matrices.frequencies), len(self.tag_s), 2, len(self.ksd.w_q))
        full_rho_wsrq = np.zeros(wsrq_shape, dtype=complex)
        for fwork, dm in self.freq_density_matrices.iread_gather_on_root():
            w = fwork.globalw
            r = fwork.globalr
            self.log.start('distribute')
            for s, derivative in enumerate(self.derivative_order_s):
                rho_p = dm._get_rho(derivative, ravelled=True) if self.calc_comm.rank == 0 else None
                self.ksd.distribute_p(rho_p, full_rho_wsrq[w, s, r], root=0)
                del rho_p
            if self.loop_comm.rank == 0 and self.calc_comm.rank == 0:
                self.log(f'Distributed density matrix in {self.log.elapsed("distribute"):.1f}s', flush=True)
            gc.collect()
        full_rho_wsrq /= self.freq_density_matrices.kickstr

        full_freq_w = self.freq_density_matrices.frequencies

        matrices: dict[int, NDArray[np.complex64] | None]
        for work in self.local_work_plan:
            # Determine which subset of the full_freq_w is needed
            freq_w = convolution_freq_w(self.pulses[work.globalp])
            after_w = full_freq_w > freq_w[-1] + 1e-3
            startw: int = np.argmax(full_freq_w > freq_w[0] - 1e-3)  # type: ignore
            stopw: int = len(full_freq_w) if not any(after_w) else np.argmax(after_w)  # type: ignore

            # Extract the same subset of the density matrices
            rho_wsrq = full_rho_wsrq[startw:stopw]

            # Convolve
            convolver = FourierConvolver(work.pulse, freq_w * eV_to_au, rho_wsrq)
            self.log.start('convolve')
            pulserho_srq = convolver.convolve(work.time, units='as')
            if self.loop_comm.rank == 0 and self.calc_comm.rank == 0:
                self.log(f'Convolved density matrices in {self.log.elapsed("convolve"):.1f}s', flush=True)

            matrices = {}
            for derivative, pulserho_q in zip(self.derivative_order_s,
                                              pulserho_srq[:, 0] + 1.0j * pulserho_srq[:, 1]):
                pulserho_p = self.ksd.collect_q(pulserho_q, root=0)
                if self.calc_comm.rank == 0:
                    matrices[derivative] = pulserho_p
                else:
                    assert pulserho_p is None
                    matrices[derivative] = None

            del pulserho_srq
            del pulserho_p
            gc.collect()

            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=True)

            yield work, dm


class ConvolutionDensityMatricesFromWaveFunctions(ConvolutionDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis after convolution with
    one or several pulses, for different times. Obtained from the wave functions dump file,
    which is read from disk.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    wfs_fname
        Filename of the GPAW wave functions dump file
    perturbation
        Perturbation that was present during time propagation
    pulses
        Convolute the density matrices with these pulses
    times
        Compute density matrices for these times (or as close to them as possible). In as
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate real part of density matrices
    imag
        Calculate imaginary part of density matrices
    calc_size
        Size of the calculation communicator
    stride_opts
        Options passed to the GPAW wave functions reader
    stridet
        Skip this many steps when reading wave function dump file
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 wfs_fname: str,
                 perturbation: Perturbation | dict,
                 pulses: Collection[GaussianPulse],
                 times: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1,
                 stride_opts=None,
                 stridet: int = 1):
        _, calc_size = two_communicator_sizes(-1, calc_size)
        # The calc_comm rank 0's are world ranks 0, with a spacing of calc_size
        result_on_ranks = list(range(0, world.size, calc_size))

        rho_nn_conv = create_pulse_convolver(wfs_fname, ksd,
                                             pulses=pulses,
                                             perturbation=perturbation,
                                             yield_re=real, yield_im=imag,
                                             filter_times=np.array(times) * as_to_au,
                                             derivative_order_s=list(sorted(derivative_order_s)),
                                             stride_opts=stride_opts,
                                             stridet=stridet,
                                             result_on_ranks=result_on_ranks)
        self.rho_nn_conv = rho_nn_conv

        super().__init__(ksd=rho_nn_conv.ksd, pulses=pulses, times=rho_nn_conv.time_t * au_to_as,
                         derivative_order_s=derivative_order_s, calc_size=calc_size,
                         log=rho_nn_conv.log)

        self.rho_nn_conv.print_description()

    @property
    def myt(self) -> list[int]:
        """ List of indices corresponding to the time indices on held on this rank """
        return self.rho_nn_conv.my_work()

    def work_loop(self,
                  rank: int) -> Generator[ConvolutionDensityMatrixMetadata | None, None, None]:
        nt = len(self.times)
        ntperrank = (nt + self.loop_comm.size - 1) // self.loop_comm.size

        for p, pulse in enumerate(self.pulses):
            for localt in range(ntperrank):
                globalt = rank + localt * self.loop_comm.size
                if globalt < nt:
                    yield ConvolutionDensityMatrixMetadata(density_matrices=self, globalt=globalt,
                                                           localt=localt, globalp=p, localp=p)
                else:
                    yield None

    def __iter__(self) -> Generator[tuple[ConvolutionDensityMatrixMetadata, DensityMatrix], None, None]:
        parameters = self.rho_nn_conv.rho_nn_reader._parameters
        flt = (slice(parameters.n1size), slice(parameters.n2size))

        dist_buffer = self.rho_nn_conv.dist_buffer  # Perform the redistribution
        self.log.comm = self.loop_comm  # Indicate in the logger that we are now working on the loop comm
        self.ksd.distribute(self.calc_comm)

        if self.calc_comm.rank != 0:
            assert len(self.myt) == 0, self.myt

        for work in self.local_work_plan:
            if self.calc_comm.rank == 0:
                assert self.myt[work.localt] == work.globalt
            localflt = flt + (work.localp, work.localt)

            matrices: dict[int, NDArray[np.complex64] | None] = dict()
            for derivative in self.derivative_order_s:
                if self.calc_comm.rank > 0:
                    matrices[derivative] = None
                    continue
                # Buffer shape is i, a, pulses, times
                if 'Re' in self.reim:
                    Rerho_ia = dist_buffer._get_real(derivative)[localflt]
                if 'Im' in self.reim:
                    Imrho_ia = dist_buffer._get_imag(derivative)[localflt]
                if 'Re' in self.reim and 'Im' in self.reim:
                    # Complex result
                    # Compared to numpy, we use another convention, hence the minus sign
                    rho_ia = Rerho_ia - 1j * Imrho_ia
                elif 'Re' in self.reim:
                    # Real result
                    rho_ia = Rerho_ia
                else:
                    rho_ia = -1j * Imrho_ia
                matrices[derivative] = rho_ia
            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm

    def parallel_prepare(self):
        self.rho_nn_conv.dist_buffer  # Perform the redistribution


class FourierConvolver:
    """
    Convolve using Fourier transforms.

    Use given frequencies in Fourier transform.
    """

    def __init__(self, pulse, omega_w, data_wX):
        self.pulse = pulse

        # Impulse response data
        self.omega_w = omega_w
        d_wX = data_wX

        # Pulse in frequency space
        pulse_w = self.pulse.fourier(omega_w)

        # Convolution product
        d_Xw = np.moveaxis(d_wX, 0, -1)
        pd_Xw = d_Xw * pulse_w
        self.pd_wX = np.moveaxis(pd_Xw, -1, 0)

    def convolve(self, time, units='au'):
        # Convert time to ndarray
        time_t = np.array(time)
        if units == 'fs':
            time_t *= fs_to_au
        elif units == 'as':
            time_t *= as_to_au
        else:
            assert units == 'au'

        if time_t.ndim == 0:
            # If argument is a single number,
            # return value without time axis
            return self._convolve(time_t[np.newaxis])[0]

        return self._convolve(time_t)

    def _convolve(self, time_t):
        pd_tX = inversefourier(self.omega_w, self.pd_wX, time_t, None)
        return pd_tX


def fourier(time_t, a_tX, omega_w, folding='Gauss', width=0.08, sign=1.0):
    if width is None:
        folding = None

    if folding is None:
        def envelope(t):
            return 1.0
    else:
        width = width * eV_to_au
        if folding == 'Gauss':
            # f(w) = Nw exp(-w^2/2/sigma^2)
            # f(t) = exp(-t^2 sigma^2/2)
            def envelope(t):
                return np.exp(-0.5 * width**2 * t**2)
        elif folding == 'Lorentz':
            # f(w) = Nw eta / [omega^2 + (eta)^2]
            # f(t) = exp(-t eta)
            def envelope(t):
                return np.exp(-width * t)
        else:
            raise RuntimeError('unknown folding "' + folding + '"')

    dt_t = np.insert(time_t[1:] - time_t[:-1], 0, 0.0)
    f_wt = np.exp(sign * 1j * np.outer(omega_w, time_t))
    a_Xt = np.rollaxis(a_tX, 0, len(a_tX.shape))
    a_wX = np.tensordot(f_wt, dt_t * envelope(time_t) * a_Xt,
                        axes=(1, len(a_Xt.shape) - 1))
    return a_wX


def inversefourier(omega_w, a_wX, time_t, folding='Gauss', width=0.08):
    # This function assumes that time-domain quantity is real
    a_tX = fourier(omega_w, a_wX / (2 * np.pi), time_t, folding, width,
                   sign=-1)
    return 2 * a_tX.real


def convolution_freq_w(pulse: GaussianPulse) -> NDArray[np.float64]:
    """ Compute necessary frequency grid for the supplied pulses

    Parameters
    ----------
    pulse
        Laser pulse. The wider the pulse is in frequency
        the larger frequency grid is to be returned

    Returns
    -------
    Necessary frequency grid to perform the convolution
    """
    from gpaw.tddft.units import au_to_eV

    frequency = pulse.omega0 * au_to_eV
    sigma = pulse.sigma * au_to_eV

    freqmin = np.floor((frequency - 4 * sigma) * 20) / 20
    freqmin = max(freqmin, 0.05)
    freqmax = np.ceil((frequency + 4 * sigma) * 20) / 20
    freq_w = np.arange(freqmin, freqmax + 1e-4, 0.05)
    return freq_w


def convolution_freq_w_many(pulses: Collection[GaussianPulse]) -> NDArray[np.float64]:
    """ Compute necessary frequency grid for the supplied pulses

    Parameters
    ----------
    pulses
        List of laser pulses to consider. The wider the pulses are in frequency
        the larger frequency grid is to be returned

    Returns
    -------
    Necessary frequency grid to perform the convolution
    """
    from gpaw.tddft.units import au_to_eV

    omega0s = np.array([pulse.omega0 for pulse in pulses])
    sigmas = np.array([pulse.sigma for pulse in pulses])

    sigma = np.max(sigmas) * au_to_eV

    freqmin = np.floor((np.min(omega0s) * au_to_eV - 4 * sigma) * 20) / 20
    freqmin = max(freqmin, 0.05)
    freqmax = np.ceil((np.max(omega0s) * au_to_eV + 4 * sigma) * 20) / 20
    freq_w = np.arange(freqmin, freqmax + 1e-4, 0.05)
    return freq_w
