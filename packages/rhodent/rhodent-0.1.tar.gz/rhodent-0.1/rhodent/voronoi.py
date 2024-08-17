from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterator, Sequence, Union

import numpy as np
from numpy.typing import NDArray

from gpaw import GPAW
from gpaw.analyse.wignerseitz import wignerseitz
from gpaw.arraydict import ArrayDict
from gpaw.matrix import Matrix, suggest_blocking
from gpaw.mpi import SerialCommunicator, broadcast, world
from gpaw.utilities.partition import AtomPartition
from gpaw.utilities.tools import tri2full

from .utils import Logger, parulmopen, proj_as_dict_on_master, redistribute_LCAO_into_block_cyclic_form
from .typing import Communicator, GPAWCalculator


AtomProjectionsType = Sequence[Union[list[int], NDArray[np.float64]]]  # | breaks on py3.9


class VoronoiWeights(ABC):

    broadcast_weights: bool
    _comm: Any  # MPI communicator
    _log: Logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def __len__(self) -> int:
        """ Return the number of projections """
        return self.nproj

    @abstractmethod
    def __iter__(self) -> Iterator[NDArray[np.float64] | None]:
        """ Yields the weights

        None is yielded on non-root ranks unless broadcast_weights is True
        """
        raise NotImplementedError

    def __str__(self) -> str:
        lines = [f'{self.__class__.__name__} for ground state with {self.nn} bands',
                 f'{self.nproj} projections:']

        for i, atoms in enumerate(self.atom_projections):
            atomsstr = str(atoms)
            if len(atomsstr) > 50:
                atomsstr = atomsstr[:47] + '...'
            lines.append(f'- #{i:<3.0f}: On atoms {atomsstr}')

        return '\n'.join(lines)

    @property
    def log(self) -> Logger:
        return self._log

    @property
    @abstractmethod
    def atom_projections(self) -> AtomProjectionsType:
        """ Atom projections """
        raise NotImplementedError

    @property
    @abstractmethod
    def nn(self) -> int:
        """ Global number of bands """
        raise NotImplementedError

    @property
    @abstractmethod
    def dtype(self) -> np.dtype:
        """ dtype of wave functions """
        raise NotImplementedError

    @property
    def nproj(self) -> int:
        return len(self.atom_projections)

    @property
    def comm(self) -> Communicator:
        """ Communicator """
        return self._comm

    @property
    @abstractmethod
    def saved_fields(self) -> dict[str, Any]:
        """ Saved data fields associated with the object

        If this object is read from a ULM file there might be some extra
        data in that file. Return that data, or an empty dict if there is none.
        """
        raise NotImplementedError


class EmptyVoronoiWeights(VoronoiWeights):

    def __init__(self):
        self._log = Logger()
        self._comm = self._log.comm
        self.broadcast_weights = True

    def __iter__(self):
        return
        yield

    @property
    def atom_projections(self):
        return []

    @property
    def nn(self):
        return 0

    @property
    def dtype(self):
        return float

    @property
    def saved_fields(self):
        return {}


class VoronoiLCAOWeights(ABC):

    _atom_projections: AtomProjectionsType
    broadcast_weights: bool
    _comm: Any  # MPI communicator
    _log: Logger
    _dS_aii: Any
    _dist_C_nM: NDArray[np.float64] | None = None
    _P_ani: ArrayDict
    _gather_P_ani: ArrayDict | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def __len__(self) -> int:
        """ Return the number of projections """
        return self.nproj

    @abstractmethod
    def __iter__(self) -> Iterator[NDArray[np.float64] | None]:
        """ Yields the weights.

        Different data is returned on different ranks of the domain communicator.
        Duplicate data is returned on different ranks of the band communicator.
        """
        raise NotImplementedError

    @property
    def log(self) -> Logger:
        return self._log

    @property
    @abstractmethod
    def dtype(self) -> np.dtype:
        """ dtype of the wave functions """
        raise NotImplementedError

    @property
    @abstractmethod
    def nn(self) -> int:
        """ Global number of bands """
        raise NotImplementedError

    @property
    @abstractmethod
    def nM(self) -> int:
        """ Global number of bands """
        raise NotImplementedError

    @property
    def nproj(self) -> int:
        """ Number of atomic projections """
        return len(self.atom_projections)

    @property
    def atom_projections(self) -> AtomProjectionsType:
        return self._atom_projections

    @property
    def calc(self) -> GPAWCalculator | None:
        return None

    @property
    def comm(self) -> Communicator:
        """ Communicator """
        return self._comm

    @property
    @abstractmethod
    def C_nM(self):
        """ LCAO wave function coefficients. Distributed over bands. """
        raise NotImplementedError

    @property
    @abstractmethod
    def P_ani(self) -> ArrayDict:
        r""" PAW projectors. Distributed over domains and bands.

        .. math::

            P_{ni}^a = \left<\tilde{p}_i^a | \tilde{\psi}_n \right>
        """
        raise NotImplementedError

    @property
    def dist_C_nM(self):
        """ LCAO wave function coefficients. Distributed in block cyclic form. """
        if self._dist_C_nM is None:
            self._prepare_C()
        return self._dist_C_nM

    @property
    def gather_P_ani(self) -> ArrayDict:
        """ PAW projectors. Gathered to band comm rank 0. None on all other band comm ranks. """
        if self._gather_P_ani is None:
            self._prepare_P()
        assert self._gather_P_ani is not None
        return self._gather_P_ani

    @property
    def dS_aii(self):
        r""" Overlap matrix PAW corrections. Same data on all ranks

        .. math::

            \Delta S_{ij}^a=
            = \left<\phi_i^a|\phi_j^a\right>
            - \left<\tilde{\phi}_i^a|\tilde{\phi}_j^a\right>
        """
        return self._dS_aii

    @property
    def dist(self):
        return self.dist_C_nM.dist

    @abstractmethod
    def _prepare_P(self):
        raise NotImplementedError

    @abstractmethod
    def _prepare_C(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def band_comm(self) -> Communicator:
        raise NotImplementedError

    @property
    @abstractmethod
    def domain_comm(self) -> Communicator:
        raise NotImplementedError

    @property
    @abstractmethod
    def saved_fields(self) -> dict[str, Any]:
        """ Saved data fields associated with the object.

        If this object is read from a ULM file there might be some extra
        data in that file. Return that data, or an empty dict if there is none.
        """
        raise NotImplementedError


class VoronoiReader(VoronoiWeights):

    """ Read Voronoi weights from ulm file.

    Parameters
    ----------
    ulm_fname
        filename
    broadcast_weights
        If true, the array of weights is broadcasted and yielded on all ranks
    comm
        GPAW MPI communicator object. Defaults to world
    """

    _nn: int
    _dtype: np.dtype
    _atom_projections: AtomProjectionsType

    def __init__(self,
                 ulm_fname: str,
                 broadcast_weights: bool = False,
                 comm=None):
        self.ulm_fname = ulm_fname
        self.broadcast_weights = broadcast_weights

        if comm is None:
            comm = world

        self._log = Logger(comm=comm)
        self._comm = comm
        self.reader = parulmopen(self.ulm_fname, self.comm)

        # Read size
        if self.comm.rank == 0:
            weight_inn = self.reader.proxy('weight_inn')
            assert weight_inn.dtype is np.dtype(float)
            assert weight_inn.shape[1] == weight_inn.shape[2]
            atom_projections = self.reader.atom_projections
            nn = weight_inn.shape[1]
            brdcast = (atom_projections, nn, weight_inn.dtype)
        else:
            brdcast = None

        brdcast = broadcast(brdcast, root=0, comm=self.comm)
        self._atom_projections, self._nn, self._dtype = brdcast  # type: ignore

    @property
    def atom_projections(self) -> AtomProjectionsType:
        return self._atom_projections

    @property
    def nn(self) -> int:
        return self._nn

    @property
    def dtype(self) -> np.dtype:
        return self._dtype

    def __exit__(self, exc_type, exc_value, tb):
        self.reader.close()

    def __iter__(self) -> Iterator[NDArray[np.float64] | None]:
        for i in range(len(self)):
            if self.comm.rank == 0:
                weight_nn = self.reader.proxy('weight_inn', i)[:]
            else:
                if self.broadcast_weights:
                    weight_nn = np.empty((self.nn, self.nn), self.dtype)
                else:
                    weight_nn = None
            if self.broadcast_weights:
                self.comm.broadcast(weight_nn, 0)

            yield weight_nn

    @property
    def saved_fields(self) -> dict[str, Any]:
        """ Saved data fields associated with the object

        If this object is read from a ULM file there might be some extra
        data in that file. Return that data, or an empty dict if there is none.
        """
        data = {key: getattr(self.reader, key) for key in self.reader.keys()
                if key not in ['weight_inn', 'atom_projections']}

        return data


class VoronoiLCAOReader(VoronoiLCAOWeights):

    """ Read Voronoi weights in LCAO basis from ulm file.

    Parameters
    ----------
    ulm_fname
        filename
    broadcast_weights
        If true, the array of weights is broadcasted and yielded on all ranks
    comm
        GPAW MPI communicator object. Defaults to world
    """

    _comm_is_domain: bool

    def __init__(self,
                 ulm_fname: str,
                 comm_is_domain: bool = False,
                 comm=None):
        self.ulm_fname = ulm_fname
        self._comm_is_domain = comm_is_domain

        if comm is None:
            comm = world

        self._log = Logger(comm=comm)
        self._comm = comm
        self.reader = parulmopen(self.ulm_fname, self.comm)

        # Read size
        if self.comm.rank == 0:
            weight_iMM = self.reader.proxy('weight_iMM')
            assert weight_iMM.dtype is np.dtype(float)
            assert weight_iMM.shape[1] == weight_iMM.shape[2]
            dS_aii = self.reader.dS_aii
            P_ani = self.reader.P_ani
            shapes_a = [P_ani[a].shape for a in range(len(P_ani))]
            self._C_nM = self.reader.C_nM[:]
            atom_projections = self.reader.atom_projections
            brdcast = (atom_projections, dS_aii, self._C_nM.dtype) + self._C_nM.shape
        else:
            brdcast = None
            P_ani = {}
            self._C_nM = None

        brdcast = broadcast(brdcast, root=0, comm=self.comm)
        self._atom_projections, self._dS_aii, self._dtype, self._nn, self._nM = brdcast  # type: ignore

        natoms = len(self._dS_aii)
        if self.domain_comm.rank == 0:
            if self.band_comm.rank != 0:
                shapes_a = natoms*[(0, 0)]
                P_ani = {a: np.zeros(shape) for a, shape in enumerate(shapes_a)}
            partition = AtomPartition(self.domain_comm, natoms*[0], 'All on root partition')
        else:
            shapes_a = []
            partition = AtomPartition(self.domain_comm, [], 'Empty partition')

        self._P_ani = ArrayDict(partition, shapes_a, d=P_ani)
        self._gather_P_ani = self._P_ani

    def __exit__(self, exc_type, exc_value, tb):
        self.reader.close()

    @property
    def C_nM(self):
        return self._C_nM

    @property
    def P_ani(self) -> ArrayDict:
        return self._P_ani

    @property
    def dtype(self) -> np.dtype:
        return self._dtype

    @property
    def nn(self) -> int:
        return self._nn

    @property
    def nM(self) -> int:
        return self._nM

    def __iter__(self) -> Iterator[NDArray[np.float64]]:
        for i in range(len(self)):
            if self.domain_comm.rank == 0:
                if self.band_comm.rank == 0:
                    weight_MM = self.reader.proxy('weight_iMM', i)[:]
                else:
                    weight_MM = np.zeros((self.nM, self.nM), float)
                self.band_comm.broadcast(weight_MM, 0)
            else:
                weight_MM = np.zeros((self.nM, self.nM), float)

            yield weight_MM

    def _prepare_P(self):
        pass

    def _prepare_C(self):
        dist = (self.comm, ) + suggest_blocking(self.nn, self.comm.size)
        dist_C_nM = Matrix(self.nn, self.nM, dtype=self.dtype, dist=dist)
        serial_C_nM = Matrix(self.nn, self.nM, dtype=self.dtype,
                             dist=(self.comm, 1, 1, None), data=self.C_nM)
        serial_C_nM.redist(dist_C_nM)
        self._dist_C_nM = dist_C_nM

        self.log('Done distributing', rank=0)

    @property
    def band_comm(self) -> Communicator:
        if self._comm_is_domain:
            return SerialCommunicator()  # type: ignore
        else:
            return self.comm

    @property
    def domain_comm(self) -> Communicator:
        if self._comm_is_domain:
            return self.comm
        else:
            return SerialCommunicator()  # type: ignore

    @property
    def saved_fields(self) -> dict[str, Any]:
        data = {key: getattr(self.reader, key) for key in self.reader.keys()
                if key not in ['weight_iMM', 'atom_projections',
                               'dS_aii', 'P_ani', 'C_nM']}

        return data


class VoronoiWeightCalculator(VoronoiWeights):

    r"""Calculates KS wave function overlaps under operator :math:`\hat{w}`
    using LCAO basis function overlaps and PAW corrections.

    .. math::

        W_{nn'}
        = \left<\psi_n | \hat{w} | \psi_{n'}\right>
        = \left<\tilde{\psi}_n | \hat{T}^\dagger \hat{w} \hat{T} | \tilde{\psi}_{n'}\right>
        = \left<\tilde{\psi}_n | \hat{w} | \tilde{\psi}_{n'}\right>
        + \sum_{aij} \left<\tilde{\psi}_n | \tilde{p}_i^a\right>
        \Delta S_{ij}^a \left<\tilde{p}_i^a | \tilde{\psi}_{n'}\right>

    where the operator :math:`\hat{w} = w(\vec{r})` is 1 in the
    Voronoi region of atoms :attr:`proj_atoms` and 0 outside.

    The sum over atoms is restricted to atoms in the region :math:`w(\vec{r}) = 1`.

    :math:`\hat{T}` is the PAW transformation operator.

    Parameters
    ----------
    voronoi_lcao_gen
        Object that calculates or loads the LCAO weights from file
    use_pblas
        Whether PBLAS/ScaLAPACK should be used (more efficient parallelization)

    """

    _voronoi_lcao_gen: VoronoiLCAOWeights

    def __init__(self,
                 voronoi_lcao_gen: VoronoiLCAOWeights,
                 use_pblas: bool = False):
        assert isinstance(voronoi_lcao_gen, VoronoiLCAOWeights)
        self._voronoi_lcao_gen = voronoi_lcao_gen

        self._log = self.voronoi_lcao_gen.log
        self.use_pblas = use_pblas

        if not use_pblas:
            assert self.band_comm.size == 1, 'Only domain parallelization allowed when not using PBLAS'

        self.log('Start', rank=0, flush=True)

    def __iter__(self) -> Iterator[NDArray[np.float64] | None]:
        """ Yields weights in KS basis. """
        for proj_atoms, weight_MM in zip(self.atom_projections, self.voronoi_lcao_gen):
            if self.use_pblas:
                yield self.calculate_weight_nn_pblas(proj_atoms, weight_MM)
            else:
                self.voronoi_lcao_gen.gather_P_ani  # Needs to be called by all domains to be gathered
                yield self.calculate_weight_nn(proj_atoms, weight_MM)

    def calculate_weight_nn_pblas(self,
                                  proj_atoms: list[int] | NDArray[np.float64],
                                  weight_MM: NDArray[np.float64] | None,
                                  out: NDArray[np.float64] | None = None) -> NDArray[np.float64] | None:
        r""" Calculates weights using PBLAS.

        Parameters
        ----------
        proj_atoms
            Do the Voronoi decomposition for these atoms
        weight_MM
            The weights in LCAO without PAW corrections.

            The weights should be summed to the rank 0 of the domain communicator
            The weights on other ranks than 0 on the band communicator are ignored
            (they should be identical on all ranks)
        out
            If this is specified the result is written to here on rank 0

        Returns
        -------
            The matrix elements :math:`W_{nn'}` on root and ``None`` on other ranks
        """
        if out is not None and self.comm.rank == 0:
            assert out.shape == (self.nn, self.nn), out.shape

        # Only non-None on comm root
        gather_P_ani = self.voronoi_lcao_gen.gather_P_ani

        if weight_MM is None:
            # It is permissible to let weight_MM be None. Then all projectors
            # must be on the root rank of the domain comm
            assert self.domain_comm.rank != 0, 'Weights must not be None on non-root rank'
            assert gather_P_ani.partition.natoms == 0, gather_P_ani.partition.natoms
            if self.band_comm.rank == 0:
                v_nn = np.zeros((self.nn, self.nn), dtype=self.dtype)
        else:
            # Perform the transformation to KS basis only on domain comms where
            # weight_MM is not None

            if self.band_comm.rank != 0:
                # Weights should be identical over the entire band communicator
                weight_MM = np.zeros((0, 0))

            dist = self.voronoi_lcao_gen.dist

            # redistribute the overlaps into block cyclic form
            serial_vt_MM: Matrix | None
            serial_vt_MM = Matrix(self.nM, self.nM, dtype=float,
                                  dist=(self.band_comm, 1, 1, None), data=weight_MM)
            dist_vt_MM = Matrix(self.nM, self.nM, dtype=float,
                                dist=(self.band_comm, dist.rows, dist.columns, dist.blocksize))
            serial_vt_MM.redist(dist_vt_MM)
            serial_vt_MM = None
            weight_MM = None

            if self.band_comm.rank == 0:
                self.log('Distributed vt_MM')

            # Transform into KS basis
            vt_nn = Matrix(self.nn, self.nn, dtype=float,
                           dist=(self.band_comm, dist.rows, dist.columns, dist.blocksize))
            calc_vt_nn_pblas(self.voronoi_lcao_gen.dist_C_nM, dist_vt_MM, vt_nn)
            if self.band_comm.rank == 0:
                self.log('Calculated vt_nn in parallel')

            # redistribute the v_nn matric to serial again
            serial_vt_nn = Matrix(self.nn, self.nn, dtype=float, dist=(self.band_comm, 1, 1, None))
            vt_nn.redist(serial_vt_nn)
            v_nn = serial_vt_nn.array
            if self.band_comm.rank == 0:
                self.log('Distributed vt_nn', rank=0)

        if self.band_comm.rank == 0:
            calc_correction(proj_atoms, gather_P_ani,
                            self.voronoi_lcao_gen.dS_aii, self.nn, out=v_nn)
            self.domain_comm.sum(v_nn)
            self.log('Calculated correction', rank=0)

        if self.comm.rank == 0:
            if out is not None:
                out[:] = v_nn
            return v_nn
        else:
            return None

    def calculate_weight_nn(self,
                            proj_atoms: list[int] | NDArray[np.float64],
                            weight_MM: NDArray[np.float64] | None,
                            out: NDArray[np.float64] | None = None) -> NDArray[np.float64] | None:
        r""" Calculates weights.

        Parameters
        ----------
        proj_atoms
            Do the Voronoi decomposition for these atoms
        weight_MM
            The weights in LCAO without PAW corrections
        out
            If this is specified the result is written to here on rank 0

        Returns
        -------
            The matrix elements :math:`W_{nn'}` on root and ``None`` on other ranks
        """
        if out is not None and self.comm.rank == 0:
            assert out.shape == (self.nn, self.nn), out.shape

        gather_P_ani = self.voronoi_lcao_gen.gather_P_ani
        if weight_MM is None:
            # It is permissible to let weight_MM be None. Then all projectors
            # must be on the root rank of the domain comm
            assert self.comm.rank != 0, 'Weights must not be None on non-root rank'
            assert gather_P_ani.partition.natoms == 0, gather_P_ani.partition.natoms
            v_nn = np.zeros((self.nn, self.nn), dtype=self.dtype)
        else:
            # Since we assume that all parallelization is over the domain
            # C_nM is only distributed over domain
            v_nn = calc_vt_nn(self.voronoi_lcao_gen.C_nM, weight_MM)

        calc_correction(proj_atoms, gather_P_ani,
                        self.voronoi_lcao_gen.dS_aii, self.nn, out=v_nn)
        self.domain_comm.sum(v_nn)

        if self.comm.rank == 0:
            if out is not None:
                out[:] = v_nn
            return v_nn
        else:
            return None

    @property
    def voronoi_lcao_gen(self) -> VoronoiLCAOWeights:
        return self._voronoi_lcao_gen

    @property
    def atom_projections(self) -> AtomProjectionsType:
        return self.voronoi_lcao_gen.atom_projections

    @property
    def nn(self) -> int:
        return self.voronoi_lcao_gen.nn

    @property
    def dtype(self) -> np.dtype:
        return self.voronoi_lcao_gen.dtype

    @property
    def nM(self) -> int:
        return self.voronoi_lcao_gen.nM

    @property
    def comm(self) -> Communicator:
        return self.voronoi_lcao_gen.comm

    @property
    def band_comm(self) -> Communicator:
        return self.voronoi_lcao_gen.band_comm

    @property
    def domain_comm(self) -> Communicator:
        return self.voronoi_lcao_gen.domain_comm

    @property
    def saved_fields(self) -> dict[str, Any]:
        return dict()


class VoronoiLCAOWeightCalculator(VoronoiLCAOWeights):

    r"""Loads Voronoi grid and calculates Voronoi weights from ground state file
    using LCAO basis function overlaps and PAW corrections.

    .. math::

        W_{nn'}
        = \left<\psi_n|\hat{w}|\psi_{n'}\right>
        = \int w(\vec{r}) \psi_n^*(\vec{r}) \psi_{n'}(\vec{r}) d\vec{r}

    where the operator :math:`\hat{w} = w(\vec{r})` is 1 in the
    Voronoi region of the atomic projections and 0 outside.

    Parameters
    ----------
    atom_projections
        List of atom groups (length ``Ni``). Each atom group is a list of integers (of any length)
    gpw_file
        Filename of GPAW ground state file

    """

    _big_a_G: NDArray[np.int_] | None
    _a_G: NDArray[np.int_] | None
    _calc: GPAWCalculator

    def __init__(self,
                 atom_projections: AtomProjectionsType,
                 gpw_file: str,
                 voronoi_grid_file: str | None = None,
                 recalculate_grid: bool = False,
                 domain: int = -1,
                 use_pblas: bool = False,
                 comm=None):
        assert all([isinstance(proj_atoms, list) or isinstance(proj_atoms, np.ndarray)
                    for proj_atoms in atom_projections])
        self._atom_projections = atom_projections

        if comm is None:
            comm = world

        self._comm = comm
        self._log = Logger(comm=comm)

        self.log('Start', rank=0, flush=True)

        if domain == -1:
            domain = self.comm.size

        calc = GPAW(gpw_file, txt=None, communicator=self.comm, parallel={'domain': domain})
        calc.initialize_positions()
        self._calc = calc

        self._dS_aii = {a: setup.dO_ii for a, setup in enumerate(calc.wfs.setups)}  # Same data on all ranks
        self._proj = self.calc.wfs.kpt_u[0].projections.toarraydict()

        # Load or calculate (and optionally save) Voronoi grid
        if recalculate_grid or voronoi_grid_file is None:
            self.log('compute a_g', rank=0, flush=True)
            big_a_G = calculate_a_g(fine_grid=False, calc=calc)
            if self.comm.rank == 0:
                if voronoi_grid_file is not None:
                    if voronoi_grid_file[-4:] == '.npz':
                        np.savez_compressed(voronoi_grid_file, a_G=big_a_G)
                    else:
                        np.save(voronoi_grid_file, big_a_G)
            self.log('Computed Voronoi decomposition grid', rank=0, flush=True)
        else:
            if self.comm.rank == 0:
                if voronoi_grid_file[-4:] == '.npz':
                    files = np.load(voronoi_grid_file)
                    big_a_G = files['a_G']
                else:
                    big_a_G = np.load(voronoi_grid_file)
            else:
                big_a_G = None
            self.log('Loaded Voronoi decomposition grid', rank=0, flush=True)

        self._big_a_G = big_a_G
        self._a_G = None

    @property
    def dtype(self) -> np.dtype:
        """ Global number of bands """
        return self.C_nM.dtype

    @property
    def nn(self) -> int:
        """ Global number of bands """
        return self.calc.wfs.bd.nbands

    @property
    def nM(self) -> int:
        """ Global number of bands """
        return self.C_nM.shape[1]

    @property
    def calc(self) -> GPAWCalculator:
        return self._calc

    @property
    def C_nM(self):
        return self.calc.wfs.kpt_u[0].C_nM

    @property
    def P_ani(self):
        return self.calc.wfs.kpt_u[0].P_ani

    def _prepare_P(self):
        self._gather_P_ani_on_band_comm_root()

    def _gather_P_on_comm_root(self):
        # Do not use this one
        self.log('Gather P_ani to comm root', rank=0)

        gather_P_ani = proj_as_dict_on_master(self.calc.wfs.kpt_u[0].projections, 0, self.nn)

        if self.comm.rank != 0:
            gather_P_ani = None

        self._gather_P_ani = gather_P_ani
        self.log('Done gathering', rank=0)

    def _gather_P_ani_on_band_comm_root(self):
        self.log('Gather P_ani', rank=0)

        proj = self.calc.wfs.kpt_u[0].projections
        serial_proj = proj.new(bcomm=None)
        proj.matrix.redist(serial_proj.matrix)
        if self.band_comm.rank == 0:
            gather_P_ani = serial_proj.toarraydict()
        else:
            # Array dict with dimension n == 0
            shape = proj.myshape[:-2] + (0, )
            shapes = [shape + (nproj,) for nproj in proj.nproj_a]
            gather_P_ani = proj.atom_partition.arraydict(shapes, proj.matrix.array.dtype)

        self._gather_P_ani = gather_P_ani
        self.log('Done gathering', rank=0)

    def _prepare_C(self):
        # mynn is the number of bands on this rank
        mynn = len(self.C_nM)
        maxlocalnn = (self.nn + self.band_comm.size - 1) // self.band_comm.size
        assert mynn <= maxlocalnn

        # Distribute the LCAO coefficients and projectors into block cyclic form
        self.log('Distribute C_nM and P_ani', rank=0)
        dist_C_nM = redistribute_LCAO_into_block_cyclic_form(self.C_nM, self.nn, self.band_comm)

        self._dist_C_nM = dist_C_nM
        self.log('Done distributing', rank=0)

    @property
    def big_a_G(self):
        return self._big_a_G

    @property
    def a_G(self):
        """ Returns the voronoi decomposition on the coarse grid, distributed over domain_comm

        If this quantity is not stored, the voronoi decomposition on the master rank is distributed
        """

        if self._a_G is None:
            self.distribute_a_G()

        return self._a_G

    def distribute_a_G(self):
        """ Distribute the voronoi decomposition on the coarse grid over domain_comm

        Afterwards delete the non-distributed array
        """

        domain_comm = self.domain_comm
        gd = self.calc.density.gd

        if domain_comm.rank == 0:
            assert self.big_a_G is not None, \
                'Full Voronoi grid must be given on rank 0 if distributed grid is not given'
            assert self.big_a_G.dtype == np.int16

        # Now distribute to other domain ranks
        a_G = gd.zeros(dtype=np.int16)
        gd.distribute(self.big_a_G, a_G)
        self._a_G = a_G
        self._big_a_G = None

    def __iter__(self) -> Iterator[NDArray[np.float64]]:
        """ Yields weights in LCAO basis. """

        for proj_atoms in self.atom_projections:
            # assert isinstance(proj_atoms, list) or isinstance(proj_atoms, np.ndarray)

            weight_MM = self.calculate_voronoi_weights_LCAO_only(proj_atoms)
            self.log(f'Computed LCAO weights for projection {proj_atoms}', rank=0, flush=True)

            yield weight_MM

    def calculate_voronoi_weights_LCAO_only(self,
                                            proj_atoms: list[int] | NDArray[np.float64],
                                            out: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
        if out is not None:
            assert out.shape == (self.nM, self.nM), out.shape

        w_G = np.where(np.isin(self.a_G, proj_atoms), 1.0, 0.0)
        v_MM = calc_vt_MM(self.calc, w_G)

        if out is not None:
            out[:] = v_MM
        return v_MM

    @property
    def domain_comm(self) -> Communicator:
        return self.calc.comms['d']

    @property
    def band_comm(self) -> Communicator:
        return self.calc.comms['b']

    @property
    def saved_fields(self) -> dict[str, Any]:
        return dict()


def calculate_a_g(gpw_file: str | None = None,
                  fine_grid: bool = True,
                  calc: GPAWCalculator | None = None):
    """Calculate Voronoi grid

    Parameters
    ----------
    gpw_file
        Filename of ground state file. Ignored if calc is not None
    calc
        Initialized GPAW calculator
    fine_grid
        True if Voronoi grid on fine grid should be calculated, False if on coarse

    Returns
    -------
    Voronoi grid as nx,ny,nz array
    """
    calc_comm = world

    if calc is None:
        calc = GPAW(gpw_file, txt='/dev/null', communicator=calc_comm,
                    parallel={'domain': calc_comm.size})
        calc.initialize_positions()

    atoms = calc.get_atoms()
    if fine_grid:
        gd = calc.density.finegd
    else:
        gd = calc.density.gd
    a_g = wignerseitz(gd, atoms)
    a_g = a_g.astype(np.int16)  # Storing as 16 bit integers reduces file size significantly

    big_g = gd.collect(a_g)

    return big_g


def calc_vt_MM(calc: GPAWCalculator,
               w_G: NDArray[np.float64]) -> NDArray[np.float64]:
    r""" Calculate LCAO basis function overlaps.

    .. math::

        \tilde{v}_{\mu\nu}
        = \left<\tilde{\phi}_{\mu} | \hat{w} | \tilde{\phi}_{\nu}\right>
        = \int w(\vec{r}) \tilde{\phi}_{\mu}^*(\vec{r}) \tilde{\phi}_{\nu}(\vec{r}) d\vec{r}

    Parameters
    ----------
    calc
        GPAW calculator object.
    w_G
        Operator w in real space (distributed on the domain of each rank). Should be
        0 or 1 in each grid point.

    Returns
    -------
        The contribution to :math:`\tilde{v}_{\mu\nu}` from this domain
    """
    vt_MM = calc.wfs.basis_functions.calculate_potential_matrices(w_G)[0]
    tri2full(vt_MM)

    return vt_MM


def calc_vt_nn(C_nM: NDArray[np.float64],
               vt_MM: NDArray[np.float64]) -> NDArray[np.float64]:
    r""" Calculate pseudo KS wave function overlaps from LCAO overlaps.

    .. math::

        \widetilde{W}_{nn'}
        = \left<\tilde{\psi}_n | \hat{w} | \tilde{\psi}_{n'}\right>
        = \sum_{\mu\nu} C_{\mu n}^* C_{\nu n'} \left<\tilde{\phi}_{\mu} | \hat{w} | \tilde{\phi}_{\nu}\right>
        = \sum_{\mu\nu} C_{\mu n}^* C_{\nu n'} \tilde{v}_{\mu\nu}

    Parameters
    ----------
    C_nM
        The (transposed) LCAO coefficients :math:`C_{\mu n}`
    vt_MM
        The contribution to :math:`\tilde{v}_{\mu\nu}` on domain

    Returns
    -------
    The contribution to :math:`\widetilde{W}_{nn'}` on this domain
    """
    Wt_nn = C_nM @ vt_MM @ C_nM.T

    return Wt_nn


def calc_vt_nn_pblas(dist_C_nM,
                     dist_vt_MM,
                     dist_vt_nn):
    r""" See :func:`calc_vt_nn`.

    Parameters
    ----------
    dist_C_nM
        LCAO coefficients, in block cyclic form
    dist_vt_MM
        The contribution to :math:\tilde{v}_{\mu\nu}` on domain, in block cyclic form
    dist_vt_nn
        Buffer in block cyclic form, into which the contribution to
        :math:`\widetilde{W}_{nn}` on this domain will be written
    """
    dist_buf_nM = dist_C_nM.new()

    # buf_nM <- C_nM @ vt_MM
    dist_C_nM.dist.multiply(1.0, dist_C_nM, 'N', dist_vt_MM, 'N', 0.0, dist_buf_nM, symmetric=False)

    # v_nn <- buf_nM @ C_nM.T
    dist_C_nM.dist.multiply(1.0, dist_buf_nM, 'N', dist_C_nM, 'T', 0.0, dist_vt_nn, symmetric=False)


def calc_correction(correction_on_atoms: list[int] | NDArray[np.float64],
                    P_ani: dict[int, NDArray[np.float64]] | ArrayDict,
                    dS_aii: dict[int, NDArray[np.float64]],
                    Nn: int,
                    out: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
    r"""
    Calculate the PAW correction to KS wave function overlaps on this domain.

    .. math::

        c_{nn'}
        = \sum_a \left<\tilde{\psi}_n | \tilde{p}_i^a\right>
        \Delta S_{ij}^a \left<\tilde{p}_j^a | \tilde{\psi}_{n'}\right>,

    where the sum over atoms only includes a selection of atoms.

    Parameters
    ----------
    correction_on_atoms
        Which atoms to loop over
    P_ani
        The matrix of projectors :math:`\left<\tilde{p}_i^a | \tilde{\psi}_{n}\right>`
    dS_aii
        :math:`\Delta S_{ij}^a`
    Nn
        Global number of bands
    out
        If this is specified the result is appended to here

    Returns
    -------
        :math:`c_{nn'}'`
    """
    if out is None:
        corr_nn = np.zeros((Nn, Nn))
    else:
        assert out.shape == (Nn, Nn)
        corr_nn = out

    for a in P_ani.keys():
        if a not in correction_on_atoms:
            continue
        corr_nn += P_ani[a] @ dS_aii[a] @ P_ani[a].T

    return corr_nn
