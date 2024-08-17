from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Generator

from .base import BaseObservableCalculator
from ..density_matrices.base import WorkMetadata
from ..utils import ResultKeys, Result


class HotCarriersCalculator(BaseObservableCalculator):

    r""" Obtain hot-carrier distributions, by calculating the second order response of the density matrix.

    For weak perturbations, the response of the density matrix is
    to first order non-zero only in the occupied-unoccupied space,
    i.e. the block off-diagonals

    .. math::

        \delta\rho = \begin{bmatrix}
            0         &  [\delta\rho_{ai}^*] \\
            [\delta\rho_{ia}] &  0
        \end{bmatrix}.

    The unoccupied-occupied, or electron-hole, part of the density matrix is thus
    linear in perturbation and can by transformed using Fourier transforms.

    From the first-order response, the second order response, i.e. the hole-hole
    (:math:`\delta\rho_{ii'}`) and electron-electron (:math:`\delta\rho_{aa}`) parts
    can be obtained.

    The hole-hole part is

    .. math::

        \delta\rho_{ii'} = - \frac{1}{2} \sum_n^{f_n > f_i, f_n > f_{i'}}
                           P_{ni} P_{ni'} + Q_{ni} Q_{ni'}

    and the electron-hole part

    .. math::

        \delta\rho_{aa'} = \frac{1}{2} \sum_n^{f_n < f_a, f_n < f_a'}
                           P_{ia} P_{ia'} + Q_{ia} Q_{ia'}

    where

    .. math::

        \begin{align}
            P_{ia} &= \frac{2 \mathrm{Im}\:\delta\rho_{ia}}{\sqrt{2 f_{ia}}} \\
            Q_{ia} &= \frac{2 \mathrm{Re}\:\delta\rho_{ia}}{\sqrt{2 f_{ia}}} ,
        \end{align}

    where :math:`f_{ia}` is the occupation number difference of pair :math:`ia`.

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

    def get_result_keys(self,
                        yield_total_hcdists: bool = False,
                        yield_proj_hcdists: bool = False,
                        yield_total_P: bool = False,
                        yield_proj_P: bool = False,
                        yield_total_P_ou: bool = False,
                        ):
        """ Get the keys that each result will contain, and dimensions thereof.

        Parameters
        ----------
        yield_total_hcdists
            The results should include the total hot-carrier distributions on the energy grid
        yield_proj_hcdists
            The results should include the projections of the hot-carrier distributions on the energy grid
        yield_total_P
            The results should include the total hot-carrier distributions in the electron-hole basis
        yield_proj_P
            The results should include the projections of the hot-carrier distributions in the electron-hole basis
        yield_total_P_ou
            The results should include the transition matrix broadened on the energy grid
        """
        nI = self.nproj
        imin, imax, amin, amax = self.ksd.ialims()
        ni = int(imax - imin + 1)
        na = int(amax - amin + 1)
        no = len(self.energies_occ)
        nu = len(self.energies_unocc)

        resultkeys = ResultKeys('sumocc', 'sumunocc')

        if yield_total_P:
            resultkeys.add_key('P_i', ni)
            resultkeys.add_key('P_a', na)
        if yield_total_hcdists:
            resultkeys.add_key('hcdist_o', no)
            resultkeys.add_key('hcdist_u', nu)

        if yield_total_P_ou:
            resultkeys.add_key('P_ou', (no, nu))

        resultkeys.add_key('sumocc_proj_I', nI)
        resultkeys.add_key('sumunocc_proj_I', nI)
        if yield_proj_P:
            resultkeys.add_key('P_proj_Ii', (nI, ni))
            resultkeys.add_key('P_proj_Ia', (nI, na))
        if yield_proj_hcdists:
            resultkeys.add_key('hcdist_proj_Io', (nI, no))
            resultkeys.add_key('hcdist_proj_Iu', (nI, nu))

        return resultkeys

    def icalculate(self,
                   yield_total_hcdists: bool = False,
                   yield_proj_hcdists: bool = False,
                   yield_total_P: bool = False,
                   yield_proj_P: bool = False,
                   yield_total_P_ou: bool = False,
                   ) -> Generator[tuple[WorkMetadata, Result], None, None]:
        r""" Iteratively calculate second order density matrices and hot-carrier distributions.

        Parameters
        ----------
        yield_total_hcdists
            The results should include the total hot-carrier distributions on the energy grid
        yield_proj_hcdists
            The results should include the projections of the hot-carrier distributions on the energy grid
        yield_total_P
            The results should include the total hot-carrier distributions in the electron-hole basis
        yield_proj_P
            The results should include the projections of the hot-carrier distributions in the electron-hole basis
        yield_total_P_ou
            The results should include the transition matrix broadened on the energy grid

        Yields
        ------
        Tuple (work, result) on the root rank of the calculation communicator:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the calculation communicator.
        """
        include_energy_dists = (yield_proj_hcdists or yield_total_hcdists)
        if include_energy_dists:
            assert self.sigma is not None

        assert all([order in self.density_matrices.derivative_order_s for order in [0]])
        assert 'Re' in self.density_matrices.reim and 'Im' in self.density_matrices.reim

        # List all keys that this method computes
        # This is necessary to safely send and receive data across ranks
        resultkeys = self.get_result_keys(yield_total_hcdists=yield_total_hcdists,
                                          yield_proj_hcdists=yield_proj_hcdists,
                                          yield_total_P=yield_total_P,
                                          yield_proj_P=yield_proj_P,
                                          yield_total_P_ou=yield_total_P_ou,
                                          )

        self._read_weights_eh()

        # Iterate over the pulses and times
        for work, dm in self.density_matrices:
            Q_ia = dm.Q_ia  # Read these now, so non calc_comm root ranks can continue
            P_ia = dm.P_ia

            if dm.rank > 0:
                continue

            # Holes
            M_ii = 0.5 * (Q_ia @ Q_ia.T + P_ia @ P_ia.T)

            # Electrons
            M_aa = 0.5 * (Q_ia.T @ Q_ia + P_ia.T @ P_ia)

            result = Result()

            # (Optional) Compute broadened transition matrix
            if yield_total_P_ou:
                transition_ia = 0.5 * (Q_ia**2 + P_ia**2)
                result['P_ou'] = self.broaden_ia2ou(transition_ia)

            # Compute quantities in all space
            P_i = calculate_hcdist(None, M_ii)
            P_a = calculate_hcdist(None, M_aa)
            result['sumocc'] = np.sum(P_i)
            result['sumunocc'] = np.sum(P_a)
            if yield_total_hcdists:
                result['hcdist_o'] = self.broaden_occ(P_i)
                result['hcdist_u'] = self.broaden_unocc(P_a)
            if yield_total_P:
                result['P_i'] = P_i
                result['P_a'] = P_a

            result.create_all_empty(resultkeys)

            # Iterate over projections
            for iI, (weight_ii, weight_aa) in enumerate(self._iterate_weights_eh):
                P_proj_i = calculate_hcdist(weight_ii, M_ii)
                P_proj_a = calculate_hcdist(weight_aa, M_aa)
                result['sumocc_proj_I'][iI] = np.sum(P_proj_i)
                result['sumunocc_proj_I'][iI] = np.sum(P_proj_a)
                if yield_proj_hcdists:
                    result['hcdist_proj_Io'][iI] = self.broaden_occ(P_proj_i)
                    result['hcdist_proj_Iu'][iI] = self.broaden_unocc(P_proj_a)
                if yield_proj_P:
                    result['P_proj_Ii'][iI] = P_proj_i
                    result['P_proj_Ia'][iI] = P_proj_a

            self.log(f'Calculated and broadened HC distributions in {self.log.elapsed("calculate"):.2f}s '
                     f'for {work.desc}', flush=True)

            yield work, result

        if self.calc_comm.rank == 0 and self.density_matrices.localn > 0:
            self.log('Finished calculating hot-carrier matrices', flush=True)


def calculate_hcdist(weight_xx: NDArray[np.float64] | None,
                     M_xx: NDArray[np.float64],
                     ) -> NDArray[np.float64]:
    r""" Calculate row-wise summed hot carrier distribution.

    .. math::

        \rho_n = \sum_{n'} \rho_{nn'} w_{nn'}

    Parameters
    ----------
    weight_xx
        Voronoi weights :math:`w_{ii}` or :math:`w_{aa}`.
        Specify None to let the weights be the identity matrix
    M_xx
        Matrix :math:`M_{ii}` or :math:`M_{aa}`

    Returns
    -------
        Hot carrier distribution by eigenvalue :math:`\rho_n`
    """
    if weight_xx is None:
        P_x = np.diag(M_xx)
    else:
        P_x = np.sum(weight_xx*M_xx, axis=0)

    return P_x
