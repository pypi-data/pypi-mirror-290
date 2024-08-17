from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Generator, Sequence

from ase.units import Bohr
from gpaw import GPAW
from gpaw.grid_descriptor import GridDescriptor
from gpaw.lcaotddft.densitymatrix import get_density

from .base import BaseObservableCalculator
from ..typing import GPAWCalculator
from ..density_matrices.base import BaseDensityMatrices, WorkMetadata
from ..voronoi import VoronoiWeights
from ..utils import ArrayIsOnRootRank, DistributedArray, ResultKeys, Result


class DensityCalculator(BaseObservableCalculator):

    r""" Obtain induced density from frequency or pulse response density matrices.

    The induced density (i.e. the density minus the ground state density) is to first
    order given by

    .. math::

        \delta n(\boldsymbol{r}) = -2 \sum_{ia}^\text{eh}
        n_{ia}(\boldsymbol{r}) \mathrm{Re}\:\delta\rho_{ia}

    plus PAW corrections, where :math:`n_{ia}(\boldsymbol{r})` is the density of
    ground state Kohn-Sham pair :math:`ia`

    .. math::

        n_{ia}(\boldsymbol{r}) = \psi^{(0)}_i(\boldsymbol{r}) \psi^{(0)}_a(\boldsymbol{r}).

    Parameters
    ----------
    gpw_file
        Filename of GPAW ground state file
    density_matrices
        Object that gives the density matrix in the time or freqency domain
    filter_occ
        Filters for occupied states (holes). Provide a list of tuples (low, high)
        to compute the density of holes with energies within the interval low-high.
    filter_unocc
        Filters for unoccupied states (electrons). Provide a list of tuples (low, high)
        to compute the density of excited electrons with energies within the interval low-high.
    """

    def __init__(self,
                 gpw_file: str,
                 density_matrices: BaseDensityMatrices,
                 filter_occ: Sequence[tuple[float, float]] = [],
                 filter_unocc: Sequence[tuple[float, float]] = []):
        self._density_matrices = density_matrices
        self._energies_occ = np.array([0])
        self._energies_unocc = np.array([0])
        self._sigma = 0
        self._occ_filters = [self._build_single_filter('o', low, high) for low, high in filter_occ]
        self._unocc_filters = [self._build_single_filter('u', low, high) for low, high in filter_unocc]

        self.log.start('load_gpaw')
        self._calc = GPAW(gpw_file, txt=None, communicator=self.calc_comm,
                          parallel={'domain': self.calc_comm.size})
        msg = f'Loaded and init GPAW in {self.log.elapsed("load_gpaw"):.1f}s'
        self.log.start('init_gpaw')

        self.calc.initialize_positions()  # Initialize in order to calculate density
        msg += f'+{self.log.elapsed("init_gpaw"):.1f}s'
        if self.calc_comm.rank == 0:
            self.log(msg)
        self.ksd.density = self.calc.density

    @property
    def gdshape(self) -> tuple[int, int, int]:
        """ Shape of the real space grid """
        shape = tuple(int(N) - 1 for N in self.N_c)
        return shape  # type: ignore

    @property
    def gd(self) -> GridDescriptor:
        """ Real space grid """
        return self.ksd.density.finegd

    @property
    def N_c(self) -> NDArray[np.int_]:
        """ Number of points in each Cartesian direction of the grid """
        return self.gd.N_c

    @property
    def cell_cv(self) -> NDArray[np.float64]:
        """ Cell vectors """
        return self.gd.cell_cv * Bohr

    @property
    def voronoi(self) -> VoronoiWeights:
        """ Voronoi weights object """
        raise NotImplementedError

    @property
    def occ_filters(self) -> list[slice]:
        """ List of energy filters for occupied states """
        return self._occ_filters

    @property
    def unocc_filters(self) -> list[slice]:
        """ List of energy filters for unoccupied states """
        return self._unocc_filters

    @property
    def calc(self) -> GPAWCalculator:
        """ GPAW calculator instance """
        return self._calc

    def get_result_keys(self) -> ResultKeys:
        noccf = len(self.occ_filters)
        nunoccf = len(self.unocc_filters)

        resultkeys = ResultKeys()
        resultkeys.add_key('rho_g', self.gdshape)
        resultkeys.add_key('occ_rho_g', self.gdshape)
        resultkeys.add_key('unocc_rho_g', self.gdshape)

        resultkeys.add_key('occ_rho_rows_fg', (noccf, ) + self.gdshape)
        resultkeys.add_key('unocc_rho_rows_fg', (nunoccf, ) + self.gdshape)

        resultkeys.add_key('occ_rho_diag_fg', (noccf, ) + self.gdshape)
        resultkeys.add_key('unocc_rho_diag_fg', (nunoccf, ) + self.gdshape)

        return resultkeys

    def _find_limit(self,
                    lim: float) -> int:
        """ Find the first eigenvalue larger than lim

        Parameters
        ----------
        lim
            Threshold value in eV

        Returns
        -------
        The index of the first eigenvalue larger than lim.
        Returns len(eig_n) if lim is larger than all eigenvalues
        """
        if lim > self.eig_n[-1]:
            return len(self.eig_n)
        return int(np.argmax(self.eig_n > lim))

    def _build_single_filter(self,
                             key: str,
                             low: float,
                             high: float) -> slice:
        imin, imax, amin, amax = self.ksd.ialims()

        if key == 'o':
            nlow = min(self._find_limit(low), imax) - imin
            nhigh = min(self._find_limit(high), imax) - imin
        elif key == 'u':
            nlow = min(self._find_limit(low), amax) - amin
            nhigh = min(self._find_limit(high), amax) - amin
        else:
            raise RuntimeError(f'Unknown key {key}. Key must be "o" or "u"')
        return slice(nlow, nhigh)

    def get_density(self,
                    rho_ia: DistributedArray,
                    n1: slice,
                    n2: slice,
                    fltn1: slice | NDArray[np.bool_] = slice(None),
                    fltn2: slice | NDArray[np.bool_] = slice(None),
                    u: int = 0) -> DistributedArray:
        """ Calculate a real space density from a density matrix in the Kohn-Sham basis.

        Returns
        -------
        Distributed array with the density in real space on the root rank
        """
        self.log.start('transform_dm')
        C0_nM = self.ksd.C0_unM[u]
        nM = C0_nM.shape[1]
        if self.calc_comm.rank == 0:
            assert np.issubdtype(rho_ia.dtype, float)

            # Filter
            rho_ia = rho_ia[fltn1][:, fltn2]
            C0_n1M = C0_nM[n1][fltn1]
            C0_n2M = C0_nM[n2][fltn2]

            # Sum for sanity check
            total = np.trace(rho_ia)

            # Transform to LCAO basis
            rho_MM = C0_n1M.T @ rho_ia @ C0_n2M.conj()
            rho_MM = 0.5 * (rho_MM + rho_MM.T)
        else:
            assert isinstance(rho_ia, ArrayIsOnRootRank)
            rho_MM = np.zeros((nM, nM), dtype=float)

        self.calc_comm.broadcast(rho_MM, 0)
        msg = f'Transformed DM and constructed density in {self.log.elapsed("transform_dm"):.1f}s'
        self.log.start('get_density')
        rho_g = get_density(rho_MM, self.calc.wfs, self.calc.density, u=u)
        msg += f'+{self.log.elapsed("get_density"):.1f}s'
        if self.calc_comm.rank == 0:
            self.log(msg)
        integ = self.gd.integrate(rho_g)
        if self.calc_comm.rank == 0:
            rerr = np.abs(integ - total) / total
            if False:
                self.log(f'Relative error: {rerr}')

        big_rho_g = self.gd.collect(rho_g)

        if self.calc_comm.rank == 0:
            return big_rho_g
        else:
            return ArrayIsOnRootRank()

    def icalculate(self) -> Generator[tuple[WorkMetadata, Result], None, None]:
        """ Iteratively calculate results. The results include the total induced density,
        and the densities of electrons and holes, optionally decomposed by `filter_occ`
        and `filter_unocc`.

        Yields
        ------
        Tuple (work, result) on the root rank of the calculation communicator:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the calculation communicator.
        """

        # Iterate over the pulses and times, or frequencies
        for work, dm in self.density_matrices:
            Q_ia = dm.Q_ia
            P_ia = dm.P_ia
            rho_ia = dm.rho_ia  # Read these now, so non calc_comm root ranks can continue

            # Holes
            M_ii = 0.5 * (Q_ia @ Q_ia.T + P_ia @ P_ia.T)

            # Electrons
            M_aa = 0.5 * (Q_ia.T @ Q_ia + P_ia.T @ P_ia)

            self.log.start('calculate')

            imin, imax, amin, amax = self.ksd.ialims()
            islice = slice(imin, imax + 1)
            aslice = slice(amin, amax + 1)

            rho_g = self.get_density(rho_ia.real, islice, aslice)

            occ_rho_g = self.get_density(M_ii, islice, islice)
            unocc_rho_g = self.get_density(M_aa, aslice, aslice)

            occ_rho_rows_fg = np.array([self.get_density(M_ii, islice, islice, fltn1=flt)
                                        for flt in self.occ_filters])
            occ_rho_diag_fg = np.array([self.get_density(M_ii, islice, islice, fltn1=flt, fltn2=flt)
                                        for flt in self.occ_filters])
            unocc_rho_rows_fg = np.array([self.get_density(M_aa, aslice, aslice, fltn1=flt)
                                         for flt in self.unocc_filters])
            unocc_rho_diag_fg = np.array([self.get_density(M_aa, aslice, aslice, fltn1=flt, fltn2=flt)
                                          for flt in self.unocc_filters])

            if dm.rank > 0:
                continue

            result = Result()
            result['rho_g'] = rho_g * Bohr ** -3

            result['occ_rho_g'] = occ_rho_g * Bohr ** -3
            result['unocc_rho_g'] = unocc_rho_g * Bohr ** -3

            result['occ_rho_rows_fg'] = occ_rho_rows_fg * Bohr ** -3
            result['occ_rho_diag_fg'] = occ_rho_diag_fg * Bohr ** -3
            result['unocc_rho_rows_fg'] = unocc_rho_rows_fg * Bohr ** -3
            result['unocc_rho_diag_fg'] = unocc_rho_diag_fg * Bohr ** -3

            self.log(f'Calculated density in {self.log.elapsed("calculate"):.2f}s '
                     f'for {work.desc}', flush=True)

            yield work, result

        if self.calc_comm.rank == 0:
            self.log('Finished calculating density contributions', flush=True)
