from __future__ import annotations

from collections.abc import Sequence
import numpy as np
from typing import Generator

from .base import BaseObservableCalculator
from ..density_matrices.base import WorkMetadata
from ..density_matrices.time import ConvolutionDensityMatrixMetadata
from ..utils import ResultKeys, Result, broaden_n2e


class EnergyCalculator(BaseObservableCalculator):

    r""" Obtain energy contributions from pulse response density matrices.

    The total energy can be written

    .. math::

        E_\text{tot}(t) = E^{(0)}_\text{tot} + \sum_{ia}^\text{eh} E_{ia}(t) + E_\text{pulse}(t).

    The contributions to the total energy are

    .. math::

        E_{ia} = \frac{1}{2} \left[
        p_{ia}\dot{q}_{ia} - q_{ia} \dot{p}_{ia} - v_{ia} q_{ia} \right],

    the contributions to the Hartree energy are

    .. math::

        E_{ia}^\text{c} = -\frac{1}{2} \left[
        \omega_{ia} q_{ia}^2 - q_{ia} \dot{p}_{ia} - v_{ia} q_{ia} \right],

    and the rate of energy change is

    .. math::

        \dot{E}_{ia} = \frac{1}{2} \left[
        p_{ia}\ddot{q}_{ia} - q_{ia} \ddot{p}_{ia}
        - v_{ia} \dot{q}_{ia} - \dot{v}_{ia} q_{ia} \right],

    where

    .. math::

        v_{ia} = \sqrt{2 f_{ia}}  \int \psi^{(0)}_i(\boldsymbol{r})
        \left(\boldsymbol{r}\cdot\hat{\boldsymbol{e}}_\text{pulse}\right)
        \psi^{(0)}_a(\boldsymbol{r}) \mathrm{d}\boldsymbol{r}.


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
                        yield_total_E_ia: bool = False,
                        yield_proj_E_ia: bool = False,
                        yield_total_E_ou: bool = False,
                        yield_total_dists: bool = False,
                        direction: int | Sequence[int] = 2,
                        ) -> ResultKeys:
        r""" Get the keys that each result will contain, and dimensions thereof.

        Parameters
        ----------
        yield_total_E_ia
            The results should include the contributions in the electron-hole basis to
            the total energy :math:`E_{ia}` and Coulomb energy :math:`E_{ia}^\text{c}`
        yield_proj_E_ia
            The results should include the contributions in the electron-hole basis to
            the total energy projected on the occupied and unoccupied Voronoi weights
            :math:`E_{ia} w_i` and :math:`E_{ia} w_a`.
        yield_total_E_ou
            The results should include the contributions the total energy broadened on the
            occupied and unoccupied energy grids
            :math:`\sum_{ia} E_{ia}\delta(\varepsilon_\text{occ}-\varepsilon_{i})
            \delta(\varepsilon_\text{unocc}-\varepsilon_{a})` and
        yield_total_dists
            The results should include the contributions the total energy and Coulomb energy
            broadened by electronic transition energy onto the unoccupied energies grid
            :math:`\sum_{ia} E_{ia} \delta(\varepsilon-\omega_{ia})` and
            :math:`\sum_{ia} E_{ia}^\text{C} \delta(\varepsilon-\omega_{ia})`
        direction
            Direction :math:`\hat{\boldsymbol{e}}_\text{pulse}` of the polarization of the
            pulse. Integer 0, 1 or 2 to specify x, y or z, or the direction vector specified as
            a list of three values. Default: polarization along z.
        """
        nI = self.nproj
        imin, imax, amin, amax = self.ksd.ialims()
        ni = imax - imin + 1
        na = amax - amin + 1
        no = len(self.energies_occ)
        nu = len(self.energies_unocc)

        assert direction in [0, 1, 2] or (isinstance(direction, Sequence) and len(direction) == 3)

        resultkeys = ResultKeys('dm', 'total', 'total_coulomb', 'Epulse')

        if yield_total_E_ia:
            resultkeys.add_key('E_ia', (ni, na))
            resultkeys.add_key('Ec_ia', (ni, na))
        if yield_total_dists:
            resultkeys.add_key('E_transition_u', nu)
            resultkeys.add_key('Ec_transition_u', nu)
        if yield_total_E_ou:
            resultkeys.add_key('E_ou', (no, nu))
            resultkeys.add_key('Ec_ou', (no, nu))

        resultkeys.add_key('total_proj_II', (nI, nI))
        resultkeys.add_key('total_coulomb_proj_II', (nI, nI))
        if yield_proj_E_ia:
            resultkeys.add_key('E_occ_proj_Iia', (nI, ni, na))
            resultkeys.add_key('E_unocc_proj_Iia', (nI, ni, na))

        return resultkeys

    def icalculate(self,
                   yield_total_E_ia: bool = False,
                   yield_proj_E_ia: bool = False,
                   yield_total_E_ou: bool = False,
                   yield_total_dists: bool = False,
                   direction: int | Sequence[int] = 2,
                   ) -> Generator[tuple[WorkMetadata, Result], None, None]:
        r""" Iteratively calculate energies.

        Parameters
        ----------
        yield_total_E_ia
            The results should include the contributions in the electron-hole basis to
            the total energy :math:`E_{ia}` and Coulomb energy :math:`E_{ia}^\text{c}`
        yield_proj_E_ia
            The results should include the contributions in the electron-hole basis to
            the total energy projected on the occupied and unoccupied Voronoi weights
            :math:`E_{ia} w_i` and :math:`E_{ia} w_a`.
        yield_total_E_ou
            The results should include the contributions the total energy broadened on the
            occupied and unoccupied energy grids
            :math:`\sum_{ia} E_{ia}\delta(\varepsilon_\text{occ}-\varepsilon_{i})
            \delta(\varepsilon_\text{unocc}-\varepsilon_{a})` and
        yield_total_dists
            The results should include the contributions the total energy and Coulomb energy
            broadened by electronic transition energy onto the unoccupied energies grid
            :math:`\sum_{ia} E_{ia} \delta(\varepsilon-\omega_{ia})` and
            :math:`\sum_{ia} E_{ia}^\text{C} \delta(\varepsilon-\omega_{ia})`
        direction
            Direction :math:`\hat{\boldsymbol{e}}_\text{pulse}` of the polarization of the
            pulse. Integer 0, 1 or 2 to specify x, y or z, or the direction vector specified as
            a list of three values. Default: polarization along z.

        Yields
        ------
        Tuple (work, result) on the root rank of the calculation communicator:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the calculation communicator.
        """
        from gpaw.tddft.units import as_to_au, au_to_eV, au_to_eA

        include_energy_dists = (yield_total_dists or yield_total_E_ou)
        if include_energy_dists:
            assert self.sigma is not None

        assert all([order in self.density_matrices.derivative_order_s for order in [0, 1]])
        assert 'Re' in self.density_matrices.reim and 'Im' in self.density_matrices.reim

        assert direction in [0, 1, 2] or (isinstance(direction, Sequence) and len(direction) == 3)
        if direction in [0, 1, 2]:
            direction_v = np.zeros(3)
            direction_v[direction] = 1
        else:
            direction_v = np.array(direction)
            direction_v /= np.linalg.norm(direction_v)

        dm_p = direction_v @ self.ksd.dm_vp
        v0_p = dm_p * np.sqrt(2 * self.ksd.f_p)
        w_p = self.ksd.w_p

        # List all keys that this method computes
        # This is necessary to safely send and receive data across ranks
        resultkeys = self.get_result_keys(yield_total_dists=yield_total_dists,
                                          yield_total_E_ia=yield_total_E_ia,
                                          yield_proj_E_ia=yield_proj_E_ia,
                                          yield_total_E_ou=yield_total_E_ou,
                                          )

        self._read_weights_diagonal()

        # Iterate over the pulses and times
        for work, dm in self.density_matrices:
            dm.rho_p  # Read these now, so non calc_comm root ranks can continue
            dm.drho_p

            if dm.rank > 0:
                continue
            self.log.start('calculate')

            assert isinstance(work, ConvolutionDensityMatrixMetadata)
            pulsestr = work.pulse.strength(work.time * as_to_au)

            dipmom = - 2 * dm_p @ dm.rho_p.real
            Epulse = - dipmom * pulsestr * au_to_eV

            # Calculate v_ia
            v_p = v0_p * pulsestr

            E_p = -v_p * dm.Q_p
            E_p -= dm.Q_p * dm.dP_p

            Ec_p = E_p.copy()

            E_p += dm.P_p * dm.dQ_p
            E_p *= 0.5 * au_to_eV

            Ec_p -= w_p * dm.Q_p ** 2
            Ec_p *= 0.5 * au_to_eV

            if yield_total_E_ia or yield_total_E_ou:
                E_ia = self.ksd.M_ia_from_M_p(E_p)
                Ec_ia = self.ksd.M_ia_from_M_p(Ec_p)

            result = Result()
            if yield_total_E_ia:
                result['E_ia'] = E_ia
                result['Ec_ia'] = Ec_ia

            result['dm'] = dipmom * au_to_eA
            result['Epulse'] = Epulse
            result['total'] = np.sum(E_p)
            result['total_coulomb'] = np.sum(Ec_p)

            # (Optional) Broaden transitions by transition energy
            if yield_total_dists:
                assert self.sigma is not None
                result['E_transition_u'] = broaden_n2e(E_p, w_p * au_to_eV, self.energies_unocc, self.sigma)
                result['Ec_transition_u'] = broaden_n2e(Ec_p, w_p * au_to_eV, self.energies_unocc, self.sigma)

            # (Optional) Compute energy contribution matrix
            if yield_total_E_ou:
                result['E_ou'] = self.broaden_ia2ou(E_ia)
                result['Ec_ou'] = self.broaden_ia2ou(Ec_ia)

            # Initialize the remaining empty arrays
            result.create_all_empty(resultkeys)

            # Iterate over projections
            for iI, weight_n in enumerate(self._iterate_weights_diagonal):
                assert weight_n is not None
                weight_i = weight_n[self.flti]
                weight_a = weight_n[self.flta]

                for iI2, weight2_n in enumerate(self._iterate_weights_diagonal):
                    assert weight2_n is not None
                    weight2_a = weight2_n[self.flta]

                    result['total_proj_II'][iI, iI2] = np.einsum(
                        'ia,i,a->', E_ia, weight_i, weight2_a, optimize=True)
                    result['total_coulomb_proj_II'][iI, iI2] = np.einsum(
                        'ia,i,a->', Ec_ia, weight_i, weight2_a, optimize=True)

                if yield_proj_E_ia:
                    E_occ_proj_ia = E_ia * weight_i[:, None]
                    E_unocc_proj_ia = E_ia * weight_a[None, :]

                    result['E_occ_proj_Iia'][iI] = E_occ_proj_ia
                    result['E_unocc_proj_Iia'][iI] = E_unocc_proj_ia

            self.log(f'Calculated and broadened energies in {self.log.elapsed("calculate"):.2f}s '
                     f'for {work.desc}', flush=True)

            yield work, result

        if self.calc_comm.rank == 0:
            self.log('Finished calculating energies', flush=True)
