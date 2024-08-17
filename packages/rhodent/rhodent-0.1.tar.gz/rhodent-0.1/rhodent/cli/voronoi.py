from __future__ import annotations

from sys import exit
import numpy as np
from numpy.typing import NDArray

from ..voronoi import (AtomProjectionsType, VoronoiWeights, VoronoiLCAOWeights,
                       VoronoiReader, VoronoiWeightCalculator,
                       VoronoiLCAOReader, VoronoiLCAOWeightCalculator)


def add_projections_argument(parser,
                             required: bool = True):
    parser.add_argument('atoms', action='extend', nargs='+' if required else '*', type=str,
                        help='List of projections to consider. Give one or multiple projections '
                             'as space separated arguments. Each argument should be a '
                             'comma-separated list of atomic indices or ranges.\n\n'
                             'Example: 0,1,2,3 6 8 0:5 100:200:10')


def add_voronoi_weights_arguments(parser):
    ggroup = parser.add_argument_group(
        'Ground state options',
        'Calculate weights in Kohn-Sham or LCAO basis from ground state. '
        'The default is to compute basis in Kohn-Sham basis and save to OUTPUT_FILE')
    ggroup.add_argument('--calculate-grid', action='store_true',
                        help='Force recalculation of Voronoi grid. The Voronoi grid tells which '
                             'atom is closest to each grid point. This option '
                             'is implicit if GRID_FILE is not given')
    ggroup.add_argument('--grid-file', metavar='GRID_FILE',
                        help='Load the Voronoi grid from GRID_FILE. If --calculate-grid is given, '
                             'the grid is computed in the beginning of the calculation and saved '
                             'to this file instead.')
    ggroup.add_argument('-g', '--gpw-file', required=False,
                        help='Ground state file (including full KS-space).')
    ggroup.add_argument('-d', '--domain', type=int, default=-1,
                        help='Number of ranks participating in domain decomposition. -1 means all.')
    add_projections_argument(ggroup, required=False)
    lgroup = parser.add_argument_group(
        'Precomputed weights options',
        'Calculate weights in Kohn-Sham basis from weights in LCAO basis')
    lgroup.add_argument('-l', '--lcao-weights', required=False,
                        help='If given, the weights in LCAO basis, projectors and LCAO coefficients '
                        'are read from this file')


def add_voronoi_weights_read_arguments(parser):
    parser.add_argument('-V', '--voronoi', required=False,
                        help='Read Voronoi weights in KS basis from this file.\n\n'
                             'Must be in ASE ULM format.')
    add_voronoi_weights_arguments(parser)


def add_voronoi_weights_save_arguments(parser):
    parser.add_argument('-o', '--output-file', required=True,
                        help='Save the computed weights in this file.\n\n'
                             'Use .npz extension to save as a (non-compressed) numpy zip archive. '
                             'Use .ulm extension to save in ASE ULM format. The latter is suitable '
                             'for large files, as the entire file need not be held in memory')
    parser.add_argument('-L', '--only-lcao', action='store_true',
                        help='Compute the weights in LCAO basis and save to OUTPUT_FILE. '
                        'The transformation to Kohn-Sham basis will not be done')
    add_voronoi_weights_arguments(parser)


def parse_projections(args):
    """ Parse the atom projection arguments

    Each argument can be a comma separated list of either
      - Integers
      - Ranges on the form start:stop:step (same as numpy slicing conventions)
    """

    def parse_range(rstr):
        split = rstr.split(':')
        assert len(split) > 0 and len(split) < 4
        if len(split) == 1:
            return [int(split[0])]
        else:
            ind = [int(s) if len(s) > 0 else None for s in split]
            assert ind[1] is not None, 'Slice to end not allowed yet'
            assert ind[0] >= 0, 'Negative values not allowed yet'
            assert ind[1] >= 0, 'Negative values not allowed yet'
            return list(range(*ind))

    atom_projections = []
    for i, atoms_str in enumerate(args.atoms):
        parts = atoms_str.split(',')
        try:
            atom_list = [atomid for rangestr in parts for atomid in parse_range(rangestr)]
        except ValueError:
            print(f'Argument {i} ("{atoms_str}") is not a comma separated list of integers. ')
            exit(1)
        atom_projections.append(atom_list)

    return atom_projections


def parse_voronoi_lcao_weights(parser,
                               args,
                               warn_gs: bool = True) -> VoronoiLCAOWeights:
    voronoi_lcao: VoronoiLCAOWeights
    if args.lcao_weights is None:
        # Compute Voronoi weights in LCAO basis

        if args.gpw_file is None:
            print('GPW_FILE must be given')
            exit(1)

        atom_projections = parse_projections(args)
        if len(atom_projections) == 0:
            print('atoms must not be empty')
            exit(1)

        voronoi_lcao = VoronoiLCAOWeightCalculator(
            atom_projections=atom_projections,
            gpw_file=args.gpw_file,
            voronoi_grid_file=args.grid_file,
            recalculate_grid=args.calculate_grid,
            domain=args.domain)
    else:
        # Read Voronoi weights in LCAO basis
        if args.domain != parser.get_default('domain'):
            print(f'Ignoring domain setting {args.domain} when reading LCAO weights')
        if args.gpw_file is not None and warn_gs:
            print(f'Ignoring GPW_FILE setting {args.gpw_file} when reading LCAO weights')

        if args.lcao_weights[-4:] == '.ulm':
            voronoi_lcao = VoronoiLCAOReader(args.lcao_weights, comm_is_domain=False)
        else:
            print('Reading LCAO weights is only supported from ULM formatted '
                  f'files. File must have extension .ulm, has {args.lcao_weights}')
            exit(1)

    return voronoi_lcao


def parse_voronoi_weights(parser,
                          args,
                          warn_gs: bool = True) -> VoronoiWeights:
    voronoi_fname = getattr(args, 'voronoi', None)

    use_pblas = True
    voronoi: VoronoiWeights

    if voronoi_fname is None:
        # Calculate Voronoi weights in KS basis

        # Keep parsing arguments to find out how
        voronoi_lcao = parse_voronoi_lcao_weights(parser, args, warn_gs=warn_gs)
        voronoi = VoronoiWeightCalculator(voronoi_lcao, use_pblas=use_pblas)
    else:
        # Read Voronoi weights in KS basis
        if voronoi_fname[-4:] == '.ulm':
            voronoi = VoronoiReader(voronoi_fname)
        else:
            print('Reading Voronoi weights is only supported from ULM formatted '
                  f'files. File must have extension .ulm, has {voronoi_fname}')
            exit(1)

    return voronoi


def atom_projections_to_numpy(atom_projections: AtomProjectionsType) -> NDArray[np.int_]:
    Ni = len(atom_projections)
    if Ni == 0:
        Nj = 0
    else:
        Nj = max([len(proj_atoms) for proj_atoms in atom_projections])
    atom_projections_ij = np.full((Ni, Nj), -1, dtype=int)
    for i, proj_atoms in enumerate(atom_projections):
        na = len(proj_atoms)
        atom_projections_ij[i, :na] = proj_atoms

    return atom_projections_ij
