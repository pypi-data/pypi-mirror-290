from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator

import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.laser import GaussianPulse
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

from ..typing import Communicator
from ..density_matrices.base import BaseDensityMatrices, WorkMetadata
from ..density_matrices.time import TimeDensityMatrices, ConvolutionDensityMatrices
from ..density_matrices.frequency import FrequencyDensityMatrices
from ..voronoi import VoronoiWeights
from ..utils import Logger, ResultKeys, Result, broaden_n2e, broaden_xn2e, broaden_ia2ou


class BaseObservableCalculator(ABC):

    """ Object of this class compute observables.

    Parameters
    ----------
    density_matrices
        Object that gives the density matrix in the time or freqency domain
    voronoi
        Voronoi weights object
    energies_occ
        Energy grid (in eV) for occupied levels (hot holes)
    energies_unocc
        Energy grid (in eV) for unoccupied levels (hot electrons)
    sigma
        Gaussian broadening width in eV
    """

    def __init__(self,
                 density_matrices: BaseDensityMatrices,
                 voronoi: VoronoiWeights | None,
                 energies_occ: list[float] | NDArray[np.float64],
                 energies_unocc: list[float] | NDArray[np.float64],
                 sigma: float | None = None):
        self._density_matrices = density_matrices
        self._voronoi = voronoi
        self._energies_occ = np.asarray(energies_occ)
        self._energies_unocc = np.asarray(energies_unocc)
        self._sigma = sigma
        self._weight_In: NDArray[np.float64] | None = None
        self._weight_Iii: NDArray[np.float64] | None = None
        self._weight_Iaa: NDArray[np.float64] | None = None

    def __str__(self) -> str:
        lines = [f'{self.__class__.__name__}']

        if self.voronoi is None:
            lines.append('No Voronoi decomposition')
        else:
            lines += str(self.voronoi).split('\n') + ['']

        if len(self.energies_occ) == 0 or len(self.energies_unocc) == 0 or self.sigma is None:
            lines.append('No energies for broadening')
        else:
            lines += [f'Energies for broadening (sigma = {self.sigma:.1f} eV)',
                      f'  Occupied: {len(self.energies_occ)} from '
                      f'{self.energies_occ[0]:.1f} to {self.energies_occ[-1]:.1f} eV',
                      f'  Unoccupied: {len(self.energies_unocc)} from '
                      f'{self.energies_unocc[0]:.1f} to {self.energies_unocc[-1]:.1f} eV',
                      ''
                      ]

        return '\n'.join(lines)

    @property
    def density_matrices(self) -> BaseDensityMatrices:
        """ Object that gives the density matrix in the time or freqency domain. """
        return self._density_matrices

    @property
    def nproj(self) -> int:
        """ Number of projections in the Voronoi weights object """
        if self.voronoi is None:
            return 0
        else:
            return self.voronoi.nproj

    @property
    def voronoi(self) -> VoronoiWeights | None:
        """ Voronoi weights object """
        return self._voronoi

    @property
    def energies_occ(self) -> NDArray[np.float64]:
        """ Energy grid (in eV) for occupied levels (hot holes). """
        return self._energies_occ

    @property
    def energies_unocc(self) -> NDArray[np.float64]:
        """ Energy grid (in eV) for unoccupied levels (hot electrons). """
        return self._energies_unocc

    @property
    def sigma(self) -> float | None:
        """ Gaussian broadening width in eV. """
        return self._sigma

    @property
    def ksd(self) -> KohnShamDecomposition:
        """ Kohn-Sham decomposition object """
        return self.density_matrices.ksd

    @property
    def log(self) -> Logger:
        """ Logger """
        return self.density_matrices.log

    @property
    def frequencies(self) -> NDArray[np.float64]:
        """ Frequencies (in eV) at which the density matrices are evaluated.

        Only valid when the density matrices object is defined in the frequency domain. """
        assert isinstance(self.density_matrices, FrequencyDensityMatrices)
        return self.density_matrices.frequencies

    @property
    def times(self) -> NDArray[np.float64]:
        """ Times (in as) at which the density matrices are evaluated.

        Only valid when the density matrices object is defined in the time domain. """
        assert isinstance(self.density_matrices, (TimeDensityMatrices, ConvolutionDensityMatrices))
        return self.density_matrices.times

    @property
    def pulses(self) -> list[GaussianPulse]:
        """ List of pulses which the density matrices are responses to.

        Only valid when the density matrices object is a convolution with pulses. """
        assert isinstance(self.density_matrices, ConvolutionDensityMatrices)
        return self.density_matrices.pulses

    @property
    def calc_comm(self) -> Communicator:
        """ Calculation communicator.

        Each rank of this communicator calculates the observables corresponding to
        a part (in electron-hole space) of the density matrices. """
        return self.density_matrices.calc_comm

    @property
    def loop_comm(self) -> Communicator:
        """ Loop communicator.

        Each rank of this communicator calculates the density matrices corresponding to
        different times, frequencies or after convolution with a different pulse. """
        return self.density_matrices.loop_comm

    @property
    def eig_n(self) -> NDArray[np.float64]:
        """ Eigenvalues (in eV) relative to Fermi level in the full ground state KS basis. """
        eig_n, _ = self.ksd.get_eig_n(zero_fermilevel=True)
        return eig_n

    @property
    def eig_i(self) -> NDArray[np.float64]:
        """ Eigenvalues (in eV) relative to Fermi level of occupied states (holes). """
        return self.eig_n[self.flti]

    @property
    def eig_a(self) -> NDArray[np.float64]:
        """ Eigenvalues (in eV) relative to Fermi level of unoccupied states (electrons). """
        return self.eig_n[self.flta]

    @property
    def flti(self) -> slice:
        """ Slice for extracting indices corresponding to occupied states. """
        imin, imax, _, _ = self.ksd.ialims()
        return slice(imin, imax+1)

    @property
    def flta(self) -> slice:
        """ Slice for extracting indices corresponding to unoccupied states. """
        _, _, amin, amax = self.ksd.ialims()
        return slice(amin, amax+1)

    def _read_weights_diagonal(self) -> None:
        """ Read the diagonal weights from the voronoi object and store them in memory. """
        if self.voronoi is None:
            return
        nI = self.voronoi.nproj
        Nn = self.voronoi.nn

        weights_MiB = nI*Nn*8/1024**2
        if self.voronoi.comm.rank == 0:
            self.voronoi.log(f'Will use {weights_MiB:.1f}MiB per rank (total '
                             f'{weights_MiB*self.loop_comm.size*1e-3:.1f} GiB on {self.loop_comm.size} ranks)',
                             flush=True)

        if self.calc_comm.rank == 0:
            weight_In = np.empty((nI, Nn), dtype=float)
        else:
            weight_In = None
        for iI, weight_nn in enumerate(self.voronoi):
            if self.voronoi.comm.rank == 0:
                assert weight_In is not None
                assert weight_nn is not None
                weight_In[iI, ...] = weight_nn.diagonal()
            else:
                assert weight_nn is None

        if self.calc_comm.rank == 0:
            # Broadcast to all calc_comm rank 0's
            self.loop_comm.broadcast(weight_In, 0)

        self._weight_In = weight_In

    def _read_weights_eh(self) -> None:
        """ Read the electron-hole weights from the voronoi object and store them in memory. """
        if self.voronoi is None:
            return

        nI = self.voronoi.nproj
        Nn = self.voronoi.nn

        weights_MiB = nI*Nn*8/1024**2
        if self.voronoi.comm.rank == 0:
            self.voronoi.log(f'Will use {weights_MiB:.1f}MiB per rank (total '
                             f'{weights_MiB*self.loop_comm.size*1e-3:.1f}GiB on {self.loop_comm.size} ranks)',
                             flush=True)

        if self.calc_comm.rank == 0:
            weight_Iii = np.empty((nI, len(self.eig_i), len(self.eig_i)), dtype=float)
            weight_Iaa = np.empty((nI, len(self.eig_a), len(self.eig_a)), dtype=float)
        else:
            weight_Iii = None
            weight_Iaa = None
        for iI, weight_nn in enumerate(self.voronoi):
            if self.voronoi.comm.rank == 0:
                assert weight_nn is not None
                assert weight_Iii is not None
                assert weight_Iaa is not None
                weight_Iii[iI, ...] = weight_nn[self.flti, self.flti]
                weight_Iaa[iI, ...] = weight_nn[self.flta, self.flta]
            else:
                assert weight_nn is None

        if self.calc_comm.rank == 0:
            # Broadcast to all calc_comm rank 0's
            self.loop_comm.broadcast(weight_Iii, 0)
            self.loop_comm.broadcast(weight_Iaa, 0)

        self._weight_Iii = weight_Iii
        self._weight_Iaa = weight_Iaa

    @property
    def _iterate_weights_diagonal(self) -> Generator[NDArray[np.float64], None, None]:
        """ Iterate over the diagonal weights.

        Yields
        ------
        The diagonal of the Voronoi weights, one projection at a time """
        assert self.calc_comm.rank == 0
        if self.voronoi is None:
            return

        if self._weight_In is None:
            self._read_weights_diagonal()
        assert self._weight_In is not None

        for weight_n in self._weight_In:
            yield weight_n

    @property
    def _iterate_weights_eh(self) -> Generator[tuple[NDArray[np.float64], NDArray[np.float64]], None, None]:
        """ Iterate over the electron-hole part of the weights.

        Yields
        ------
        The electron-hole part of the Voronoi weights, one projection at a time """
        assert self.calc_comm.rank == 0
        if self.voronoi is None:
            return

        if self._weight_Iaa is None or self._weight_Iii is None:
            self._read_weights_eh()
        assert self._weight_Iii is not None
        assert self._weight_Iaa is not None

        for weight_ii, weight_aa in zip(self._weight_Iii, self._weight_Iaa):
            yield weight_ii, weight_aa

    @abstractmethod
    def get_result_keys(self) -> ResultKeys:
        """ Get the keys that each result will contain, and dimensions thereof.

        Returns
        -------
        Object representing the data that will be present in the result objects. """
        raise NotImplementedError

    @abstractmethod
    def icalculate(self) -> Generator[tuple[WorkMetadata, Result], None, None]:
        """ Iteratively calculate results.

        Yields
        ------
        Tuple (work, result) on the root rank of the calculation communicator:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the calculation communicator.
        """
        raise NotImplementedError

    def icalculate_gather_on_root(self, **kwargs) -> Generator[
            tuple[WorkMetadata, Result], None, None]:
        """ Iteratively calculate results and gather to the root rank.

        Yields
        ------
        Tuple (work, result) on the root rank of the both calculation and loop communicators:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the communicators.
        """
        resultkeys = self.get_result_keys(**kwargs)
        gen = iter(self.icalculate(**kwargs))

        # Loop over the work to be done, and the ranks that are supposed to do it
        for rank, work in self.density_matrices.global_work_loop_with_idle():
            if work is None:
                # Rank rank will not do any work at this point
                continue

            if self.calc_comm.rank > 0:
                continue

            if self.loop_comm.rank == 0 and rank == 0:
                # This is the root rank, and the root rank should yield its own work
                mywork, result = next(gen)
                assert work.global_indices == mywork.global_indices, f'{work.desc} != {mywork.desc}'
                yield mywork, result
                # self.log.start('communicate')
            elif self.loop_comm.rank == 0:
                # This is the root rank, and the root rank should receive the work
                # done by rank rank, and yield that
                result.inplace_receive(resultkeys, rank, comm=self.loop_comm)
                yield work, result
                # self.log(f'Communicated for {self.log.elapsed("communicate"):.2f}s', flush=True)
            elif self.loop_comm.rank == rank:
                # This is not the root rank, but this rank should send its data to root
                _, result = next(gen)
                result.send(resultkeys, 0, comm=self.loop_comm)

        _exhausted = object()
        rem = next(gen, _exhausted)
        assert rem is _exhausted, rem

    def broaden_occ(self,
                    M_i: NDArray[np.float64]) -> NDArray[np.float64]:
        """ Broaden array corresponding to occupied levels with Gaussians of width sigma

        Parameters
        ----------
        M_i
            Array to broaden

        Returns
        -------
        Broadened array
        """
        assert self.sigma is not None

        return broaden_n2e(M_i, self.eig_i, self.energies_occ, self.sigma)

    def broaden_unocc(self,
                      M_a: NDArray[np.float64]) -> NDArray[np.float64]:
        """ Broaden array corresponding to unoccupied levels with Gaussians of width sigma

        Parameters
        ----------
        M_a
            Array to broaden

        Returns
        -------
            Broadened array
        """
        assert self.sigma is not None

        return broaden_n2e(M_a, self.eig_a, self.energies_unocc, self.sigma)

    def broaden_xi2o(self,
                     M_xi: NDArray[np.float64]) -> NDArray[np.float64]:
        """ Broaden array corresponding to occupied levels with Gaussians of width sigma

        Parameters
        ----------
        M_xa
            Array to broaden. The last dimension should correspond to the occupied levels

        Returns
        -------
        Broadened array
        """
        assert self.sigma is not None

        return broaden_xn2e(M_xi, self.eig_i, self.energies_occ, self.sigma)

    def broaden_xi2u(self,
                     M_xa: NDArray[np.float64]) -> NDArray[np.float64]:
        """ Broaden array corresponding to unoccupied levels with Gaussians of width sigma

        Parameters
        ----------
        M_xa
            Array to broaden. The last dimension should correspond to the unoccupied levels

        Returns
        -------
            Broadened array
        """
        assert self.sigma is not None

        return broaden_xn2e(M_xa, self.eig_a, self.energies_unocc, self.sigma)

    def broaden_ia2ou(self,
                      M_ia: NDArray[np.float64]) -> NDArray[np.float64]:
        """ Broaden matrix in electron-hole basis with Gaussians of width sigma.

        Parameters
        ----------
        M_ia
            Matrix to broaden. The first dimension should correspond to occupied levels
            and the second to unoccupied levels.

        Returns
        -------
            Broadened array
        """
        assert self.sigma is not None

        return broaden_ia2ou(M_ia, self.eig_i, self.eig_a,
                             self.energies_occ, self.energies_unocc, self.sigma)
