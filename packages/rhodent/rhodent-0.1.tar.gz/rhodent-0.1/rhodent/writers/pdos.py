from __future__ import annotations

import sys
import numpy as np
from numpy.typing import NDArray
from typing import Any
from gpaw.mpi import world

from ..cli.voronoi import atom_projections_to_numpy
from ..voronoi import VoronoiWeights
from ..pdos import PDOSCalculator


def calculate_and_save_by_filename(out_fname: str,
                                   **kwargs):
    """ Read eigenvalues and wave functions from ground state and calculate broadened PDOS

    The PDOS is projected on each group of atoms in atom_projections

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    voronoi
        Voronoi weights calculator/reader
    energies
        Array of energies (in eV) for which the broadened DOS is computed
    sigma
        Gaussian broadening width in eV
    gpw_file
        Filename of GPAW ground state file
    zerofermi
        Eigenvalues relative to Fermi level if true, else relative to vacuum
    """
    if out_fname[-4:] == '.npz':
        calculate_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.dat':
        calculate_and_save_dat(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .dat, is {out_fname}')
        sys.exit(1)


def calculate_and_save_dat(out_fname: str,
                           voronoi: VoronoiWeights,
                           energies: list[float] | NDArray[np.float64],
                           sigma: float,
                           gpw_file: str,
                           zerofermi: bool = False):
    """ Read eigenvalues and wave functions from ground state and calculate broadened PDOS

    The PDOS is projected on each group of atoms in atom_projections

    Save the broadened PDOS in a text file

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    voronoi
        Voronoi weights calculator/reader
    energies
        Array of energies (in eV) for which the broadened DOS is computed
    sigma
        Gaussian broadening width in eV
    gpw_file
        Filename of GPAW ground state file
    zerofermi
        Eigenvalues relative to Fermi level if true, else relative to vacuum
    """
    if zerofermi:
        zerostr = 'relative to Fermi level'
    else:
        zerostr = 'relative to vacuum level'

    Ni = len(voronoi)

    calc = PDOSCalculator(voronoi, energies=energies, sigma=sigma,
                          zerofermi=zerofermi, gpw_file=gpw_file)

    if world.rank == 0:
        # Construct energy grid
        savedata = np.zeros((len(energies), Ni + 1))
        savedata[:, 0] = energies
        pdos_ei = savedata[:, 1:]

    for i, ret in enumerate(calc.icalculate()):
        if world.rank != 0:
            continue
        pdos_ei[:, i] = ret['pdos_e']

    if world.rank != 0:
        return

    projectionsstr = '\n'.join([f'  {i:4.0f}: {str(proj)}'
                                for i, proj in enumerate(voronoi.atom_projections)])
    projcolumns = '   '.join([f'PDOS {i:4.0f} (1/eV)' for i in range(Ni)])

    header = (f'PDOS {zerostr}\n'
              'Atomic projections:\n'
              f'{projectionsstr}\n'
              f'Gaussian folding, Width {sigma:.4f}eV\n'
              f'Energy (eV)   {projcolumns}')
    fmt = ['%13.6f'] + Ni*['%18.8e']
    np.savetxt(out_fname, savedata, fmt, header=header)


def calculate_and_save_npz(out_fname: str,
                           voronoi: VoronoiWeights,
                           energies: list[float] | NDArray[np.float64],
                           sigma: float,
                           gpw_file: str,
                           zerofermi: bool = False,
                           write_extra: dict[str, Any] = dict(),
                           write_extra_from_voronoi: bool = False):
    """ Read eigenvalues and wave functions from ground state and calculate broadened PDOS

    The PDOS is projected on each group of atoms in atom_projections

    Save the broadened PDOS in a compressed numpy .npz archive

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    voronoi
        Voronoi weights calculator/reader
    energies
        Array of energies (in eV) for which the broadened DOS is computed
    sigma
        Gaussian broadening width in eV
    gpw_file
        Filename of GPAW ground state file
    zerofermi
        Eigenvalues relative to Fermi level if true, else relative to vacuum
    write_extra
        Dictionary of extra key-value pairs to write to the .npz file
    write_extra_from_voronoi
        If true, and voronoi is a ULM reader, extra key-value pairs are read from
        voronoi and written to the .npz file
    """
    ni = len(voronoi)

    write: dict[str, Any] = dict()
    if world.rank == 0:
        write['energy_e'] = energies
        write['atom_projections'] = atom_projections_to_numpy(voronoi.atom_projections)
        pdos_ei = write['pdos_ei'] = np.zeros((len(energies), ni))
        write.update(voronoi.saved_fields)
        write.update(write_extra)

    calc = PDOSCalculator(voronoi, energies=energies, sigma=sigma,
                          zerofermi=zerofermi, gpw_file=gpw_file)

    for i, ret in enumerate(calc.icalculate()):
        if world.rank != 0:
            continue
        pdos_ei[:, i] = ret['pdos_e']

    if world.rank != 0:
        return

    write.update(sigma=sigma, zerofermi=zerofermi)

    np.savez(out_fname, **write)
    print(f'Written {out_fname}', flush=True)
