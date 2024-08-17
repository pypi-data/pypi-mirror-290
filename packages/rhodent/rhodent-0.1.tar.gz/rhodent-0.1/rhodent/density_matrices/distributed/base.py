from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator, Generic, NamedTuple, Iterable
from itertools import zip_longest

import numpy as np
from numpy._typing import _DTypeLike as DTypeLike  # parametrizable wrt generic

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

from ..buffer import DensityMatrixBuffer
from ...utils import DTypeT, Logger, concatenate_indices
from ...typing import Communicator


class RhoIndices(NamedTuple):

    s: int
    k: int
    n1: slice
    n2: slice

    @staticmethod
    def concatenate_indices(indices_list: Iterable[RhoIndices],
                            ) -> tuple[RhoIndices, list[RhoIndices]]:
        indices_list = list(indices_list)
        assert len(indices_list) > 0
        s, k = indices_list[0][:2]
        assert all(indices.s == s for indices in indices_list), f'All s must be identical {indices_list}'
        assert all(indices.k == k for indices in indices_list), f'All k must be identical {indices_list}'

        _indices_concat, _reduced_indices_list = concatenate_indices(
            [(indices.n1, indices.n2) for indices in indices_list])
        indices_concat = RhoIndices(s, k, *_indices_concat)
        reduced_indices_list = [RhoIndices(s, k, *indices) for indices in _reduced_indices_list]

        return indices_concat, reduced_indices_list


class BaseDistributor(ABC, Generic[DTypeT]):

    """ Distribute density matrices over time, frequency or other dimensions across MPI ranks
    """

    def __init__(self,
                 nnshape: tuple[int, int],
                 xshape: tuple[int, ...],
                 dtype: DTypeLike[DTypeT],
                 datadesc: str,
                 derivative_order_s: list[int] = [0]):
        assert all(order in [0, 1, 2] for order in derivative_order_s)
        assert all(np.diff(derivative_order_s) > 0), 'Derivative orders must be strictly increasing'

        self.nnshape = nnshape
        self.xshape = xshape
        self._dtype = np.dtype(dtype)
        self.datadesc = datadesc
        self.derivative_order_s = derivative_order_s

    @property
    def dtype(self) -> np.dtype[DTypeT]:
        """ Dtype of the buffers """
        return self._dtype

    @property
    @abstractmethod
    def ksd(self) -> KohnShamDecomposition:
        raise NotImplementedError

    @property
    @abstractmethod
    def comm(self) -> Communicator:
        raise NotImplementedError

    @property
    @abstractmethod
    def yield_re(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def yield_im(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def log(self) -> Logger:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Generator[DensityMatrixBuffer, None, None]:
        """ Yield density matrices in parts. Different data is
        yielded on different ranks

        Yields
        ------
        Part of the density matrix
        """
        raise NotImplementedError

    def work_loop(self,
                  rank: int) -> Generator[RhoIndices | None, None, None]:
        """ Like work_loop_by_rank but for one particular rank
        """
        for chunks_r in self.work_loop_by_ranks():
            yield chunks_r[rank]

    def global_work_loop(self) -> Generator[RhoIndices, None, None]:
        for chunks_r in self.work_loop_by_ranks():
            for chunk in chunks_r:
                if chunk is None:
                    continue
                yield chunk

    def describe_reim(self) -> str:
        if self.yield_re and self.yield_im:
            return 'Real and imaginary parts'
        elif self.yield_re:
            return 'Real part'
        else:
            return 'Imaginary part'

    def describe_derivatives(self) -> str:
        return 'derivative orders: ' + ', '.join([str(d) for d in self.derivative_order_s])

    @abstractmethod
    def work_loop_by_ranks(self) -> Generator[list[RhoIndices | None], None, None]:
        """ Yield slice objects corresponding to the chunk of the density matrix
        that is gathered on each rank.

        New indices are yielded until the entire density matrix is processed
        (across all ranks).

        Yields
        ------
        List of slice objects corresponding to part of the density matrix
        yielded on each ranks.  None in place of the slice object if there is
        nothing yielded for that rank.
        """
        raise NotImplementedError

    def gather_on_root(self) -> Generator[DensityMatrixBuffer | None, None, None]:
        for indices_r, dm_buffer in zip_longest(self.work_loop_by_ranks(),
                                                self, fillvalue=None):
            assert indices_r is not None, 'Work loop shorter than work'

            # Yield root's own work
            if self.comm.rank == 0:
                assert indices_r[0] is not None
                assert dm_buffer is not None
                dm_buffer.ensure_contiguous_buffers()

                yield dm_buffer.copy()
            else:
                yield None

            # Yield the work of non-root
            for recvrank, recvindices in enumerate(indices_r[1:], start=1):
                if recvindices is None:
                    # No work on this recvrank
                    continue

                if self.comm.rank == 0:
                    # Receive work
                    assert dm_buffer is not None
                    dm_buffer.recv_arrays(self.comm, recvrank, log=self.log)
                    yield dm_buffer.copy()
                else:
                    # Send work to root if there is any
                    if self.comm.rank == recvrank:
                        assert dm_buffer is not None
                        dm_buffer.send_arrays(self.comm, 0, log=self.log)
                    yield None

    def collect_on_root(self) -> DensityMatrixBuffer | None:
        full_dm = DensityMatrixBuffer(self.nnshape, self.xshape, dtype=self.dtype)
        full_dm.zero_buffers(real=self.yield_re, imag=self.yield_im, derivative_order_s=self.derivative_order_s)

        for indices, dm_buffer in zip_longest(self.global_work_loop(),
                                              self.gather_on_root(), fillvalue=None):
            if self.comm.rank != 0:
                continue

            assert indices is not None, 'Iterators must be same length'
            assert dm_buffer is not None, 'Iterators must be same length'

            s, k, n1, n2 = indices
            assert s == 0
            assert k == 0

            for partial_data, full_data in zip(dm_buffer._iter_buffers(), full_dm._iter_buffers()):
                _nn1, _nn2 = full_data[n1, n2].shape[:2]
                # Numpy struggles with the static type below
                full_data[n1, n2, :] += partial_data[:_nn1, :_nn2:]  # type: ignore
            self.log(f'Read {self.datadesc} array_nn[{s},{k},{n1},{n2}].', flush=True)

        if self.comm.rank != 0:
            return None

        return full_dm
