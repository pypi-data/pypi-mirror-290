from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Collection, Generator, Iterator

from gpaw.mpi import world
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.laser import GaussianPulse
from gpaw.tddft.units import eV_to_au

from rhodent.density_matrices.buffer import DensityMatrixBuffer
from rhodent.density_matrices.density_matrix import DensityMatrix
from rhodent.density_matrices.readers.gpaw import KohnShamRhoWfsReader, LCAORhoWfsReader
from rhodent.density_matrices.frequency import FrequencyDensityMatrices
from rhodent.density_matrices.time import (TimeDensityMatrices, ConvolutionDensityMatrices,
                                           TimeDensityMatrixMetadata, ConvolutionDensityMatrixMetadata)
from rhodent.utils import Logger, add_fake_kpts
from rhodent.voronoi import AtomProjectionsType, VoronoiWeights


class MockVoronoiWeights(VoronoiWeights):

    """ Read Voronoi weights from ulm file.

    Parameters
    ----------
    nn
        Number of states
    atom_projections
        List of projections on atoms
    dtype
        Datatype of weights
    broadcast_weights
        If true, the array of weights is broadcasted and yielded on all ranks
    comm
        GPAW MPI communicator object. Defaults to world
    """

    _nn: int
    _dtype: np.dtype
    _atom_projections: AtomProjectionsType

    def __init__(self,
                 nn: int,
                 atom_projections: AtomProjectionsType,
                 dtype: np.dtype = float,
                 broadcast_weights: bool = False,
                 comm=None):
        self.broadcast_weights = broadcast_weights

        if comm is None:
            comm = world

        self._log = Logger(comm=comm)
        self._comm = comm
        self._atom_projections = atom_projections
        self._nn = nn
        self._dtype = np.dtype(dtype)

    @property
    def atom_projections(self) -> AtomProjectionsType:
        return self._atom_projections

    @property
    def nn(self) -> int:
        return self._nn

    @property
    def dtype(self) -> np.dtype:
        return self._dtype

    def __iter__(self) -> Iterator[NDArray[np.float64] | None]:
        shape = (self.nn, self.nn)
        for proj_atoms in self.atom_projections:
            if self.comm.rank == 0:
                weight_nn = np.zeros(shape, self.dtype)
                for a in proj_atoms:
                    rng = np.random.default_rng(1423 + 13 * a)
                    weight_nn += rng.uniform(-1e-5, 1e-5, shape)
            else:
                if self.broadcast_weights:
                    weight_nn = np.empty(shape, self.dtype)
                else:
                    weight_nn = None
            if self.broadcast_weights:
                self.comm.broadcast(weight_nn, 0)

            yield weight_nn

    @property
    def saved_fields(self):
        return {}


class MockLCAOWfsReader(LCAORhoWfsReader):

    def __init__(self):
        self._striden = 0
        self._rho0_skMM = 0


class MockKohnShamRhoWfsReader(KohnShamRhoWfsReader):
    """ Pretend reader of Kohn-Sham density matrices

    Yield density matrices time by time

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename to the ksd file
    comm
        MPI communicator
    yield_re
        Whether to yield the real part of wave functions/density matrices
    yield_im
        Whether to yield the imaginary part of wave functions/density matrices
    filter_times
        A list of times to generate in au
    log
        Logger object
    """
    def __init__(self,
                 ksd: str | KohnShamDecomposition,
                 comm=world,
                 yield_re: bool = True,
                 yield_im: bool = True,
                 filter_times: list[float] | NDArray[np.float64] | None = None,
                 log: Logger | None = None):
        if comm is None:
            comm = world
        self._comm = comm

        # Set up ksd
        if isinstance(ksd, KohnShamDecomposition):
            self._ksd = ksd
        else:
            self._ksd = KohnShamDecomposition(filename=ksd)
            add_fake_kpts(self._ksd)

        if log is None:
            log = Logger(comm=self.comm)
        self._log = log
        self._time_t = np.array(filter_times)
        self._flt_t = slice(None)
        self._yield_re = yield_re
        self._yield_im = yield_im

        self._C0S_sknM: NDArray[np.float64] | None = None
        self._rho0_sknn: NDArray[np.float64] | None = None
        self.lcao_rho_reader = MockLCAOWfsReader()

    def iread(self,
              s: int,
              k: int,
              n1: slice,
              n2: slice) -> Generator[DensityMatrixBuffer, None, None]:
        """ Read the density matrices time by time

        Parameters
        ----------
        s, k, n1, n2
            Read these indices
        """
        dm_buffer = DensityMatrixBuffer(self.nnshape(s, k, n1, n2), (), np.float64)
        if self.yield_re:
            dm_buffer.zeros(True, 0)
        if self.yield_im:
            dm_buffer.zeros(False, 0)
        self.C0S_sknM  # Read this on all ranks
        nn = self.C0S_sknM.shape[3]
        full_nnshape = (nn, nn)

        for globalt in self.work_loop(self.comm.rank):
            if globalt is None:
                continue
            self.log.start('read')
            rngseed = globalt + 832 * s + 42140 * k

            if self.yield_re:
                rng = np.random.default_rng(32636 + rngseed)
                Rerho_x = rng.uniform(-1e-5, 1e-5, full_nnshape)[n1, n2]
                dm_buffer.safe_fill(True, 0, Rerho_x)
            if self.yield_im:
                rng = np.random.default_rng(94234 + rngseed)
                Rerho_x = rng.uniform(-1e-5, 1e-5, full_nnshape)[n1, n2]
                dm_buffer.safe_fill(False, 0, Rerho_x)

            yield dm_buffer


class MockTimeDensityMatrices(TimeDensityMatrices):

    """
    Pretend TimeDensityMatrices that are filled with random values.

    The random values are generated using a fixed seed

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    times
        Produce density matrices for these times. In as
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
                 calc_size: int = 1):
        super().__init__(ksd=ksd, times=times, calc_size=1, real=real, imag=imag)

        imin, imax, amin, amax = self.ksd.ialims()

        # Read density matrices corresponding to ksd ialims
        self._n1slice = slice(imin, imax + 1)
        self._n2slice = slice(amin, amax + 1)

        self._runtime_verify_work_loop()

        self._time_t = np.array(times)

    def __iter__(self) -> Generator[tuple[TimeDensityMatrixMetadata, DensityMatrix], None, None]:
        shape = (self._n1slice.stop - self._n1slice.start, self._n2slice.stop - self._n2slice.start)
        assert self.calc_comm.size == 1  # TODO

        for work in self.work_loop(self.loop_comm.rank):
            if work is None:
                # Nothing more to do
                return

            rho_ia = np.zeros(shape, dtype=complex)

            if 'Re' in self.reim:
                rng = np.random.default_rng(248203 + work.globalt)
                rho_ia += rng.uniform(-1e-5, 1e-5, shape)
            if 'Im' in self.reim:
                rng = np.random.default_rng(614203 + work.globalt)
                rho_ia += 1.0j * rng.uniform(-1e-5, 1e-5, shape)

            matrices = {0: rho_ia}
            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm

    def work_loop(self,
                  rank: int) -> Generator[TimeDensityMatrixMetadata | None, None, None]:
        nt = self.nt
        ntperrank = (nt + self.loop_comm.size - 1) // self.loop_comm.size

        for localt in range(ntperrank):
            globalt = rank + localt * self.loop_comm.size
            if globalt < nt:
                yield TimeDensityMatrixMetadata(density_matrices=self, globalt=globalt, localt=localt)
            else:
                yield None


class MockConvolutionDensityMatrices(ConvolutionDensityMatrices):

    """
    Pretend ConvolutionDensityMatrices that are filled with random values.

    The random values are generated using a fixed seed

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    pulses
        Convolute the density matrices with these pulses
    times
        Produce density matrices for these times. In as
    derivative_order_s
        Density matrix derivatives of the following orders.
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
                 calc_size: int = 1):
        super().__init__(ksd=ksd, times=times, pulses=pulses,
                         derivative_order_s=derivative_order_s, calc_size=calc_size, real=real, imag=imag)

        imin, imax, amin, amax = self.ksd.ialims()

        # Read density matrices corresponding to ksd ialims
        self._n1slice = slice(imin, imax + 1)
        self._n2slice = slice(amin, amax + 1)

        self._runtime_verify_work_loop()

        self._time_t = np.array(times)

    def __iter__(self) -> Generator[tuple[ConvolutionDensityMatrixMetadata, DensityMatrix], None, None]:
        shape = (self._n1slice.stop - self._n1slice.start, self._n2slice.stop - self._n2slice.start)

        for work in self.local_work_plan:
            matrices = dict()
            seeds = {0: 0, 1: 992292, 2: 1281934}
            for derivative in self.derivative_order_s:
                if self.calc_comm.rank > 0:
                    matrices[derivative] = None
                    continue
                rho_ia = np.zeros(shape, dtype=complex)
                seed = seeds[derivative] + work.globalt + int(11403 * work.pulse.omega0)

                if 'Re' in self.reim:
                    rng = np.random.default_rng(seed + 573929)
                    rho_ia += rng.uniform(-1e-5, 1e-5, shape)
                if 'Re' in self.reim:
                    rng = np.random.default_rng(seed + 156305)
                    rho_ia += 1.0j * rng.uniform(-1e-5, 1e-5, shape)
                matrices[derivative] = rho_ia

            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm


class MockFrequencyDensityMatrices(FrequencyDensityMatrices):

    """
    Pretend FrequencyDensityMatrices that are filled with random values.

    The random values are generated using a fixed seed

    Parameters
    ----------
    ksd
        KohnShamDecomposition object or filename
    frequencies
        Produce density matrices for these frequencies. In eV
    derivative_order_s
        Density matrix derivatives of the following orders.
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
                 frequencies: list[float] | NDArray[np.float64],
                 derivative_order_s: list[int] = [0],
                 real: bool = True,
                 imag: bool = True,
                 calc_size: int = 1):
        super().__init__(ksd=ksd, frequencies=frequencies, derivative_order_s=derivative_order_s,
                         calc_size=calc_size, real=real, imag=imag)

        imin, imax, amin, amax = self.ksd.ialims()

        # Read density matrices corresponding to ksd ialims
        self._n1slice = slice(imin, imax + 1)
        self._n2slice = slice(amin, amax + 1)

        self._runtime_verify_work_loop()

    def __iter__(self) -> Generator[tuple[ConvolutionDensityMatrixMetadata, DensityMatrix], None, None]:
        shape = (self._n1slice.stop - self._n1slice.start, self._n2slice.stop - self._n2slice.start)
        omega_w = self.frequencies * eV_to_au

        for work in self.local_work_plan:
            seed = work.globalw + 1412 if work.reim == 'Re' else 0
            rng = np.random.default_rng(seed + 421420)
            rho_ia = np.zeros(shape, dtype=complex)
            rho_ia += rng.uniform(-1e-5, 1e-5, shape)
            rho_ia += 1.0j * rng.uniform(-1e-5, 1e-5, shape)

            matrices = dict()
            if self.calc_comm.rank == 0:
                if 0 in self.derivative_order_s:
                    matrices[0] = rho_ia
                if 1 in self.derivative_order_s:
                    matrices[1] = rho_ia * 1.0j * omega_w[work.globalw]  # TODO * -1j
                if 2 in self.derivative_order_s:
                    matrices[2] = - rho_ia * omega_w[work.globalw] ** 2
            else:
                matrices.update({order: None for order in self.derivative_order_s})

            dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=False)

            yield work, dm
