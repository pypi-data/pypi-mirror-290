from __future__ import annotations

import numpy as np
from typing import Generator

from .base import BaseObservableCalculator
from ..density_matrices.base import WorkMetadata
from ..utils import ResultKeys, Result


class DipoleCalculator(BaseObservableCalculator):

    r""" Obtain contributions to induced dipole moment from density matrices

    The induced dipole moment (i.e. the dipole moment minus the permanent
    component) is to first order given by

    .. math::

        \delta\boldsymbol{\mu} = -2 \sum_{ia}^\text{eh}
        \boldsymbol{\mu}_{ia} \mathrm{Re}\:\delta\rho_{ia},

    where :math:`\boldsymbol{\mu}_{ia}` is the dipole matrix element of ground state Kohn-Sham
    pair :math:`ia`

    .. math::

        \boldsymbol{\mu}_{ia} = \int \psi^{(0)}_i(\boldsymbol{r}) \boldsymbol{r}
        \psi^{(0)}_a(\boldsymbol{r}) \mathrm{d}\boldsymbol{r}.

    This class can also compute projections of the above on Voronoi weights :math:`w_{ia}`.

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
                        yield_total_ia: bool = False,
                        yield_proj_ia: bool = False,
                        yield_total_ou: bool = False,
                        yield_proj_ou: bool = False,
                        decompose_v: bool = True,
                        v: int | None = None,
                        ) -> ResultKeys:
        r""" Get the keys that each result will contain, and dimensions thereof.

        Parameters
        ----------
        yield_total_ia
            The results should include the total dipole contributions in the electron-hole basis
            :math:`-2 \boldsymbol{\mu}_{ia} \mathrm{Re}\:\delta\rho_{ia}`.
        yield_proj_ia
            The results should include projections of the dipole contributions in the electron-hole basis
            :math:`-2 \boldsymbol{\mu}_{ia} \mathrm{Re}\:\delta\rho_{ia} w_{ia}`.
        yield_total_ou
            The results should include the total dipole contributions on the energy grid
        yield_proj_ou
            The results should include projections of the dipole contributions on the energy grid
        decompose_v
            The results should include the dipole moment and/or its contributions decomposed
            by Cartesian direction.
        v
            If not None, then the results should include the v:th Cartesian component
            of the dipole moment and its contributions.
        """
        assert decompose_v or v is not None

        nI = self.nproj
        imin, imax, amin, amax = self.ksd.ialims()
        ni = imax - imin + 1
        na = amax - amin + 1
        no = len(self.energies_occ)
        nu = len(self.energies_unocc)

        resultkeys = ResultKeys()
        if v is not None:
            resultkeys.add_key('dm')
            if yield_total_ia:
                resultkeys.add_key('dm_ia', (ni, na))
            if yield_total_ou:
                resultkeys.add_key('dm_ou', (no, nu))

            resultkeys.add_key('dm_proj_II', (nI, nI))
            if yield_proj_ia:
                resultkeys.add_key('dm_occ_proj_Iia', (nI, ni, na))
                resultkeys.add_key('dm_unocc_proj_Iia', (nI, ni, na))
            if yield_proj_ou:
                resultkeys.add_key('dm_occ_proj_Iou', (nI, no, nu))
                resultkeys.add_key('dm_unocc_proj_Iou', (nI, no, nu))
        if decompose_v:
            resultkeys.add_key('dm_v', 3)
            if yield_total_ia:
                resultkeys.add_key('dm_iav', (ni, na, 3))
            if yield_total_ou:
                resultkeys.add_key('dm_ouv', (no, nu, 3))

            resultkeys.add_key('dm_proj_IIv', (nI, nI, 3))
            if yield_proj_ia:
                resultkeys.add_key('dm_occ_proj_Iiav', (nI, ni, na, 3))
                resultkeys.add_key('dm_unocc_proj_Iiav', (nI, ni, na, 3))
            if yield_proj_ou:
                resultkeys.add_key('dm_occ_proj_Iouv', (nI, no, nu, 3))
                resultkeys.add_key('dm_unocc_proj_Iouv', (nI, no, nu, 3))

        return resultkeys

    def icalculate(self,
                   yield_total_ia: bool = False,
                   yield_proj_ia: bool = False,
                   yield_total_ou: bool = False,
                   yield_proj_ou: bool = False,
                   decompose_v: bool = True,
                   v: int | None = None,
                   ) -> Generator[tuple[WorkMetadata, Result], None, None]:
        r""" Iteratively calculate dipole contributions.

        Parameters
        ----------
        yield_total_ia
            The results should include the total dipole contributions in the electron-hole basis
            :math:`-2 \boldsymbol{\mu}_{ia} \mathrm{Re}\:\delta\rho_{ia}`.
        yield_proj_ia
            The results should include projections of the dipole contributions in the electron-hole basis
            :math:`-2 \boldsymbol{\mu}_{ia} \mathrm{Re}\:\delta\rho_{ia} w_{ia}`.
        yield_total_ou
            The results should include the total dipole contributions on the energy grid
        yield_proj_ou
            The results should include projections of the dipole contributions on the energy grid
        decompose_v
            The results should include the dipole moment and/or its contributions decomposed
            by Cartesian direction.
        v
            If not None, then the results should include the v:th Cartesian component
            of the dipole moment and its contributions.

        Yields
        ------
        Tuple (work, result) on the root rank of the calculation communicator:

        work
            An object representing the metadata (time, frequency or pulse) for the work done
        result
            Object containg the calculation results for this time, frequency or pulse

        Yields nothing on non-root ranks of the calculation communicator.
        """
        from gpaw.tddft.units import au_to_eA

        include_energy_dists = (yield_total_ou or yield_proj_ou)
        if include_energy_dists:
            assert self.sigma is not None
        need_entire_matrix = (yield_total_ou or yield_proj_ou
                              or yield_total_ia or yield_proj_ia
                              or self.nproj > 0)

        assert all([order in self.density_matrices.derivative_order_s for order in [0]])

        dm0_vp = 2 * self.ksd.dm_vp * au_to_eA

        # List all keys that this method computes
        # This is necessary to safely send and receive data across ranks
        resultkeys = self.get_result_keys(yield_total_ia=yield_total_ia,
                                          yield_proj_ia=yield_proj_ia,
                                          yield_total_ou=yield_total_ou,
                                          yield_proj_ou=yield_proj_ou,
                                          decompose_v=decompose_v,
                                          v=v,
                                          )

        self._read_weights_diagonal()

        # Iterate over the pulses and times
        for work, dm in self.density_matrices:
            dm.rho_p  # Read these now, so non calc_comm root ranks can continue

            if dm.rank > 0:
                continue

            self.log.start('calculate')

            if need_entire_matrix:
                dm_pv = - (dm0_vp * dm.rho_p.real).T
                dm_v = np.sum(dm_pv, axis=0)

                dm_iav = dm.M_ia_from_M_p(dm_pv)
                if yield_total_ou:
                    dm_ouv = self.broaden_ia2ou(dm_iav)
            else:
                dm_v = - dm0_vp @ dm.rho_p.real

            result = Result()
            if decompose_v:
                result['dm_v'] = dm_v
                if yield_total_ia:
                    result['dm_iav'] = dm_iav
                if yield_total_ou:
                    result['dm_ouv'] = dm_ouv
            if v is not None:
                result['dm'] = dm_v[v]
                if yield_total_ia:
                    result['dm_ia'] = dm_iav[..., v]
                if yield_total_ou:
                    result['dm_ou'] = dm_ouv[..., v]

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

                    dm_proj_v = np.einsum('iav,i,a->v', dm_iav, weight_i, weight2_a, optimize=True)
                    result['dm_proj_IIv'][iI, iI2] = dm_proj_v

                if yield_proj_ia or yield_proj_ou:
                    dm_occ_proj_iav = dm_iav * weight_i[:, None, None]
                    dm_unocc_proj_iav = dm_iav * weight_a[None, :, None]

                    if yield_proj_ou:
                        dm_occ_proj_ouv = self.broaden_ia2ou(dm_occ_proj_iav)
                        dm_unocc_proj_ouv = self.broaden_ia2ou(dm_unocc_proj_iav)

                    if decompose_v:
                        if yield_proj_ia:
                            result['dm_occ_proj_Iiav'][iI] = dm_occ_proj_iav
                            result['dm_unocc_proj_Iiav'][iI] = dm_unocc_proj_iav
                        if yield_proj_ou:
                            result['dm_occ_proj_Iouv'][iI] = dm_occ_proj_ouv
                            result['dm_unocc_proj_Iouv'][iI] = dm_unocc_proj_ouv
                    if v is not None:
                        if yield_proj_ia:
                            result['dm_occ_proj_Iia'][iI] = dm_occ_proj_iav[..., v]
                            result['dm_unocc_proj_Iia'][iI] = dm_unocc_proj_iav[..., v]
                        if yield_proj_ou:
                            dm_occ_proj_ouv = self.broaden_ia2ou(dm_occ_proj_iav)
                            dm_unocc_proj_ouv = self.broaden_ia2ou(dm_unocc_proj_iav)

                        if decompose_v:
                            if yield_proj_ia:
                                result['dm_occ_proj_Iiav'][iI] = dm_occ_proj_iav
                                result['dm_unocc_proj_Iiav'][iI] = dm_unocc_proj_iav
                            if yield_proj_ou:
                                result['dm_occ_proj_Iouv'][iI] = dm_occ_proj_ouv
                                result['dm_unocc_proj_Iouv'][iI] = dm_unocc_proj_ouv
                        if v is not None:
                            if yield_proj_ia:
                                result['dm_occ_proj_Iia'][iI] = dm_occ_proj_iav[..., v]
                                result['dm_unocc_proj_Iia'][iI] = dm_unocc_proj_iav[..., v]
                            if yield_proj_ou:
                                result['dm_occ_proj_Iou'][iI] = dm_occ_proj_ouv[..., v]
                                result['dm_unocc_proj_Iou'][iI] = dm_unocc_proj_ouv[..., v]

            self.log(f'Calculated and broadened dipoles contributions in {self.log.elapsed("calculate"):.2f}s '
                     f'for {work.desc}', flush=True)

            yield work, result

        if self.calc_comm.rank == 0:
            self.log('Finished calculating dipoles contributions', flush=True)
