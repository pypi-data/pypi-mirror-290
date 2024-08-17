from __future__ import annotations

from typing import Generator, NamedTuple
from itertools import product
import numpy as np
from numpy.typing import NDArray

from gpaw.mpi import world
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

from rhodent.density_matrices.buffer import DensityMatrixBuffer
from rhodent.density_matrices.readers.gpaw import KohnShamRhoWfsReader
from rhodent.utils import Logger, safe_fill
from .base import BaseDistributor, RhoIndices
from ...typing import Communicator


def get_default_parameters(comm=None,
                           nn1: int | None = None,
                           nn2: int | None = None) -> dict[str, int]:
    stride_opts = dict(striden1=100, striden2=100)
    if comm is None:
        comm = world
    if nn1 is not None:
        maxn = (nn1 + comm.size - 1) // ((comm.size+1) // 2)
        if stride_opts['striden1'] > maxn:
            stride_opts['striden1'] = maxn
    if nn2 is not None:
        maxn = (nn2 + comm.size - 1) // ((comm.size+1) // 2)
        if stride_opts['striden2'] > maxn:
            stride_opts['striden2'] = maxn

    return stride_opts


class TimeDistributor(BaseDistributor):

    """ Iteratively read density matrices in the time domain

    This class uses the KohnShamRhoWfsReader to iteratively read wave functions
    (each rank reading the same times) and construct density matrices in the ground state
    Kohn-Sham basis for each time. The different ranks are reading different chunks of
    the density matrices. The density matrices are accumulated in a buffer and yielded
    when all times have been read.

    Parameters
    ----------
    rho_reader
        Density matrices reader
    comm
        Communicator
    log
        Logger
    """

    def __init__(self,
                 rho_reader: KohnShamRhoWfsReader,
                 comm=world,
                 stride_opts: dict[str, int] | None = None,
                 log: Logger | None = None):
        self.rho_wfs_reader = rho_reader
        self._comm = comm
        if log is None:
            self._log = Logger(comm=self.comm)
        self._ksd = self.rho_wfs_reader.ksd

        if stride_opts is None:
            stride_opts = dict()
        else:
            stride_opts = dict(stride_opts)
        self._parameters = self._prepare_parameters(stride_opts)
        self._nchunks = sum(1 for _ in self.work_loop(self.comm.rank))

        assert self.rho_wfs_reader.comm.size == 1, 'Serial TimeDistributor must have serial reader'
        nnshape = (self._parameters.n1size, self._parameters.n2size)
        xshape = (self.nt, )

        super().__init__(nnshape, xshape, float, '', derivative_order_s=[0])

    def print_work(self):
        if self.comm.rank > 0:
            return
        nwork_r = self.comm.size * [0]
        nchunksperrank = (self.localnchunks + self.comm.size - 1) // self.comm.size
        gen = self.work_loop(self.comm.rank)

        try:
            for localchunk in range(nchunksperrank):
                # Get the next comm.size chunks (or fewer if there are no more left)
                for rank in range(self.comm.size):
                    next(gen)
                    nwork_r[rank] += 1
        except StopIteration:
            pass

        for rank, n in enumerate(nwork_r):
            print(f'      Rank {rank:04.0f}/{self.comm.size:04.0f} has {n} objects to work on', flush=True)

    def global_work_loop(self) -> Generator[RhoIndices, None, None]:
        params = self._parameters
        for s, k, n1, n2 in product(range(params.ns), range(params.nk),
                                    range(0, params.n1size, params.cap_striden1),
                                    range(0, params.n2size, params.cap_striden2)):
            indices = RhoIndices(s=0, k=0,
                                 n1=slice(n1, n1 + params.cap_striden1),
                                 n2=slice(n2, n2 + params.cap_striden2))
            yield indices

    def work_loop_by_ranks(self) -> Generator[list[RhoIndices | None], None, None]:
        gen = self.global_work_loop()

        while True:
            chunks_r: list[RhoIndices | None] = [indices for _, indices
                                                 in zip(range(self.comm.size), gen)]

            remaining = self.comm.size - len(chunks_r)
            if remaining == 0:
                yield chunks_r
            elif remaining == self.comm.size:
                # There is nothing left to do for any rank
                break
            else:
                # Append Nones for the ranks that are not doing anything
                chunks_r += remaining * [None]
                yield chunks_r
                break

    @property
    def localnchunks(self) -> int:
        """ Total number of density matrices this rank will
        work with """
        return self._nchunks

    @property
    def C0S_sknM(self) -> NDArray[np.float64]:
        return self.rho_wfs_reader.C0S_sknM

    @property
    def rho0_sknn(self) -> NDArray[np.float64]:
        return self.rho_wfs_reader.rho0_sknn

    @property
    def ksd(self) -> KohnShamDecomposition:
        return self._ksd

    @property
    def comm(self) -> Communicator:
        return self._comm

    @property
    def dt(self):
        return self.rho_wfs_reader.dt

    @property
    def nt(self):
        return self.rho_wfs_reader.nt

    @property
    def time_t(self):
        return self.rho_wfs_reader.time_t

    @property
    def yield_re(self) -> bool:
        return self.rho_wfs_reader.yield_re

    @property
    def yield_im(self) -> bool:
        return self.rho_wfs_reader.yield_im

    @property
    def log(self) -> Logger:
        return self._log

    def _prepare_parameters(self,
                            stride_opts: dict[str, int] | None = None) -> RhoParameters:
        imin, imax, amin, amax = self.ksd.ialims()
        if stride_opts is None:
            stride_opts = get_default_parameters(nn1=imax - imin + 1, nn2=amax - amin + 1)

        if stride_opts.pop('only_ia', True):
            # Use ialims as defaults
            default_opts = dict()
            default_opts['n1min'], default_opts['n2min'] = imin, amin
            default_opts['n1max'], default_opts['n2max'] = imax, amax
            for key, def_value in default_opts.items():
                if key not in stride_opts:
                    stride_opts[key] = def_value

        ns, nk, nn, _ = self.ksd.reader.proxy('C0_unM', 0).shape

        keys = set(RhoParameters._fields) & stride_opts.keys()
        param_opts = {key: stride_opts.pop(key) for key in keys}
        parameters = RhoParameters(ns=ns, nk=nk, nn=nn, **param_opts)
        return parameters

    def print_description(self):
        pass

    def __iter__(self) -> Generator[DensityMatrixBuffer, None, None]:
        """ Yield density matrices for all times, chunk by chunk

        The wave function file is read in chunks, time by time, with
        the reading of times in the inner loop.

        Yields
        ------
        Chunks of the density matrix
        """
        read_dm = DensityMatrixBuffer(self._parameters.nnshape,
                                      (self.nt, ),
                                      np.float64)
        if self.yield_re:
            read_dm.zeros(True, 0)
        if self.yield_im:
            read_dm.zeros(False, 0)

        self.rho_wfs_reader.parallel_prepare()

        # Loop over the chunks this rank should gather
        for indices in self.work_loop(self.comm.rank):
            if indices is None:
                continue
            # Convert to reading indices
            n1 = slice(self._parameters.n1min + indices.n1.start, self._parameters.n1min + indices.n1.stop)
            n2 = slice(self._parameters.n2min + indices.n2.start, self._parameters.n2min + indices.n2.stop)
            gen = self.rho_wfs_reader.iread(indices.s, indices.k, n1, n2)
            for t in self.rho_wfs_reader.work_loop(self.rho_wfs_reader.comm.rank):
                if t is None:
                    continue
                dm_buffer = next(gen)
                for source_nn, dest_nn in zip(dm_buffer._iter_buffers(), read_dm[t]._iter_buffers()):
                    dest_nn[:] = source_nn

            yield read_dm

    def gather_on_root(self) -> Generator[DensityMatrixBuffer | None, None, None]:
        self.C0S_sknM   # Make sure to read this synchronously
        yield from super().gather_on_root()


class AlltoallvTimeDistributor(TimeDistributor):

    """ Iteratively read density matrices in the time domain

    This class uses the KohnShamRhoWfsReader to iteratively read wave functions
    (one time per rank) and construct density matrices in the ground state Kohn-Sham
    basis for each time. When all ranks have read one time each, this class
    performs a redistribution of data, such that each rank only gets one chunk of the
    density matrices, but for all times. The density matrices are accumulated in a
    buffer and yielded when all times have been read.

    Parameters
    ----------
    rho_reader
        Density matrices reader
    """

    def __init__(self,
                 rho_reader: KohnShamRhoWfsReader,
                 stride_opts: dict[str, int] | None = None):
        self.rho_wfs_reader = rho_reader
        self._comm = self.rho_wfs_reader.comm
        self._log = self.rho_wfs_reader.log
        self._ksd = self.rho_wfs_reader.ksd
        if stride_opts is None:
            stride_opts = dict()
        else:
            stride_opts = dict(stride_opts)
        self._parameters = self._prepare_parameters(stride_opts)
        self._nchunks = sum(1 for _ in self.work_loop(self.comm.rank))

        assert self.rho_wfs_reader.lcao_rho_reader.striden == 0, \
            'n stride must be 0 (index all) for alltoallv parallelized method'

        nnshape = (self._parameters.n1size, self._parameters.n2size)
        xshape = (self.nt, )

        BaseDistributor.__init__(self, nnshape, xshape, float, '', derivative_order_s=[0])

    def print_description(self):
        if self.comm.rank != 0:
            return

        narrays = (2 if self.yield_re and self.yield_im else 1) * len(self.derivative_order_s)

        # Number of iterations needed to read all chunks
        niters = len(list(self.work_loop_by_ranks()))

        # For each chunk: number of iterations needed to read all times
        ntimeiters = len(list(self.rho_wfs_reader.work_loop_by_ranks()))

        # Maximum number of ranks participating in reading of chunks
        for chunks_r in self.work_loop_by_ranks():
            maxnchunks = sum(1 for chunk in chunks_r if chunk is not None)
            break

        # Maximum number of ranks participating in reading of times
        for t_r in self.rho_wfs_reader.work_loop_by_ranks():
            maxntimes = sum(1 for t in t_r if t is not None)
            break

        before_MiB = (np.prod(self._parameters.nnshape + (maxnchunks, )) * maxntimes *
                      np.dtype(float).itemsize / (1024 ** 2)) * narrays
        after_MiB = (np.prod(self._parameters.nnshape + (self.nt, )) * maxnchunks *
                     np.dtype(float).itemsize / (1024 ** 2)) * narrays
        msg = (f'Parallel density matrices reader:\n'
               '=================================\n'
               f'Reading chunks in {niters} iterations.\n'
               f'Reading times in {ntimeiters} iterations.\n'
               f'Up to {maxntimes} ranks reading times and '
               f'{maxnchunks} ranks receiving chunks of the density matrices.\n'
               f'Density matrix buffers:\n'
               f'  Buffers hold {narrays} arrays ({self.describe_reim()})\n'
               f'  Before parallel redistribution - {self._parameters.nnshape + (maxnchunks, )}\n'
               f'  for a size of {before_MiB:.1f}MiB on {maxntimes} ranks\n'
               f'  After parallel redistribution  - {self._parameters.nnshape + (self.nt, )}\n'
               f'  for a size of {after_MiB:.1f}MiB on {maxnchunks} ranks\n'
               f''
               )
        self.log.log(msg, flush=True)

    def __iter__(self) -> Generator[DensityMatrixBuffer, None, None]:
        """ Yield density matrices for all times, chunk by chunk

        The wave function file is read in chunks, time by time. However,
        chunks are grouped together so that the density matrix at each
        time is read in large chunks. Each rank reads the same chunk for
        a different time. Then, the chunks and times are redistributed,
        so that each rank now holds a small chunk, but for many times.
        The same chunk is read for all times before it is yielded.

        Yields
        ------
        Chunks of the density matrix
        """
        log = self.log

        # Number of iterations needed to read all chunks
        niters = len(list(self.work_loop_by_ranks()))

        # Maximum number of ranks participating in reading of times
        for t_r in self.rho_wfs_reader.work_loop_by_ranks():
            maxntimes = sum(1 for t in t_r if t is not None)
            break

        self.rho_wfs_reader.parallel_prepare()

        # Here x is a compound index for a slice of both n and M
        for chunki, chunks_r in enumerate(self.work_loop_by_ranks()):
            log.start('read_alltoallv')

            # The work this rank is supposed to read
            indices = chunks_r[self.comm.rank]
            indices_by_rank = [chunk for chunk in chunks_r if chunk is not None]

            # Number of chunks of nn-indices being read
            nchunks = len(indices_by_rank)
            assert nchunks > 0

            # Find out how much of the total density matrix need to be read to get only
            # the required chunks
            indices_concat, reduced_indices_by_rank = RhoIndices.concatenate_indices(indices_by_rank)

            if indices is None:
                # This rank does not want any slices of n1 and n2.
                # It will still potentially participate in the parallel reading of times
                assert self.comm.rank >= nchunks

            n1 = slice(self._parameters.n1min + indices_concat.n1.start,
                       self._parameters.n1min + indices_concat.n1.stop)
            n2 = slice(self._parameters.n2min + indices_concat.n2.start,
                       self._parameters.n2min + indices_concat.n2.stop)

            if self.comm.rank < maxntimes:
                # This rank will read
                contiguous_chunks_buffer = DensityMatrixBuffer(self._parameters.nnshape,
                                                               (nchunks, ),
                                                               np.float64)
            else:
                # This rank does not read any times
                contiguous_chunks_buffer = DensityMatrixBuffer(self._parameters.nnshape,
                                                               (0, ),
                                                               np.float64)
            if self.comm.rank < nchunks:
                # This rank will get a chunk of the density matrices after redistribution
                contiguous_time_buffer = DensityMatrixBuffer(self._parameters.nnshape,
                                                             (self.nt, ),
                                                             np.float64)
            else:
                contiguous_time_buffer = DensityMatrixBuffer(self._parameters.nnshape,
                                                             (0, ),
                                                             np.float64)
            if self.yield_re:
                contiguous_chunks_buffer.zeros(True, 0)
                contiguous_time_buffer.zeros(True, 0)
            if self.yield_im:
                contiguous_chunks_buffer.zeros(False, 0)
                contiguous_time_buffer.zeros(False, 0)

            gen = self.rho_wfs_reader.iread(indices_concat.s, indices_concat.k, n1, n2)

            for t_r in self.rho_wfs_reader.work_loop_by_ranks():
                # Number of times being read
                ntimes = sum(1 for t in t_r if t is not None)
                # Time index this rank is reading, or None if not reading
                globalt = t_r[self.comm.rank]

                # Read the density matrices for one time per rank,
                # with each rank reading a large chunk of the density matrix
                if globalt is not None:
                    read_dm = next(gen)

                    for recvrank, readindices in enumerate(reduced_indices_by_rank):
                        for source_nn, dest_nn in zip(read_dm._iter_buffers(),
                                                      contiguous_chunks_buffer[recvrank]._iter_buffers()):
                            safe_fill(dest_nn, source_nn[readindices.n1, readindices.n2])
                else:
                    # This rank actually has no time to read (number of times
                    # is not evenly divisible by number of ranks, and this rank
                    # is trying to read past the end)
                    # This rank will still participate in the alltoallv operation
                    assert self.comm.rank >= ntimes

                # Perform the redistributions, so that each rank now holds
                # a smaller chunk of the density matrix, but for many times.
                contiguous_chunks_buffer.redistribute(
                        contiguous_time_buffer, comm=self.comm,
                        source_indices_r=[(r, ) if r < nchunks else None for r in range(self.comm.size)],
                        target_indices_r=[None if t is None else (t, ) for t in t_r],
                        log=log if 0 in t_r else None)

            if self.comm.rank == 0:
                log.log(f'Chunk {chunki+1}/{niters}: Read and distributed density matrices in '
                        f'{log.elapsed("read_alltoallv"):.1f}s', flush=True)

            if indices is not None:
                yield contiguous_time_buffer


class RhoParameters(NamedTuple):

    """ Class to hold the parameters for TimeDistributor

    """

    ns: int
    nk: int
    nn: int
    n1min: int = 0
    n1max: int = -1
    n2min: int = 0
    n2max: int = -1
    striden1: int = 4
    striden2: int = 4

    @property
    def full_nnshape(self) -> tuple[int, int]:
        return (self.n1size, self.n2size)

    @property
    def nnshape(self) -> tuple[int, int]:
        return (self.cap_striden1, self.cap_striden2)

    @property
    def cap_striden1(self) -> int:
        return min(self.striden1, self.n1size)

    @property
    def cap_striden2(self) -> int:
        return min(self.striden2, self.n2size)

    @property
    def true_n1max(self) -> int:
        if self.n1max < 0:
            return self.n1max + self.nn
        return self.n1max

    @property
    def true_n2max(self) -> int:
        if self.n2max < 0:
            return self.n2max + self.nn
        return self.n2max

    @property
    def n1size(self) -> int:
        return self.true_n1max + 1 - self.n1min

    @property
    def n2size(self) -> int:
        return self.true_n2max + 1 - self.n2min
