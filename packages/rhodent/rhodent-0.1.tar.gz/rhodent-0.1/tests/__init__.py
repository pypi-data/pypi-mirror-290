from __future__ import annotations

from contextlib import contextmanager
import os
import numpy as np
from pathlib import Path

testdatapath = Path('tests/data')

permanent_test_files: dict[str, dict[str, Path]] = {
    '2H2': {
        'gpw_fname': testdatapath / '2H2_unocc.gpw',  # Large file; not in git repo
        'fdm_fname': testdatapath / '2H2_fdm.ulm',
        'wfs_fname': testdatapath / '2H2_wfs.ulm',
        'wfssnap_fname': testdatapath / '2H2_wfssnap.ulm',
        'ref_density_matrix': testdatapath / '2H2_ref.npz',
        'ref_voronoi': testdatapath / '2H2_voronoi_ref.npz',
        'ref_hcdist': testdatapath / '2H2_hcdist_ref.npz',
        },
    'Na8': {
        'gpw_fname': testdatapath / 'Na8_unocc.gpw',  # Large file; not in git repo
        'fdm_fname': testdatapath / 'Na8_fdm.ulm',  # Large file; not in git repo
        'wfs_fname': testdatapath / 'Na8_wfs.ulm',  # Large file; not in git repo
        'wfssnap_fname': testdatapath / 'Na8_wfssnap.ulm',
        'ref_density_matrix': testdatapath / 'Na8_ref.npz',
        'ref_voronoi': testdatapath / 'Na8_voronoi_ref.npz',
        'ref_hcdist': testdatapath / 'Na8_hcdist_ref.npz',
        },
    'Ag8': {
        'gpw_fname': testdatapath / 'Ag8_unocc.gpw',  # Large file; not in git repo
        'fdm_fname': testdatapath / 'Ag8_fdm.ulm',  # Large file; not in git repo
        'wfs_fname': testdatapath / 'Ag8_wfs.ulm',  # Large file; not in git repo
        'wfssnap_fname': testdatapath / 'Ag8_wfssnap.ulm',
        'ref_density_matrix': testdatapath / 'Ag8_ref.npz',
        'ref_voronoi': testdatapath / 'Ag8_voronoi_ref.npz',
        'ref_hcdist': testdatapath / 'Ag8_hcdist_ref.npz',
        },
    'Na_5x5': {
        'ksd_fname': testdatapath / 'Na_5x5_ksd.ulm',
        },
}


def nottest(obj):
    obj.__test__ = False
    return obj


def wrap_test(source_fct):
    from inspect import signature

    def copy(target_fct):
        # target_fct is just a dummy
        def calltest(*args, **kwargs):
            source_fct(*args, **kwargs)

        calltest.__signature__ = signature(source_fct)
        return calltest

    return copy


@nottest
def get_permanent_test_file(test_system, key):
    assert test_system in permanent_test_files, f'{test_system} is an invalid test system'
    return permanent_test_files[test_system][key]


@nottest
def ksbasis(gpw_fname, ksd_fname, only_ia=True):
    from gpaw import GPAW
    from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

    # Calculate ground state with full unoccupied space
    calc = GPAW(str(gpw_fname), txt='/dev/null')

    # Construct KS electron-hole basis
    ksd = KohnShamDecomposition(calc)
    ksd.initialize(calc, only_ia=only_ia)
    ksd.write(str(ksd_fname))


@nottest
def frho(ksd_fname, fdm_fname, frho_dname):
    from gpaw.mpi import SerialCommunicator, world
    from gpaw.lcaotddft.frequencydensitymatrix import FrequencyDensityMatrixReader
    from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
    from gpaw.tddft.units import au_to_eV

    from rhodent.utils import add_fake_kpts

    calc_comm = SerialCommunicator()
    loop_comm = world

    # Output directory
    if world.rank == 0:
        if not os.path.isdir(frho_dname):
            os.makedirs(frho_dname)
    world.barrier()

    # Load ksd and fdm
    ksd = KohnShamDecomposition(filename=str(ksd_fname))
    ksd.distribute(calc_comm)
    add_fake_kpts(ksd)
    fdm = FrequencyDensityMatrixReader(str(fdm_fname), ksd.ksl, ksd.kpt_u)

    ffreq_w = fdm.freq_w
    rw_i = [(r, w) for r in ['Re', 'Im'] for w in range(len(ffreq_w))]
    for i in range(loop_comm.rank, len(rw_i), loop_comm.size):
        reim, w = rw_i[i]
        ffreq = ffreq_w[w]
        freq = ffreq.freq * au_to_eV
        folding = ffreq.folding.folding
        if folding is None:
            fname = 'w%05.2f-%s.npy' % (freq, reim)
        else:
            width = ffreq.folding.width * au_to_eV
            fname = 'w%05.2f-%s-%.3f-%s.npy' % (freq, folding, width, reim)
        fpath = os.path.join(frho_dname, fname)
        if not os.path.exists(fpath):
            print('Calculate %s' % fpath)
            rho_uMM = fdm.read_FDrho(reim, [w])[0]
            rho_p = ksd.transform(rho_uMM)[0]
            np.save(fpath, rho_p)


@contextmanager
def temporary_ksbasis(gpw_fname):
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tempdir:
        path = Path(tempdir)
        ksd_fname = path / 'ksd.ulm'
        ksbasis(gpw_fname, ksd_fname)

        yield ksd_fname
