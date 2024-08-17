from __future__ import annotations

import sys
import numpy as np
from typing import Any
from gpaw.io import Writer
from gpaw.mpi import world

from ..cli.voronoi import atom_projections_to_numpy
from ..utils import proj_as_dict_on_master
from ..voronoi import VoronoiWeights, VoronoiLCAOWeightCalculator


def calculate_and_save_by_filename(out_fname: str,
                                   **kwargs):
    """ Save Voronoi weights to file

    The file format of the resulting file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi
        Voronoi weights object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    if out_fname[-4:] == '.npz':
        calculate_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.ulm':
        calculate_and_save_ulm(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .ulm, is {out_fname}')
        sys.exit(1)


def calculate_and_save_LCAO_only_by_filename(out_fname: str,
                                             **kwargs):
    """ Save Voronoi weights in LCAO basis to file

    The file format of the resulting file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi_lcao
        Voronoi weights in LCAO basis object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    if out_fname[-4:] == '.npz':
        calculate_and_save_npz_LCAO_only(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.ulm':
        calculate_and_save_ulm_LCAO_only(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .ulm, is {out_fname}')
        sys.exit(1)


def calculate_and_save_ulm(out_fname: str,
                           voronoi: VoronoiWeights,
                           write_extra: dict[str, Any] = dict()):
    """ Save Voronoi weights to ULM file

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi
        Voronoi weights object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    ni = voronoi.nproj
    nn = voronoi.nn

    write = dict()
    if world.rank == 0:
        write.update(voronoi.saved_fields)
        write.update(write_extra)

    with Writer(out_fname, world, mode='w', tag='Voronoi') as writer:
        writer.write(version=1)
        writer.write('atom_projections', voronoi.atom_projections)
        for key, value in write.items():
            writer.write(key, value)

        if world.rank == 0:
            writer.add_array('weight_inn', (ni, nn, nn), dtype=voronoi.dtype)

        for weight_nn in voronoi:
            if world.rank != 0:
                continue

            writer.fill(weight_nn)
    if world.rank == 0:
        print(f'Written {out_fname}', flush=True)


def calculate_and_save_ulm_LCAO_only(out_fname: str,
                                     voronoi_lcao: VoronoiLCAOWeightCalculator,
                                     write_extra: dict[str, Any] = dict()):
    """ Save Voronoi weights in LCAO basis to ULM file

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi_lcao
        Voronoi weights in LCAO basis object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    ni = voronoi_lcao.nproj
    nM = voronoi_lcao.nM

    write = dict()
    if world.rank == 0:
        write.update(voronoi_lcao.saved_fields)
        write.update(write_extra)

    with Writer(out_fname, world, mode='w', tag='Voronoi-LCAO') as writer:
        writer.write(version=1)
        writer.write('atom_projections', voronoi_lcao.atom_projections)
        for key, value in write.items():
            writer.write(key, value)

        calc = voronoi_lcao.calc
        k, s = 0, 0
        Nn = calc.wfs.bd.nbands
        P_ani = proj_as_dict_on_master(calc.wfs.kpt_u[0].projections, 0, Nn)
        C_nM = calc.wfs.collect_array('C_nM', k, s)
        dS_aii = {a: setup.dO_ii for a, setup in enumerate(calc.wfs.setups)}  # Same data on all ranks

        if world.rank == 0:
            writer.write('C_nM', C_nM)
            writer.write('P_ani', P_ani)
            writer.write('dS_aii', dS_aii)

        if world.rank == 0:
            writer.add_array('weight_iMM', (ni, nM, nM), dtype=voronoi_lcao.dtype)

        for weight_MM in voronoi_lcao:
            voronoi_lcao.domain_comm.sum(weight_MM)

            if world.rank != 0:
                continue

            writer.fill(weight_MM)
    if world.rank == 0:
        print(f'Written {out_fname}', flush=True)


def calculate_and_save_npz(out_fname: str,
                           voronoi: VoronoiWeights,
                           write_extra: dict[str, Any] = dict()):
    """ Save Voronoi weights to numpy archive

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi
        Voronoi weights object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    ni = voronoi.nproj
    nn = voronoi.nn
    dtype = voronoi.dtype

    write = dict()
    if world.rank == 0:
        write.update(voronoi.saved_fields)
        write['atom_projections'] = atom_projections_to_numpy(voronoi.atom_projections)
        write.update(write_extra)
        weight_inn = np.zeros((ni, nn, nn), dtype=dtype)

    for i, weight_nn in enumerate(voronoi):
        if world.rank != 0:
            continue
        weight_inn[i, ...] = weight_nn

    if world.rank != 0:
        return

    np.savez(out_fname, weight_inn=weight_inn, **write)
    print(f'Written {out_fname}', flush=True)


def calculate_and_save_npz_LCAO_only(out_fname: str,
                                     voronoi_lcao: VoronoiLCAOWeightCalculator,
                                     write_extra: dict[str, Any] = dict()):
    """ Save Voronoi weights in LCAO basis to numpy archive

    Parameters
    ----------
    out_fname
        File name of the voronoi weigths file
    voronoi_lcao
        Voronoi weights in LCAO basis object
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    ni = voronoi_lcao.nproj
    nM = voronoi_lcao.nM
    dtype = voronoi_lcao.dtype

    write = dict()
    if world.rank == 0:
        write.update(voronoi_lcao.saved_fields)
        write['atom_projections'] = atom_projections_to_numpy(voronoi_lcao.atom_projections)
        write.update(write_extra)
        weight_iMM = np.zeros((ni, nM, nM), dtype=dtype)

    calc = voronoi_lcao.calc
    k, s = 0, 0
    Nn = calc.wfs.bd.nbands
    P_ani = proj_as_dict_on_master(calc.wfs.kpt_u[0].projections, 0, Nn)
    C_nM = calc.wfs.collect_array('C_nM', k, s)
    dS_aii = {a: setup.dO_ii for a, setup in enumerate(calc.wfs.setups)}  # Same data on all ranks

    write = dict()
    if world.rank == 0:
        write['C_nM'] = C_nM
        write['P_ani'] = P_ani
        write['dS_aii'] = dS_aii

    for i, weight_MM in enumerate(voronoi_lcao):
        voronoi_lcao.domain_comm.sum(weight_MM)
        if world.rank != 0:
            continue
        weight_iMM[i, ...] = weight_MM  # type: ignore

    if world.rank != 0:
        return

    np.savez(out_fname, **write, weight_iMM=weight_iMM, **write)
    print(f'Written {out_fname}', flush=True)
