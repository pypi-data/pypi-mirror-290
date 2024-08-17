from __future__ import annotations

from typing import Generator

import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.tddft.units import au_to_eV, eV_to_au
from gpaw.mpi import world

from .distributed import create_fourier_transformer
from .density_matrix import DensityMatrix
from .base import BaseDensityMatrices, WorkMetadata
from ..utils import Logger, two_communicator_sizes


class FrequencyDensityMatrixMetadata(WorkMetadata):
    """ Metadata to the density matrices """
    density_matrices: FrequencyDensityMatrices
    globalw: int
    localw: int
    globalr: int
    localr: int

    def __new__(cls,
                density_matrices: FrequencyDensityMatrices,
                globalw: int,
                globalr: int,
                localw: int,
                localr: int):
        self = WorkMetadata.__new__(cls, density_matrices=density_matrices)
        self.globalw = globalw
        self.globalr = globalr
        self.localw = localw
        self.localr = localr
        return self

    @property
    def global_indices(self):
        return (self.globalw, self.globalr)

    @property
    def freq(self) -> float:
        """ Frequency in eV """
        return self.density_matrices.frequencies[self.globalw]

    @property
    def reim(self) -> str:
        """ Returns real/imaginary tag 'Re' or 'Im'

        The tag corresponds to the Fourier transform of the real
        or imaginary part of the density matrix
        """
        return self.density_matrices.reim[self.globalr]

    @property
    def desc(self) -> str:
        return f'{self.reim} @ Freq. {self.freq:.3f}eV'


class FrequencyDensityMatrices(BaseDensityMatrices[FrequencyDensityMatrixMetadata]):

    """
    Collection of density matrices in the Kohn-Sham basis in the frequency
    domain, for different frequencies.

    Plain density matrices and/or derivatives thereof may be represented.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    frequencies
        Compute density matrices for these frequencies (or as close to them as possible). In eV
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate the Fourier transform of the real part of the density matrix
    imag
        Calculate the Fourier transform of the imaginary part of the density matrix
    calc_size
        Size of the calculation communicator
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 frequencies: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1,
                 log: Logger | None = None):
        self._freq_w = np.array(frequencies)

        super().__init__(ksd=ksd,
                         derivative_order_s=derivative_order_s,
                         real=real, imag=imag,
                         calc_size=calc_size, log=log)

    @property
    def frequencies(self) -> NDArray[np.float64]:
        """ Frequncies in eV """
        return self._freq_w

    def work_loop(self,
                  rank: int) -> Generator[FrequencyDensityMatrixMetadata | None, None, None]:
        nw = len(self.frequencies)
        nwperrank = (nw + self.loop_comm.size - 1) // self.loop_comm.size

        for localw in range(nwperrank):
            globalw = rank + localw * self.loop_comm.size
            for r in range(len(self.reim)):
                if globalw < nw:
                    yield FrequencyDensityMatrixMetadata(density_matrices=self, globalw=globalw,
                                                         localw=localw, globalr=r, localr=r)
                else:
                    yield None


class FrequencyDensityMatricesFromDisk(FrequencyDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis in the frequency
    domain, for different frequencies. Read from disk.

    Plain density matrices and/or derivatives thereof may be represented.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    frho_fmt
        The pulserho_fmt is a formatting string for the density matrices
        in frequency space saved to disk. Example:

        frho_fmt = 'frho/w{freq:05.2f}-{reim}.npy'

        Should accept variables {freq} and {reim}
    frequencies
        Compute density matrices for these frequencies (or as close to them as possible). In eV
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
    real
        Calculate the Fourier transform of the real part of the density matrix
    imag
        Calculate the Fourier transform of the imaginary part of the density matrix
    calc_size
        Size of the calculation communicator
    kickstr
        Strength of the delta kick used during time propagation
    """

    def __init__(self,
                 ksd: KohnShamDecomposition | str,
                 frho_fmt: str,
                 frequencies: list[float] | NDArray[np.float64],
                 real: bool = True,
                 imag: bool = True,
                 derivative_order_s: list[int] = [0],
                 calc_size: int = 1,
                 kickstr: float = 1e-5):
        super().__init__(ksd=ksd, frequencies=frequencies,
                         real=real, imag=imag,
                         derivative_order_s=derivative_order_s, calc_size=calc_size)
        self.frho_fmt = frho_fmt
        self.kickstr = kickstr

    def __iter__(self) -> Generator[tuple[FrequencyDensityMatrixMetadata, DensityMatrix], None, None]:
        from gpaw.tddft.units import eV_to_au

        omega_w = self.frequencies * eV_to_au
        for work in self.local_work_plan:
            self.log.start('read')
            matrices: dict[int, NDArray[np.complex64] | None] = dict()
            for derivative in self.derivative_order_s:
                if self.calc_comm.rank > 0:
                    # Don't read on non calc comm root ranks
                    matrices[derivative] = None
                    continue

                fname_kw = dict(freq=work.freq, reim=work.reim)
                fname = self.frho_fmt.format(**fname_kw)

                f = np.load(fname)
                if isinstance(f, np.lib.npyio.NpzFile):
                    # Read npz file
                    rho = f['rho_p']
                    f.close()
                else:
                    # Read npy file
                    assert isinstance(f, np.ndarray)
                    rho = f

                # Apply scale
                if derivative == 1:
                    rho *= -1.0j * omega_w[work.globalw]
                elif derivative == 2:
                    rho *= -1.0 * omega_w[work.globalw] ** 2

                if self.ksd.only_ia:
                    # Twice the rho is saved by the KohnShamDecomposition transform
                    rho /= 2

                matrices[derivative] = rho

            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=True)

            yield work, dm


class FrequencyDensityMatricesFromWaveFunctions(FrequencyDensityMatrices):

    """
    Collection of density matrices in the Kohn-Sham basis in the frequency
    domain, for different frequencies. Obtained from the wave functions dump file,
    which is read from disk.

    Plain density matrices and/or derivatives thereof may be represented.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    wfs_fname
        Filename of the GPAW wave functions dump file
    frequencies
        Compute density matrices for these frequencies (or as close to them as possible). In eV
    derivative_order_s
        Compute density matrix derivatives of the following orders.
        0 for plain density matrix and positive integers for derivatives
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
                 frequencies: list[float] | NDArray[np.float64],
                 real: bool = True,
                 imag: bool = True,
                 derivative_order_s: list[int] = [0],
                 calc_size: int = 1,
                 stride_opts=None,
                 stridet: int = 1):
        _, calc_size = two_communicator_sizes(-1, calc_size)
        # The calc_comm rank 0's are world ranks 0, with a spacing of calc_size
        result_on_ranks = list(range(0, world.size, calc_size))

        rho_nn_fft = create_fourier_transformer(wfs_fname, ksd,
                                                yield_re=real, yield_im=imag,
                                                filter_frequencies=np.array(frequencies) * eV_to_au,
                                                stride_opts=stride_opts,
                                                stridet=stridet,
                                                result_on_ranks=result_on_ranks)
        self.rho_nn_fft = rho_nn_fft
        super().__init__(ksd=rho_nn_fft.ksd, frequencies=rho_nn_fft.freq_w * au_to_eV,
                         real=real, imag=imag,
                         derivative_order_s=derivative_order_s, calc_size=calc_size,
                         log=rho_nn_fft.log)

    @property
    def myw(self) -> list[int]:
        """ List of indices corresponding to the frequency indices on held on this rank """
        return self.rho_nn_fft.my_work()

    def __iter__(self) -> Generator[tuple[FrequencyDensityMatrixMetadata, DensityMatrix], None, None]:
        parameters = self.rho_nn_fft.rho_nn_reader._parameters
        flt = (slice(parameters.n1size), slice(parameters.n2size))

        dist_buffer = self.rho_nn_fft.dist_buffer  # Perform the redistribution
        self.log.comm = self.loop_comm  # Indicate in the logger that we are now working on the loop comm
        self.ksd.distribute(self.calc_comm)

        omega_w = self.frequencies * eV_to_au

        for work in self.local_work_plan:
            if self.calc_comm.rank == 0:
                assert self.myw[work.localw] == work.globalw

            matrices: dict[int, NDArray[np.complex64] | None] = dict()
            for derivative in self.derivative_order_s:
                if self.calc_comm.rank > 0:
                    matrices[derivative] = None
                    continue
                # Buffer shape is i, a, frequencies
                rho_ia = dist_buffer._get_data(work.reim == 'Re', 0)[flt + (work.localw, )]
                if derivative == 1:
                    rho_ia = rho_ia * 1.0j * omega_w[work.globalw]  # TODO * -1j
                elif derivative == 2:
                    rho_ia = - rho_ia * omega_w[work.globalw] ** 2
                matrices[derivative] = rho_ia
            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm

    def parallel_prepare(self):
        self.rho_nn_fft.dist_buffer  # Perform the redistribution
