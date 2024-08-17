from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from gpaw.mpi import broadcast, world
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition

from ..utils import ArrayIsOnRootRank, DistributedArray


class DensityMatrix:

    """ Wrapper for the density matrix in the Kohn-Sham basis at one moment
    in time or at one frequency.

    The plain density matrix and/or derivatives thereof may be stored.

    Parameters
    ----------
    ksd
        KohnShamDecomposition object
    data_is_ravelled
        Whether the data is stored in a ravelled form (single index :math:`p` for electron-hole pairs)
        or not (two indices :math:`ia` for hole and electron).
    matrices
        Dictionary mapping derivative orders (0, 1, 2) for zeroth,
        first, second derivative, .. to file names where density matrices
        are stored.
    """

    def __init__(self,
                 ksd: KohnShamDecomposition,
                 matrices: dict[int, NDArray[np.complex64] | None],
                 data_is_ravelled: bool = True):
        self._ksd = ksd
        self._data_is_ravelled = data_is_ravelled
        self._f_ia: DistributedArray | None = None
        self._rho_ia_derivatives: dict[int, DistributedArray] = dict()
        self._rho_p_derivatives: dict[int, DistributedArray] = dict()
        self.derivative_desc = {0: 'Plain DM', 1: '1st DM derivative', 2: '2nd DM derivative'}

        # Pick the right array depending on whether ravelled p index (rho_p)
        # or two-dimensional ia index (rho_ia) is provided
        array = self._rho_p_derivatives if data_is_ravelled else self._rho_ia_derivatives
        for derivative, rho in matrices.items():
            assert isinstance(derivative, int)
            if self.rank == 0:
                assert isinstance(rho, np.ndarray), rho
                array[derivative] = rho
            else:
                assert rho is None
                array[derivative] = ArrayIsOnRootRank()

    @property
    def ksd(self) -> KohnShamDecomposition:
        """ Kohn-Sham decomposition object """
        return self._ksd

    @property
    def rank(self) -> int:
        """ MPI rank of the ksd object """
        if not hasattr(self.ksd, 'comm'):
            return 0
        return self.ksd.comm.rank

    @property
    def f_p(self) -> DistributedArray:
        """ Occupation number difference :math:`f_p`

        In ravelled form (common index :math:`p` for electron-hole pairs).
        """
        return self.ksd.f_p

    @property
    def f_ia(self) -> DistributedArray:
        """ Occupation number difference :math:`f_{ia}`

        In non-ravelled form (indices :math:`ia` for electron-hole pairs).
        """
        if self._f_ia is None:
            self._f_ia = self.M_ia_from_M_p(self.f_p)
        return self._f_ia

    @property
    def rho_p(self) -> DistributedArray:
        r""" Electron-hole part of induced density matrix :math:`\delta \rho_p`

        In ravelled form (common index :math:`p` for electron-hole pairs).
        """
        return self._get_rho(0, True)

    @property
    def drho_p(self) -> DistributedArray:
        r""" First time derivative of :math:`\delta \rho_p`

        In ravelled form (common index :math:`p` for electron-hole pairs).
        """
        return self._get_rho(1, True)

    @property
    def ddrho_p(self) -> DistributedArray:
        r""" Second time derivative of :math:`\delta \rho_p`

        In ravelled form (common index :math:`p` for electron-hole pairs).
        """
        return self._get_rho(2, True)

    @property
    def rho_ia(self) -> DistributedArray:
        r""" Electron-hole part of induced density matrix :math:`\delta rho_{ia}`

        In non-ravelled form (indices :math:`ia` for electron-hole pairs).
        """
        return self._get_rho(0, False)

    @property
    def drho_ia(self) -> DistributedArray:
        r""" First time derivative of :math:`\delta rho_{ia}`

        In non-ravelled form (indices :math:`ia` for electron-hole pairs).
        """
        return self._get_rho(1, False)

    @property
    def ddrho_ia(self) -> DistributedArray:
        r""" Second time derivative of :math:`\delta rho_{ia}`

        In non-ravelled form (indices :math:`ia` for electron-hole pairs).
        """
        return self._get_rho(2, False)

    @property
    def Q_p(self) -> DistributedArray:
        r""" :math:`Q` in ravelled form (common index :math:`p` for electron-hole pairs)

        .. math::
            Q_p = \frac{2 \mathrm{Re}\:\delta\rho_p}{\sqrt{2 f_p}}

        where :math:`f_p` is the occupation number difference of pair :math:`p`.
        """
        return self._get_PQ(0, True, False)

    @property
    def P_p(self) -> DistributedArray:
        r""" :math:`P` in ravelled form (common index :math:`p` for electron-hole pairs)

        .. math::
            P_p = \frac{2 \mathrm{Im}\:\delta\rho_p}{\sqrt{2 f_p}}

        where :math:`f_p` is the occupation number difference of pair :math:`p`.
        """
        return self._get_PQ(0, True, True)

    @property
    def dQ_p(self) -> DistributedArray:
        r""" First time derivative of :math:`Q` in ravelled form """
        return self._get_PQ(1, True, False)

    @property
    def dP_p(self) -> DistributedArray:
        r""" First time derivative of :math:`P` in ravelled form """
        return self._get_PQ(1, True, True)

    @property
    def ddQ_p(self) -> DistributedArray:
        r""" Second time derivative of :math:`Q` in ravelled form """
        return self._get_PQ(2, True, False)

    @property
    def ddP_p(self) -> DistributedArray:
        r""" Second time derivative of :math:`P` in ravelled form """
        return self._get_PQ(2, True, True)

    @property
    def Q_ia(self) -> DistributedArray:
        r""" :math:`Q` in non-ravelled form (indices :math:`ia` for electron-hole pairs)

        .. math::
            Q_{ia} = \frac{2 \mathrm{Re}\:\delta\rho_{ia}}{\sqrt{2 f_{ia}}}

        where :math:`f_{ia}` is the occupation number difference of pair :math:`ia`.
        """
        return self._get_PQ(0, False, False)

    @property
    def P_ia(self) -> DistributedArray:
        r""" :math:`P` in non-ravelled form (indices :math:`ia` for electron-hole pairs)

        .. math::
            P_{ia} = \frac{2 \mathrm{Im}\:\delta\rho_{ia}}{\sqrt{2 f_{ia}}}

        where :math:`f_{ia}` is the occupation number difference of pair :math:`ia`.
        """
        return self._get_PQ(0, False, True)

    @property
    def dQ_ia(self) -> DistributedArray:
        r""" First time derivative of :math:`Q` in non-ravelled form """
        return self._get_PQ(1, False, False)

    @property
    def dP_ia(self) -> DistributedArray:
        r""" First time derivative of :math:`P` in non-ravelled form """
        return self._get_PQ(1, False, True)

    @property
    def ddQ_ia(self) -> DistributedArray:
        r""" Second time derivative of :math:`Q` in non-ravelled form """
        return self._get_PQ(2, False, False)

    @property
    def ddP_ia(self) -> DistributedArray:
        r""" Second time derivative of :math:`P` in non-ravelled form """
        return self._get_PQ(2, False, True)

    def _get_rho(self,
                 derivative: int,
                 ravelled: bool) -> DistributedArray:
        """ Fetch density matrix from dict where it might be stored

        Parameters
        ----------
        derivative
            Derivative order. 0 is plain density matrix
        ravelled
            If true, then returned in ravelled p index
        """
        # Pick the right array depending on whether ravelled p index (rho_p)
        # or two-dimensional ia index (rho_ia) is wanted
        array = self._rho_p_derivatives if ravelled else self._rho_ia_derivatives
        desc = self.derivative_desc[derivative]

        if ravelled == self._data_is_ravelled:
            # The original data is in the correct form. Read it
            assert derivative in array, f'{desc} not in {array.keys()}'
            return array[derivative]

        # Check if the desired density matrix is already stored in the array
        if derivative not in array:
            # If not, then transform the density matrix
            rho = self._transform_rho(derivative, ravelled)
            array[derivative] = rho

        return array[derivative]

    def _transform_rho(self,
                       derivative: int,
                       ravelled: bool) -> DistributedArray:
        """ Transform rho between ravelled and not ravelled form or opposite.
        Return it in the desired form

        Parameters
        ----------
        derivative
            Derivative order. 0 is plain density matrix
        ravelled
            If true, then returned in ravelled p index
        """
        if ravelled:
            # Transform from ia index
            rho_ia = self._get_rho(derivative, not ravelled)
            return self.M_p_from_M_ia(rho_ia)
        else:
            # Transform from p index
            rho_p = self._get_rho(derivative, not ravelled)
            return self.M_ia_from_M_p(rho_p)

    def _get_PQ(self,
                derivative: int,
                ravelled: bool,
                P: bool) -> DistributedArray:
        """ Return P or Q (related to real or imaginary part of induced density matrix)

        Parameters
        ----------
        derivative
            Derivative order. 0 is plain density matrix
        P
            If true, then return P (imaginary part) else Q (real part)
        ravelled
            If true, then returned in ravelled p index
        """
        rho = self._get_rho(derivative, ravelled)
        if self.rank > 0:
            assert isinstance(rho, ArrayIsOnRootRank)
            return ArrayIsOnRootRank()
        assert not isinstance(rho, ArrayIsOnRootRank)

        rho = np.sqrt(2) * (rho.imag if P else rho.real)

        if ravelled:
            return rho / np.sqrt(self.f_p)
        else:
            return self._divide_by_sqrt_fia(rho)

    def _divide_by_sqrt_fia(self,
                            X_ia: DistributedArray) -> DistributedArray:
        r""" Divide by :math:`\sqrt{f_{ia}}` where :math:`f_{ia} \neq 0`.
        Leave everything else as 0."""
        flt_ia = self.f_ia != 0
        Y_ia = np.zeros_like(X_ia)
        Y_ia[flt_ia] = X_ia[flt_ia] / np.sqrt(self.f_ia[flt_ia])

        return Y_ia

    def M_p_from_M_ia(self,
                      M_ia: DistributedArray) -> DistributedArray:
        if self.rank > 0:
            assert isinstance(M_ia, ArrayIsOnRootRank)
            return ArrayIsOnRootRank()
        assert not isinstance(M_ia, ArrayIsOnRootRank)
        imin, imax, amin, amax = self.ksd.ialims()
        M_p = np.empty((len(self.ksd.ia_p), ) + M_ia.shape[2:], dtype=M_ia.dtype)
        for p, (i, a) in enumerate(self.ksd.ia_p):
            M_p[p] = M_ia[i - imin, a - amin]

        return M_p

    def M_ia_from_M_p(self,
                      M_p: DistributedArray) -> DistributedArray:
        if self.rank > 0:
            assert isinstance(M_p, ArrayIsOnRootRank)
            return ArrayIsOnRootRank()
        assert not isinstance(M_p, ArrayIsOnRootRank)
        imin, imax, amin, amax = self.ksd.ialims()
        M_ia = np.zeros((imax - imin + 1, amax - amin + 1) + M_p.shape[1:], dtype=M_p.dtype)
        for M, (i, a) in zip(M_p, self.ksd.ia_p):
            M_ia[i - imin, a - amin] = M

        return M_ia

    def copy(self) -> DensityMatrix:
        """ Copy the density matrix """
        array = self._rho_p_derivatives if self._data_is_ravelled else self._rho_ia_derivatives
        matrices: dict[int, NDArray[np.complex64] | None] = {
            derivative: np.array(matrix) for derivative, matrix in array.items()}
        dm = DensityMatrix(ksd=self.ksd, matrices=matrices, data_is_ravelled=self._data_is_ravelled)
        return dm

    @classmethod
    def broadcast(cls,
                  density_matrix: DensityMatrix | None,
                  ksd: KohnShamDecomposition,
                  root: int,
                  comm) -> DensityMatrix:
        """ Broadcast a density matrix object which is on one rank to all other ranks

        Parameters
        ----------
        density_matrix
            The density matrix to be broadcast on the root rank, and None on other ranks
        ksd
            KohnShamDecomposition object
        root
            Rank of the process that has the original data
        comm
            MPI communicator
        """
        matrices: dict[int, NDArray[np.complex64] | None]
        # Broadcast necessary metadata
        if comm.rank == root:
            assert density_matrix is not None
            is_ravelled = density_matrix._data_is_ravelled
            array = (density_matrix._rho_p_derivatives if density_matrix._data_is_ravelled
                     else density_matrix._rho_ia_derivatives)
            matrix_shapes_dtypes = {derivative: (matrix.shape, matrix.dtype)
                                    for derivative, matrix in array.items()}
            metadata = (is_ravelled, matrix_shapes_dtypes)
            broadcast(metadata, root=root, comm=comm)
            matrices = {derivative: None if isinstance(arr, ArrayIsOnRootRank) else arr
                        for derivative, arr in array.items()}
        else:
            assert density_matrix is None
            is_ravelled, matrix_shapes_dtypes = broadcast(None, root=root, comm=comm)

        ksdrank = ksd.comm.rank if hasattr(ksd, 'comm') else 0
        ksd_members = ksd.comm.get_members() if hasattr(ksd, 'comm') else [world.rank]

        if comm.rank != root:
            if ksdrank == 0:
                matrices = {derivative: np.empty(shape, dtype=dtype)
                            for derivative, (shape, dtype) in matrix_shapes_dtypes.items()}
            else:
                matrices = {derivative: None
                            for derivative, (shape, dtype) in matrix_shapes_dtypes.items()}

        if len(ksd_members) > 1 and comm.size > 1:
            # Make sure communicators are complementary
            comm_members = comm.get_members()

            intersect = set(comm_members) & set(ksd_members)
            intersect.remove(world.rank)
            assert len(intersect) == 0, f'{comm_members} / {ksd_members}'

        # On density matrix non-root ranks, return ArrayIsOnRootRank()
        if ksdrank > 0:
            return DensityMatrix(ksd=ksd, matrices=matrices, data_is_ravelled=is_ravelled)

        # Broadcast the matrices
        for derivative, matrix in matrices.items():
            comm.broadcast(np.ascontiguousarray(matrix), root)

        if comm.rank == root:
            assert density_matrix is not None
            return density_matrix
        else:
            return DensityMatrix(ksd=ksd, matrices=matrices, data_is_ravelled=is_ravelled)
