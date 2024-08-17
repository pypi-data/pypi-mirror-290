from __future__ import annotations
from typing import Union

import numpy as np
from numpy.typing import NDArray

from gpaw import mpi
from gpaw.calculator import GPAW

GPAWCalculator = GPAW
Communicator = mpi._Communicator
ArrayIndex = Union[NDArray[np.int_], list[int], int, slice]
