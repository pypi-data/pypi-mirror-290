from __future__ import annotations

from typing import Generator

import numpy as np
from numpy.typing import NDArray

from gpaw import GPAW
from gpaw.mpi import world, SerialCommunicator

from .utils import gauss_ij, Logger
from .voronoi import VoronoiWeights
from .typing import GPAWCalculator


class PDOSCalculator:

    """ PDOS calculator

    Parameters
    ----------
    voronoi
        Voronoi weights object
    energies
        Array of energies (in eV) for which the broadened PDOS is computed
    sigma
        Gaussian broadening width in eV
    gpw_file
        Filename of GPAW ground state file
    zerofermi
        Eigenvalues relative to Fermi level if ``True``, else relative to vacuum
    """

    def __init__(self,
                 voronoi: VoronoiWeights,
                 energies: list[float] | NDArray[np.float64],
                 sigma: float,
                 gpw_file: str | None = None,
                 zerofermi: bool = False):
        self._voronoi = voronoi
        self._energies = np.array(energies)
        self._sigma = sigma
        self._zerofermi = zerofermi
        self._gpw_file = gpw_file
        try:
            self._calc = voronoi.voronoi_lcao_gen.calc  # type: ignore
        except AttributeError:
            # Reading weights from file (either in LCAO basis or KS basis).
            # No GPAW calculator present
            self._calc = None
            assert gpw_file is not None

    @property
    def calc(self) -> GPAWCalculator:
        """ GPAW Calculator object """
        if self._calc is None:
            calc = GPAW(self._gpw_file, communicator=SerialCommunicator(), txt='/dev/null')
            self._calc = calc
        return self._calc

    @property
    def voronoi(self) -> VoronoiWeights:
        """ Voronoi weights object """
        return self._voronoi

    @property
    def log(self) -> Logger:
        """ Logger """
        return self.voronoi.log

    @property
    def zero(self) -> float:
        if self._zerofermi:
            return self.calc.get_fermi_level()
        else:
            return 0

    @property
    def eig_n(self) -> NDArray[np.float64]:
        return self.calc.get_eigenvalues() - self.zero

    @property
    def energies(self) -> NDArray[np.float64]:
        """ Energy grid in eV """
        return self._energies

    @property
    def sigma(self) -> float:
        """ Gaussian broadening width in eV. """
        return self._sigma

    def icalculate(self) -> Generator[dict[str, NDArray[np.float64] | None], None, None]:
        r"""Read eigenvalues and wave functions from ground state and calculate broadened PDOS.

        The PDOS is projected on each group of atoms in :attr:`atom_projections`.
        Calculates Voronoi weights from ground state file
        using LCAO basis function overlaps and PAW corrections,

        .. math::

            W_{nn'}
            = \left<\psi_n|\hat{w}|\psi_{n'}\right>
            = \int w(\vec{r}) \psi_n^*(\vec{r}) \psi_{n'}(\vec{r}) d\vec{r}

        where the operator :math:`\hat{w} = w(\vec{r})` is 1 in the Voronoi
        region of the atomic projections and 0 outside.

        Parameters
        ----------
        voronoi
            Voronoi weights calculator/reader
        sigma
            Gaussian broadening width in eV

        Yields
        -------
            Once per atom group in :attr:`atom_projections` a dictionary with keys
                * ``weight_n`` - Array of dimensions ``(Nn)`` of projections. ``None`` on non-root ranks.
                * ``pdos_e`` - Broadened PDOS. ``None`` on non-root ranks.
        """
        if world.rank == 0:
            # Construct gaussians
            gauss_en = gauss_ij(self.energies, self.eig_n, self.sigma)
            self.log('Computed gaussians', flush=True)

        for i, weight_nn in enumerate(self.voronoi):
            if world.rank == 0:
                assert weight_nn is not None
                weight_n = weight_nn.diagonal()
                pdos_e = gauss_en @ weight_n
                self.log(f'Computed PDOS for projection {self.voronoi.atom_projections[i]}', flush=True)
                yield dict(weight_n=weight_n, pdos_e=pdos_e)
            else:
                yield dict(weight_n=None, pdos_e=None)
