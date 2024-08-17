from __future__ import annotations

from typing import Collection

import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.laser import Laser
from gpaw.mpi import world

from .frequency import FourierTransformer
from .time import AlltoallvTimeDistributor
from .pulse import PulseConvolver, Perturbation
from ..readers.gpaw import KohnShamRhoWfsReader
from ...utils import Logger


def create_density_matrix_reader(wfs_fname: str,
                                 ksd: KohnShamDecomposition | str,
                                 comm=world,
                                 yield_re: bool = True,
                                 yield_im: bool = True,
                                 stridet: int = 1,
                                 striden: int = 0,
                                 filter_times: list[float] | NDArray[np.float64] | None = None,
                                 log: Logger | None = None) -> KohnShamRhoWfsReader:
    rho_reader = KohnShamRhoWfsReader(
        wfs_fname=wfs_fname, ksd=ksd, comm=comm,
        yield_re=yield_re, yield_im=yield_im, stridet=stridet, striden=striden, log=log,
        filter_times=filter_times)

    return rho_reader


def create_fourier_transformer(wfs_fname: str,
                               ksd: KohnShamDecomposition | str,
                               comm=world,
                               yield_re: bool = True,
                               yield_im: bool = True,
                               stride_opts: dict[str, int] | None = None,
                               stridet: int = 1,
                               filter_frequencies: list[float] | NDArray[np.float64] | None = None,
                               log: Logger | None = None,
                               result_on_ranks: list[int] = []) -> FourierTransformer:
    rho_reader = KohnShamRhoWfsReader(
        wfs_fname=wfs_fname, ksd=ksd, comm=comm,
        yield_re=yield_re, yield_im=yield_im, log=log, stridet=stridet)

    time_distributor = AlltoallvTimeDistributor(rho_reader, stride_opts)
    fourier_transformer = FourierTransformer(time_distributor,
                                             filter_frequencies,
                                             result_on_ranks=result_on_ranks)
    return fourier_transformer


def create_pulse_convolver(wfs_fname: str,
                           ksd: KohnShamDecomposition | str,
                           perturbation: Perturbation | dict,
                           pulses: Collection[Laser],
                           comm=world,
                           yield_re: bool = True,
                           yield_im: bool = True,
                           derivative_order_s: list[int] = [0],
                           stride_opts: dict[str, int] | None = None,
                           stridet: int = 1,
                           filter_times: list[float] | NDArray[np.float64] | None = None,
                           log: Logger | None = None,
                           result_on_ranks: list[int] = []) -> PulseConvolver:
    rho_chunk_reader = KohnShamRhoWfsReader(
        wfs_fname=wfs_fname, ksd=ksd, comm=comm,
        yield_re=yield_re, yield_im=yield_im, log=log, stridet=stridet)

    time_distributor = AlltoallvTimeDistributor(rho_chunk_reader, stride_opts=stride_opts)
    pulse_convolver = PulseConvolver(time_distributor,
                                     pulses=pulses,
                                     perturbation=perturbation,
                                     derivative_order_s=derivative_order_s,
                                     filter_times=filter_times,
                                     result_on_ranks=result_on_ranks)
    return pulse_convolver
