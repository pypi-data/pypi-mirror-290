from __future__ import annotations

import os


try:
    from gpaw.mpi import world
except ImportError:
    class Communicator():
        def __init__(self, size, rank):
            self.size = size
            self.rank = rank

        def barrier(self):
            pass

    world = Communicator(size=1, rank=0)  # type: ignore


def create_path(fpath: str):
    dpath = os.path.dirname(fpath)
    if dpath == '':
        return
    if world.rank == 0:
        if not os.path.isdir(dpath):
            os.makedirs(dpath)
    world.barrier()


def FilePathType(fpath: str) -> str:
    create_path(fpath)
    return fpath


def FloatOrStrType(value: str | float) -> str | float:
    try:
        return float(value)
    except ValueError:
        return value


def IntOrStrType(value: str | int) -> str | int:
    try:
        return int(value)
    except ValueError:
        return value
