from __future__ import annotations

import os
import warnings
from contextlib import contextmanager
from pathlib import Path

from ase.io.ulm import Reader
from gpaw.mpi import world

import pytest

from tests import frho, ksbasis, get_permanent_test_file, permanent_test_files
from tests.mock import (MockKohnShamRhoWfsReader, MockTimeDensityMatrices,
                        MockConvolutionDensityMatrices, MockVoronoiWeights,
                        MockFrequencyDensityMatrices)


@contextmanager
def execute_in_tmp_path(request, tmp_path_factory):
    from gpaw.mpi import broadcast

    if world.rank == 0:
        # Obtain basename as
        # * request.function.__name__  for function fixture
        # * request.module.__name__    for module fixture
        basename = getattr(request, request.scope).__name__
        path = tmp_path_factory.mktemp(basename)
    else:
        path = None
    path = broadcast(path)
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(cwd)


@pytest.fixture(scope='function')
def in_tmp_dir(request, tmp_path_factory):
    """Run test function in a temporary directory."""
    with execute_in_tmp_path(request, tmp_path_factory) as path:
        yield path


@pytest.fixture(scope='session')
def cache_path(request, tmp_path_factory) -> Path:
    """ Path for cached test data """
    import re
    from gpaw.mpi import broadcast

    pathstr: str | None = os.environ.get('GPW_TEST_FILES')
    if pathstr is not None:
        return Path(pathstr)

    warnings.warn(
        'Note that you can speed up the tests by reusing gpw-files '
        'from an earlier pytest session: '
        'set the $GPW_TEST_FILES environment variable and the '
        'files will be written to/read from that folder. ')
    if world.rank == 0:
        name = request.node.name
        name = re.sub(r'[\W]', '_', name)
        name = 'rhodent' if name == '' else name  # Explicitly needed in pytest 8.0.2
        MAXVAL = 30
        name = name[:MAXVAL]
        path = tmp_path_factory.mktemp(name, numbered=True)
        broadcast(path)
    else:
        path = broadcast(None)

    return path


@pytest.fixture
def cached_file_if_existing(cache_path, test_system):

    def _cached_file_if_existing(fname: str, check_empty: bool = False) -> tuple[Path, bool]:
        """ Return path to datafile in cache directory and whether it exists """

        from gpaw.mpi import broadcast

        parent = cache_path / test_system
        parent.mkdir(exist_ok=True)
        path = parent / fname
        if world.rank == 0:
            exists = path.exists()
            if exists and check_empty:
                exists = next(path.iterdir(), 'empty') != 'empty'
            broadcast(exists)
        else:
            exists = broadcast(None)

        return path, exists

    return _cached_file_if_existing


@pytest.fixture
def gpw_fname(test_system):
    return get_permanent_test_file(test_system, 'gpw_fname')


@pytest.fixture
def fdm_fname(test_system):
    return get_permanent_test_file(test_system, 'fdm_fname')


@pytest.fixture
def wfs_fname(test_system):
    return get_permanent_test_file(test_system, 'wfs_fname')


@pytest.fixture
def wfssnap_fname(test_system):
    return get_permanent_test_file(test_system, 'wfssnap_fname')


@pytest.fixture
def ref_density_matrix(test_system):
    return get_permanent_test_file(test_system, 'ref_density_matrix')


@pytest.fixture
def ref_voronoi(test_system):
    return get_permanent_test_file(test_system, 'ref_voronoi')


@pytest.fixture
def ref_hcdist(test_system):
    return get_permanent_test_file(test_system, 'ref_hcdist')


@pytest.fixture
def ksd_fname(cached_file_if_existing, test_system):
    """ Calculate the KohnShamDecomposition, or use a cached file """
    try:
        return get_permanent_test_file(test_system, 'ksd_fname')
    except KeyError:
        pass

    path, exists = cached_file_if_existing('ksd.ulm')
    if not exists:
        # Calculate the ksbasis
        gpw_fname = permanent_test_files[test_system]['gpw_fname']
        ksbasis(gpw_fname=gpw_fname, ksd_fname=path)
    return path


@pytest.fixture
def frho_dname(cached_file_if_existing, test_system, ksd_fname):
    path, exists = cached_file_if_existing('frho', check_empty=True)
    if not exists:
        # Extract the frho
        frho(ksd_fname=ksd_fname,
             fdm_fname=permanent_test_files[test_system]['fdm_fname'],
             frho_dname=path)
    return path


@pytest.fixture
def mock_voronoi(test_system, ksd_fname):
    with Reader(ksd_fname) as reader:
        nn = reader.eig_un.shape[2]

    def factory(**kwargs):
        reader = MockVoronoiWeights(nn=nn, **kwargs)
        return reader

    return factory


@pytest.fixture
def mock_ks_rho_reader(test_system, ksd_fname):

    def factory(**kwargs):
        reader = MockKohnShamRhoWfsReader(ksd=ksd_fname, **kwargs)
        return reader

    return factory


@pytest.fixture
def mock_time_density_matrices(test_system, ksd_fname):

    def factory(**kwargs):
        density_matrices = MockTimeDensityMatrices(ksd=ksd_fname, **kwargs)
        return density_matrices

    return factory


@pytest.fixture
def mock_convolution_density_matrices(test_system, ksd_fname):

    def factory(**kwargs):
        density_matrices = MockConvolutionDensityMatrices(ksd=ksd_fname, **kwargs)
        return density_matrices

    return factory


@pytest.fixture
def mock_frequency_density_matrices(test_system, ksd_fname):

    def factory(**kwargs):
        density_matrices = MockFrequencyDensityMatrices(ksd=ksd_fname, **kwargs)
        return density_matrices

    return factory
