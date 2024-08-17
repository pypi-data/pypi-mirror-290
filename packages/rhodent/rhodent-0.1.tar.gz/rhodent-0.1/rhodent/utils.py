from __future__ import annotations

import time
import numpy as np
from numpy.typing import NDArray
from numpy._typing import _DTypeLike as DTypeLike  # parametrizable wrt generic

from contextlib import nullcontext
from typing import Callable, Iterator, Iterable, NamedTuple, Union, TypeVar

from ase.io.ulm import open
from ase.parallel import parprint
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.laser import GaussianPulse
from gpaw.matrix import Matrix, suggest_blocking
from gpaw.mpi import SerialCommunicator, world
from gpaw.tddft.units import fs_to_au, au_to_eV

from rhodent.typing import Communicator

DTypeT = TypeVar('DTypeT', bound=np.generic, covariant=True)


class Logger:

    _t0: float
    _starttimes: dict[str, float]

    def __init__(self,
                 t0: float | None = None,
                 comm=None):
        self._starttimes = dict()
        if t0 is None:
            self._t0 = time.time()
        else:
            assert isinstance(t0, float)
            self._t0 = t0
        self.comm = comm

    @property
    def t0(self) -> float:
        return self._t0

    @t0.setter
    def t0(self,
           value: float | None):
        if value is None:
            self._t0 = time.time()
            return
        assert isinstance(value, float)
        self._t0 = value

    @property
    def comm(self) -> Communicator:
        return self._comm

    @comm.setter
    def comm(self, value: Communicator):
        if value is None:
            self.comm = world
            return

        assert hasattr(value, 'rank')
        assert hasattr(value, 'size')
        self._comm = value

    def __getitem__(self, key) -> float:
        return self._starttimes.get(key, self.t0)

    def __call__(self, *args, rank: int | None = None, **kwargs):
        if rank is not None and self.comm.rank != rank:
            return
        return self.log(*args, **kwargs)

    def __str__(self) -> str:
        s = f'{self.__class__.__name__} t0: {self.t0} comm: {self.comm}'
        return s

    def log(self, *args, **kwargs):
        commstr = f'[{self.comm.rank:04.0f}/{self.comm.size:04.0f}]'
        hh, rem = divmod(time.time() - self.t0, 3600)
        mm, ss = divmod(rem, 60)
        timestr = f'[{hh:02.0f}:{mm:02.0f}:{ss:04.1f}]'
        print(f'{commstr} {timestr}', *args, **kwargs)

    def start(self, key):
        self._starttimes[key] = time.time()

    def elapsed(self, key) -> float:
        return time.time() - self[key]


class NoLogger(Logger):

    def __str__(self) -> str:
        return self.__class__.__name__

    def log(self, *args, **kwargs):
        pass


class ResultKeys():

    _keys_dimensions_dtypes: dict[str, tuple[tuple[int, ...], np.dtype]]

    def __init__(self,
                 *scalar_keys):
        self._keys_dimensions_dtypes = dict()

        for key in scalar_keys:
            self.add_key(key, (), float)

    def add_key(self,
                key: str,
                shape: tuple[int, ...] | int = (),
                dtype: DTypeLike = float):
        assert isinstance(key, str)
        if isinstance(shape, int):
            shape = (shape, )
        assert all([isinstance(d, int) for d in shape])
        dtype = np.dtype(dtype)
        self._keys_dimensions_dtypes[key] = (shape, dtype)

    def remove(self,
               key: str):
        assert key in self
        self._keys_dimensions_dtypes.pop(key)

    def __contains__(self,
                     key: str) -> bool:
        return key in self._keys_dimensions_dtypes.keys()

    def __iter__(self) -> Iterator[tuple[str, tuple[int, ...], np.dtype]]:
        for key, (shape, dtype) in self._keys_dimensions_dtypes.items():
            yield key, shape, dtype

    def __getitem__(self,
                    key: str) -> tuple[tuple[int, ...], np.typing.DTypeLike]:
        assert key in self._keys_dimensions_dtypes, f'Key {key} not among keys'
        return self._keys_dimensions_dtypes[key]

    def __copy__(self):
        cpy = ResultKeys()
        cpy._keys_dimensions_dtypes.update(self._keys_dimensions_dtypes)
        return cpy


class Result:

    _data: dict[str, NDArray[np.float64]]

    def __init__(self,
                 mutable: bool = False):
        self._data = dict()
        self._mutable = mutable

    def __contains__(self,
                     key: str) -> bool:
        return key in self._data

    def __setitem__(self,
                    key: str,
                    value: np.typing.ArrayLike | int):
        if not self._mutable:
            assert key not in self._data, f'Key {key} is already among results'
        if np.ndim(value) == 0:
            value = np.array([value])
        self._data[key] = np.ascontiguousarray(value)

    def __getitem__(self,
                    key: str) -> NDArray[np.float64]:
        assert key in self._data, f'Key {key} not among results'
        return self._data[key]

    def __str__(self) -> str:
        lines = [f'{self.__class__.__name__} with arrays (dimensions)']

        for key, data in self._data.items():
            lines.append(f'  {key} {data.shape}')

        return '\n'.join(lines)

    def set_to(self,
               key: str,
               idx,
               value: np.typing.ArrayLike | int | float):
        if np.ndim(self._data[key][idx]) == 0:
            assert np.size(value) == 1
            value = np.atleast_1d(value)[0]
        self._data[key][idx] = value

    def add_to(self,
               key: str,
               idx,
               value: np.typing.ArrayLike | int | float):
        if np.ndim(self._data[key][idx]) == 0:
            assert np.size(value) == 1
            value = np.atleast_1d(value)[0]
        self._data[key][idx] += value

    def create_all_empty(self,
                         keys: ResultKeys):
        for key, shape, dtype in keys:
            if key in self:
                continue
            self[key] = np.empty(shape, dtype=dtype)

    def create_all_zeros(self,
                         keys: ResultKeys):
        for key, shape, dtype in keys:
            if key in self:
                continue
            self[key] = np.zeros(shape, dtype=dtype)

    def remove(self,
               key: str):
        assert key in self._data
        self._data.pop(key)

    def empty(self,
              key: str,
              keys: ResultKeys):
        shape, dtype = keys[key]
        self[key] = np.empty(shape, dtype=dtype)

    def assert_keys(self,
                    keys: ResultKeys):
        copy = dict(self._data)
        try:
            for key, shape, dtype in keys:
                array = copy.pop(key)
                if len(shape) == 0:
                    assert array.shape == (1, ), f'{array.shape} != (1,)'
                else:
                    assert array.shape == shape, f'{array.shape} != {shape}'
                assert array.dtype == dtype, f'{array.dtype} != {dtype}'
        except KeyError:
            raise AssertionError(f'Key {key} missing from Result')
        assert len(copy) == 0, f'Result has additional keys {copy.keys()}'

    def send(self,
             keys: ResultKeys,
             rank,
             comm):
        self.assert_keys(keys)
        for vi, (key, _, _) in enumerate(keys):
            value = self._data[key]
            comm.send(value, rank, tag=100 + vi)

    def inplace_receive(self,
                        keys: ResultKeys,
                        rank: int,
                        comm):
        self.assert_keys(keys)
        for vi, (key, _, _) in enumerate(keys):
            value = self._data[key]
            comm.receive(value, rank, tag=100 + vi)


class ArrayIsOnRootRank(NDArray[DTypeT]):
    def __new__(cls):
        """ Instances will act as empty numpy arrays """
        return NDArray.__new__(cls, (0, ))


DistributedArray = Union[NDArray[DTypeT], ArrayIsOnRootRank]


def gauss_ij_with_filter(energy_i: np.typing.ArrayLike,
                         energy_j: np.typing.ArrayLike,
                         sigma: float,
                         fltthresh: float | None = None,
                         ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    r""" Computes the matrix

    .. math::

        M_{ij}
        = \frac{1}{\sqrt{2 \pi \sigma^2}}
        \exp\left(-\frac{
            \left(\varepsilon_i - \varepsilon_j\right)^2
        }{
            2 \sigma^2
        }\right)

    Useful for Gaussian broadening. Optionally only computes the exponent
    above a certain threshold, and returns the filter

    Parameters
    ----------
    energy_i
        Energies :math:`\varepsilon_i`
    energy_j
        Energies :math:`\varepsilon_j`
    sigma
        Gaussian broadening width :math:`\sigma`
    fltthresh
        Filtering threshold

    Returns
    -------
        Matrix :math:`M_{ij}`, filter
    """
    energy_i = np.asarray(energy_i)
    energy_j = np.asarray(energy_j)

    norm = 1.0 / (sigma * np.sqrt(2 * np.pi))

    denergy_ij = energy_i[:, np.newaxis] - energy_j[np.newaxis, :]
    exponent_ij = -0.5 * (denergy_ij / sigma) ** 2

    if fltthresh is not None:
        flt_i = np.any(exponent_ij > fltthresh, axis=1)
        M_ij = np.zeros_like(exponent_ij)
        M_ij[flt_i] = norm * np.exp(exponent_ij[flt_i])
    else:
        flt_i = np.ones(energy_i.shape, dtype=bool)
        M_ij = norm * np.exp(exponent_ij)

    return M_ij, flt_i


def gauss_ij(energy_i: np.typing.ArrayLike,
             energy_j: np.typing.ArrayLike,
             sigma: float) -> NDArray[np.float64]:
    r""" Computes the matrix

    .. math::

        M_{ij}
        = \frac{1}{\sqrt{2 \pi \sigma^2}}
        \exp\left(-\frac{
            \left(\varepsilon_i - \varepsilon_j\right)^2
        }{
            2 \sigma^2
        }\right),

    which is useful for Gaussian broadening.

    Parameters
    ----------
    energy_i
        Energies :math:`\varepsilon_i`
    energy_j
        Energies :math:`\varepsilon_j`
    sigma
        Gaussian broadening width :math:`\sigma`

    Returns
    -------
        Matrix :math:`M_{ij}`
    """
    M_ij, _ = gauss_ij_with_filter(energy_i, energy_j, sigma)
    return M_ij


def broaden_n2e(M_n: np.typing.ArrayLike,
                energy_n: np.typing.ArrayLike,
                energy_e: np.typing.ArrayLike,
                sigma: float) -> NDArray[np.float64]:
    r""" Broaden matrix onto energy grids

    .. math::

        M(\varepsilon_e)
        = \sum_n M_n \frac{1}{\sqrt{2 \pi \sigma^2}}
        \exp\left(-\frac{
            \left(\varepsilon_n - \varepsilon_e\right)^2
        }{
            2 \sigma^2
        }\right),

    Returns
    -------
        :math:`M(\varepsilon_0)`
    """
    M_n = np.asarray(M_n)
    gauss_ne, flt_n = gauss_ij_with_filter(energy_n, energy_e, sigma)

    M_e = np.einsum('n,ne->e', M_n[flt_n], gauss_ne[flt_n], optimize=True)

    return M_e


def broaden_xn2e(M_xn: np.typing.ArrayLike,
                 energy_n: np.typing.ArrayLike,
                 energy_e: np.typing.ArrayLike,
                 sigma: float) -> NDArray[np.float64]:
    r""" Broaden matrix onto energy grids

    .. math::

        M(\varepsilon_e)
        = \sum_n M_n \frac{1}{\sqrt{2 \pi \sigma^2}}
        \exp\left(-\frac{
            \left(\varepsilon_n - \varepsilon_e\right)^2
        }{
            2 \sigma^2
        }\right),

    Returns
    -------
        :math:`M(\varepsilon_0)`
    """
    M_xn = np.asarray(M_xn)
    gauss_ne, flt_n = gauss_ij_with_filter(energy_n, energy_e, sigma)

    M_xe = np.einsum('xn,ne->xe',
                     M_xn.reshape((-1, len(flt_n)))[:, flt_n],
                     gauss_ne[flt_n],
                     optimize=True).reshape(M_xn.shape[:-1] + (-1, ))

    return M_xe


def broaden_ia2ou(M_ia: np.typing.ArrayLike,
                  energy_i: np.typing.ArrayLike,
                  energy_a: np.typing.ArrayLike,
                  energy_o: np.typing.ArrayLike,
                  energy_u: np.typing.ArrayLike,
                  sigma: float) -> NDArray[np.float64]:
    r""" Broaden matrix onto energy grids.

    .. math::

        M(\varepsilon_o, \varepsilon_u)
        = \sum_{ia} M_{ia} \frac{1}{\sqrt{2 \pi \sigma^2}}
        \exp\left(-\frac{
            (\varepsilon_i - \varepsilon_o)^2
        }{
            2 \sigma^2
        }\right)
        \exp\left(-\frac{
            (\varepsilon_a - \varepsilon_u)^2
        }{
            2 \sigma^2
        }\right)

    Returns
    -------
        :math:`M(\varepsilon_o, \varepsilon_u)`
    """
    M_ia = np.asarray(M_ia)
    ia_shape = M_ia.shape[:2]
    x_shape = M_ia.shape[2:]
    M_iax = M_ia.reshape(ia_shape + (-1, ))
    gauss_io, flt_i = gauss_ij_with_filter(energy_i, energy_o, sigma)
    gauss_au, flt_a = gauss_ij_with_filter(energy_a, energy_u, sigma)

    M_oux = np.einsum('iax,io,au->oux', M_iax[flt_i, :][:, flt_a],
                      gauss_io[flt_i], gauss_au[flt_a],
                      optimize=True, order='C')

    return M_oux.reshape(M_oux.shape[:2] + x_shape)


def get_array_filter(values: NDArray[np.float64],
                     filter_values: list[float] | NDArray[np.float64] | None) -> slice | NDArray[np.bool_]:
    """ Get array filter that can be used to filter out data.

    Parameters
    ----------
    values
        Array of values, e.g. linspace of times or frequencies
    filter_values
        List of values that one wishes to extract. The closes values from values
        will be selected as filter

    Returns
    -------
        Object that can be used to index values and arrays with the same shape as values
    """
    flt_x: slice | NDArray[np.bool_]
    if filter_values is None or len(filter_values) == 0:
        flt_x = slice(None)
    else:
        flt_x = np.zeros(len(values), dtype=bool)
        search_x = np.searchsorted(values, np.asarray(filter_values) - 1e-6)
        search_x[search_x == len(values)] = len(values) - 1
        flt_x[search_x] = True

    return flt_x


def two_communicator_sizes(*comm_sizes) -> tuple[int, int]:
    assert len(comm_sizes) == 2
    comm_size_c: list[int] = [world.size if size == 'world' else size for size in comm_sizes]
    if comm_size_c[0] == -1:
        comm_size_c[0] = world.size // comm_size_c[1]
    elif comm_size_c[1] == -1:
        comm_size_c[1] = world.size // comm_size_c[0]

    assert np.prod(comm_size_c) == world.size, \
        f'Communicator sizes must factorize world size {world.size} '\
        'but they are ' + ' and '.join([str(s) for s in comm_size_c]) + '.'
    return comm_size_c[0], comm_size_c[1]


def two_communicators(*comm_sizes) -> tuple[Communicator, Communicator]:
    """ Create two MPI communicators.

    Must satisfy ``comm_sizes[0] * comm_sizes[1] = world.size``.

    The second communicator has the ranks in sequence.

    Example
    -------

    >>> world.size == 8
    >>> two_communicators(2, 4)

    This gives::

        [0, 4]
        [1, 5]
        [2, 6]
        [3, 7]

    and::

        [0, 1, 2, 3]
        [4, 5, 6, 7]
    """
    comm_size_c = two_communicator_sizes(*comm_sizes)

    # Create communicators
    if comm_size_c[0] == 1:
        return (SerialCommunicator(), world)  # type: ignore
    elif comm_size_c[0] == world.size:
        return (world, SerialCommunicator())  # type: ignore
    else:
        assert world.size % comm_size_c[0] == 0, world.size
        # Comm 2, ranks in sequence. Comm 1, ranks skip by size of comm 2
        first_rank_in_comm_c = [world.rank % comm_size_c[1],
                                world.rank - world.rank % comm_size_c[1]]
        step_c = [comm_size_c[1], 1]
        comm_ranks_cr = [list(range(start, start + size*step, step))
                         for start, size, step in zip(first_rank_in_comm_c, comm_size_c, step_c)]
        comm_c = [world.new_communicator(comm_ranks_r) for comm_ranks_r in comm_ranks_cr]
        return comm_c[0], comm_c[1]


def detect_repeatrange(n: int,
                       stride: int,
                       verbose: bool = True) -> slice | None:
    """ If an array of length :attr:`n` is not divisible by the stride :attr:`stride`
    then some work will have to be repeated
    """
    final_start = (n // stride) * stride
    repeatrange = slice(final_start, n)
    if repeatrange.start == repeatrange.stop:
        return None
    else:
        print(f'Detected repeatrange {repeatrange}', flush=True)
        return repeatrange

    return None


def safe_fill(a: NDArray[DTypeT],
              b: NDArray[DTypeT]):
    """ Perform the operation ``a[:] = b``, checking if the dimensions match.

    If the dimensions of :attr:`b` are larger than the dimensions of :attr:`a`, raise an error.

    If the dimensions of :attr:`b` are smaller than the dimensions of :attr:`a`, write to
    the first elements of :attr:`a`.
    """
    assert len(a.shape) == len(b.shape), f'{a.shape} != {b.shape}'
    assert all([dima >= dimb for dima, dimb in zip(a.shape, b.shape)]), f'{a.shape} < {b.shape}'
    s = tuple([slice(dim) for dim in b.shape])
    a[s] = b


def safe_fill_larger(a: NDArray[DTypeT],
                     b: NDArray[DTypeT]):
    """ Perform the operation ``a[:] = b``, checking if the dimensions match

    If the dimensions of :attr:`b` are smaller than the dimensions of :attr:`a`, raise an error

    If the dimensions of :attr:`b` are larger than the dimensions of :attr:`a`, write the first
    elements of :attr:`b` to :attr:`a`.
    """
    assert len(a.shape) == len(b.shape), f'{a.shape} != {b.shape}'
    assert all([dimb >= dima for dima, dimb in zip(a.shape, b.shape)]), f'{a.shape} > {b.shape}'
    s = tuple([slice(dim) for dim in a.shape])
    a[:] = b[s]


IND = TypeVar('IND', slice, tuple[slice, ...])


def concatenate_indices(indices_list: Iterable[IND],
                        ) -> tuple[IND, list[IND]]:
    """ Concatenate indices

    Given an array A and a list of incides indices_list such that A can be indexed

    >>> for indices in indices_list:
    >>>     A[indices]

    this function shall concatenate the indices into indices_concat so that the array
    can be indexed in one go. This function will also give a new list of indices
    new_indices_list that can be used to index the A[indices_concat]. The following
    snippet shall be equivalent to the previous snipped

    >>> B = A[indices_concat]
    >>> for indices in new_indices_list:
    >>>     B[indices]

    Note that the indices need not be ordered, nor contigous, but the returned
    indices_concat will be a list of slices, and thus contiguous.

    Example
    -------

    >>> A = np.random.rand(100)
    >>> value = 0
    >>> new_value = 0
    >>>
    >>> indices_list = [slice(10, 12), slice(12, 19)]
    >>> for indices in indices_list:
    >>>     value += np.sum(A[indices])
    >>>
    >>> indices_concat, new_indices_list = concatenate_indices(indices_list)
    >>> new_value = np.sum(A[indices_concat])
    >>>
    >>> assert abs(value - new_value) < 1e-10
    >>>
    >>> B = A[indices_concat]
    >>> assert B.shape == (9, )
    >>> new_value = 0
    >>> for indices in new_indices_list:
    >>>     new_value += np.sum(B[indices])
    >>>
    >>> assert abs(value - new_value) < 1e-10

    Returns
    -------
        (indices_concat, new_indices_list)
    """
    indices_list = list(indices_list)
    if len(indices_list) == 0:
        return slice(0), []  # type: ignore

    if not isinstance(indices_list[0], tuple):
        # If indices are not tuples, then wrap everything in tuples and recurse
        assert all([not isinstance(indices, tuple) for indices in indices_list])
        _indices_concat, _new_indices_list = _concatenate_indices([(indices, ) for indices in indices_list])
        return _indices_concat[0], [indices[0] for indices in _new_indices_list]

    # All indices are wrapped in tuples
    assert all([isinstance(indices, tuple) for indices in indices_list])
    return _concatenate_indices(indices_list)  # type: ignore


def _concatenate_indices(indices_list: Iterable[tuple[slice, ...]],
                         ) -> tuple[tuple[slice, ...], list[tuple[slice, ...]]]:
    """ See :func:`concatenate_indices`
    """
    limits_jis = np.array([[(index.start, index.stop, index.step) for index in indices]
                           for indices in indices_list])

    start_i = np.min(limits_jis[..., 0], axis=0)
    stop_i = np.max(limits_jis[..., 1], axis=0)

    indices_concat = tuple([slice(start, stop) for start, stop in zip(start_i, stop_i)])
    new_indices_list = [tuple([slice(start - startcat, stop - startcat, step)
                               for (startcat, (start, stop, step)) in zip(start_i, limits_is)])
                        for limits_is in limits_jis]

    return indices_concat, new_indices_list


def redistribute_LCAO_into_block_cyclic_form(C_nM,
                                             nn,
                                             band_comm):
    """ Redistribute LCAO coefficients into a block cyclic form
    for PLBAS/ScaLAPACK.

    Parameters
    ----------
    C_nM
        LCAO coefficients distributed over bands
    nn
        Global number of bands
    band_comm
        Band communicator

    Returns
    -------
        Matrix object in block cyclic form
    """
    # mynn is the number of bands on this rank
    mynn, nM = C_nM.shape
    maxlocalnn = (nn + band_comm.size - 1) // band_comm.size
    assert mynn <= maxlocalnn

    dist = (band_comm, ) + suggest_blocking(nn, band_comm.size)
    dist_serial = (band_comm, 1, 1, None)
    dist_C_nM = Matrix(nn, nM, dtype=C_nM.dtype, dist=dist)
    serial_C_nM = Matrix(nn, nM, dtype=C_nM.dtype, dist=dist_serial)

    # Gather to root to begin with
    if band_comm.rank == 0:
        serial_C_nM.array[:mynn] = C_nM
        for sendrank in range(1, band_comm.size):
            slicen = slice(maxlocalnn * sendrank, min(maxlocalnn * (sendrank + 1), nn))
            band_comm.receive(serial_C_nM.array[slicen], sendrank)
    else:
        band_comm.send(C_nM, 0)

    serial_C_nM.redist(dist_C_nM)

    return dist_C_nM


def proj_as_dict_on_master(proj, n1: int, n2: int):
    P_nI = proj.collect()
    if P_nI is None:
        return {}
    I1 = 0
    P_ani = {}
    for a, ni in enumerate(proj.nproj_a):
        I2 = I1 + ni
        P_ani[a] = P_nI[n1:n2, I1:I2]
        I1 = I2
    return P_ani


def parulmopen(fname: str, comm: Communicator, *args, **kwargs):
    if comm.rank == 0:
        return open(fname, *args, **kwargs)
    else:
        return nullcontext()


def proxy_sknX_slicen(reader, *args, comm: Communicator) -> NDArray[np.complex64]:
    if len(args) == 0:
        A_sknX = reader
    else:
        A_sknX = reader.proxy(*args)
    nn = A_sknX.shape[2]
    nlocaln = (nn + comm.size - 1) // comm.size
    myslicen = slice(comm.rank * nlocaln, (comm.rank + 1) * nlocaln)
    my_A_sknX = np.array([[A_nX[myslicen] for A_nX in A_knX] for A_knX in A_sknX])

    return my_A_sknX


def add_fake_kpts(ksd: KohnShamDecomposition):
    """This function is necessary to read some fields without having a
    calculator attached.
    """

    class FakeKpt(NamedTuple):
        s: int
        k: int

    class FakeKsl(NamedTuple):
        using_blacs: bool = False

    # Figure out
    ksdreader = ksd.reader
    skshape = ksdreader.eig_un.shape[:2]
    kpt_u = [FakeKpt(s=s, k=k)
             for s in range(skshape[0])
             for k in range(skshape[1])]
    ksd.kpt_u = kpt_u
    ksd.ksl = FakeKsl()


def create_pulse(frequency: float,
                 fwhm: float = 5.0,
                 t0: float = 10.0,
                 print: Callable | None = None) -> GaussianPulse:
    """ Create Gaussian laser pulse.

    frequency
        Pulse frequncy in eV
    fwhm
        Full width at half maximum in time domain in fs
    t0
        Maximum of pulse envelope in fs
    print
        Printing function to control verbosity
    """
    if print is None:
        print = parprint

    # Pulse
    fwhm_eV = 8 * np.log(2) / (fwhm * fs_to_au) * au_to_eV
    tau = fwhm / (2 * np.sqrt(2 * np.log(2)))
    sigma = 1 / (tau * fs_to_au) * au_to_eV  # eV
    strength = 1e-6
    t0 = t0 * 1e3
    sincos = 'cos'
    print(f'Creating pulse at {frequency:.3f}eV with FWHM {fwhm:.2f}fs '
          f'({fwhm_eV:.2f}eV) t0 {t0:.1f}fs', flush=True)

    return GaussianPulse(strength, t0, frequency, sigma, sincos)
