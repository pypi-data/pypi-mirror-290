from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from ase.io.ulm import Reader

from ..utils import gauss_ij


def calculate_and_save_dat(out_fname: str,
                           gpw_file: str,
                           energies: list[float] | NDArray[np.float64],
                           sigma: float,
                           zerofermi: bool = False):
    """ Read eigenvalues from ground state and calculate broadened DOS

    Save the broadened DOS in a text file

    Parameters
    ----------
    out_fname
        Filename of data file where data is to be saved
    gpw_file
        Filename of GPAW ground state file
    energies
        Array of energies (in eV) for which the broadened DOS is computed
    sigma
        Gaussian broadening width in eV
    zerofermi
        True if energies are to be relative to Fermi level, False if relative to vacuum
    """
    # Construct energy grid
    energy_e = np.array(energies)

    # Read eigenenergies in eV
    reader = Reader(gpw_file)

    if zerofermi:
        zero = reader.wave_functions.fermi_levels
        zerostr = 'relative to Fermi level'
    else:
        zero = 0
        zerostr = 'relative to vacuum level'
    eig_skn = reader.wave_functions.eigenvalues - zero

    # Get only first spin channel, first k-point
    eig_n = eig_skn[0, 0]

    # Construct gaussians
    gauss_en = gauss_ij(energy_e, eig_n, sigma)

    # Construct DOS
    dos_e = np.sum(gauss_en, axis=1)

    header = (f'DOS {zerostr}\n'
              f'Gaussian folding, Width {sigma:.4f}eV\n'
              'Energy (eV)        DOS (1/eV)')
    np.savetxt(out_fname, np.array([energy_e, dos_e]).T, fmt=['%12.6f', '%18.8e'], header=header)
