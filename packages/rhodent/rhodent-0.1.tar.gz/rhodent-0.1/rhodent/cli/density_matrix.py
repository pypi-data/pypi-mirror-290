from __future__ import annotations

import sys
from argparse import ArgumentError
from typing import Collection, NamedTuple

import numpy as np
from numpy.typing import NDArray

from gpaw.lcaotddft.laser import GaussianPulse

from .argparse_util import FilePathType
from ..density_matrices.frequency import (FrequencyDensityMatrices, FrequencyDensityMatricesFromDisk,
                                          FrequencyDensityMatricesFromWaveFunctions)
from ..density_matrices.time import (ConvolutionDensityMatrices, ConvolutionDensityMatricesFromDisk,
                                     ConvolutionDensityMatricesFromFrequency,
                                     ConvolutionDensityMatricesFromWaveFunctions)


def create_convolution_density_matrices(data_files: DataFiles,
                                        pulses: Collection[GaussianPulse],
                                        times: list[float] | NDArray[np.float64],
                                        derivative_order_s: list[int] = [0],
                                        real: bool = True,
                                        imag: bool = True,
                                        calc_size: int = 1,
                                        **pulserho_iterator_kw) -> ConvolutionDensityMatrices:
    pulserho_from = ('frho' if data_files.frho_fmt is not None else
                     'wavefcn' if data_files.wfs_fname is not None else
                     'disk')

    assert isinstance(pulses, list)  # TODO try work around this

    density_matrices: ConvolutionDensityMatrices
    if pulserho_from == 'disk':
        assert data_files.pulserho_fmt is not None
        density_matrices = ConvolutionDensityMatricesFromDisk(
            pulserho_fmt=data_files.pulserho_fmt,
            ksd=data_files.ksd_fname,
            pulses=pulses,
            times=times,
            real=real, imag=imag,
            calc_size=calc_size,
            derivative_order_s=derivative_order_s)
    elif pulserho_from == 'frho':
        assert data_files.frho_fmt is not None
        density_matrices = ConvolutionDensityMatricesFromFrequency(
            frho_fmt=data_files.frho_fmt,
            ksd=data_files.ksd_fname,
            pulses=pulses,
            times=times,
            real=real, imag=imag,
            calc_size=calc_size,
            derivative_order_s=derivative_order_s)
    elif pulserho_from == 'wavefcn':
        assert data_files.wfs_fname is not None
        density_matrices = ConvolutionDensityMatricesFromWaveFunctions(
            wfs_fname=data_files.wfs_fname,
            **pulserho_iterator_kw,
            ksd=data_files.ksd_fname,
            pulses=pulses,
            times=times,
            real=real, imag=imag,
            calc_size=calc_size,
            derivative_order_s=derivative_order_s)
    else:
        raise ValueError(f'Do not recognize key {pulserho_from}')

    return density_matrices


def create_frequency_domain_density_matrices(data_files: DataFiles,
                                             frequencies: list[float] | NDArray[np.float64],
                                             derivative_order_s: list[int] = [0],
                                             real: bool = True,
                                             imag: bool = True,
                                             calc_size: int = 1,
                                             **pulserho_iterator_kw) -> FrequencyDensityMatrices:
    pulserho_from = ('frho' if data_files.frho_fmt is not None else
                     'wavefcn')

    density_matrices: FrequencyDensityMatrices
    if pulserho_from == 'frho':
        assert data_files.frho_fmt is not None
        density_matrices = FrequencyDensityMatricesFromDisk(
            frho_fmt=data_files.frho_fmt,
            ksd=data_files.ksd_fname,
            frequencies=frequencies,
            real=real, imag=imag,
            calc_size=calc_size,
            derivative_order_s=derivative_order_s)
    elif pulserho_from == 'wavefcn':
        assert data_files.wfs_fname is not None
        density_matrices = FrequencyDensityMatricesFromWaveFunctions(
            wfs_fname=data_files.wfs_fname,
            **pulserho_iterator_kw,
            ksd=data_files.ksd_fname,
            frequencies=frequencies,
            real=real, imag=imag,
            calc_size=calc_size,
            derivative_order_s=derivative_order_s)
    else:
        raise ValueError(f'Do not recognize key {pulserho_from}')

    return density_matrices


class DataFiles(NamedTuple):
    """ Convenience class to get collect filenames

    The frho_fmt is a formatting string for the density matrices in
    frequency space. Similar for pulserho_fmt. Example:

    frho_fmt = 'frho/w{freq:05.2f}-{reim}.npy'
    pulserho_fmt =  'pulserho/t{time:09.1f}{tag}.npy'
    """

    ksd_fname: str
    gpw_unocc_fname: str | None = None
    frho_fmt: str | None = None
    pulserho_fmt: str | None = None
    wfs_fname: str | None = None

    def frho_fname(self,
                   freq: float,
                   reim: str) -> str:
        assert self.frho_fmt is not None
        fname = self.frho_fmt.format(freq=freq, reim=reim)

        return fname

    @property
    def frho_dname(self) -> str:
        """ Name of frho directory

        """
        from os.path import dirname
        assert self.frho_fmt is not None
        fname = self.frho_fmt.format(freq=0, reim='Re')
        dname = dirname(fname)

        return dname

    def pulserho_fname(self,
                       time: float,
                       tag: str,
                       pulsefreq: float,
                       pulsefwhm: float) -> str:
        assert self.pulserho_fmt is not None
        fname = self.pulserho_fmt.format(time=time, tag=tag, pulsefreq=pulsefreq, pulsefwhm=pulsefwhm)

        return fname

    @property
    def pulserho_dname(self) -> str:
        """ Name of pulserho directory

        """
        assert self.pulserho_fmt is not None
        from os.path import dirname
        fname = self.pulserho_fmt.format(time=0, tag='', pulsefreq=0, pulsefwhm=0)
        dname = dirname(fname)

        return dname


def add_density_matrix_arguments(parser,
                                 allow_frho: bool = True,
                                 allow_wfs: bool = True,
                                 allow_disk: bool = False):
    nopts = sum([allow_frho, allow_wfs, allow_disk])
    assert nopts >= 1

    gparse = parser.add_argument_group(
        'Ground state')
    fparse = parser.add_argument_group(
        'Frequency response',
        'Provide one of the following files:')

    try:
        gparse.add_argument('-g', '--gpw-file', type=FilePathType, required=False,
                            help='gpw file with ground state including all unoccupied states. '
                            'Currently only used to compute Voronoi weights')
    except ArgumentError:
        pass

    gparse.add_argument('--ksdfile', type=FilePathType, required=True,
                        help='KohnShamDecomposition file')
    if allow_frho:
        fparse.add_argument('--frhodir', type=FilePathType, required=nopts == 1,
                            help='Directory with density matrices in frequency space')
    if allow_wfs:
        fparse.add_argument('--wfsfile', type=FilePathType, required=nopts == 1,
                            help='Wave function dump file')
    if allow_disk:
        fparse.add_argument('--pulserho-dir', type=FilePathType, required=nopts == 1,
                            help='Wave function dump file')


def parse_data_files(args,
                     allow_frho: bool = True,
                     allow_wfs: bool = True,
                     allow_disk: bool = False,
                     **kwargs) -> DataFiles:
    opts = []
    allowed_args = []
    if allow_frho:
        opts += ['FRHODIR']
        allowed_args += [args.frhodir]
    if allow_wfs:
        opts += ['WFSFILE']
        allowed_args += [args.wfsfile]
    if allow_disk:
        opts += ['PULSERHO-DIR']
        allowed_args += [args.pulserho_dir]

    assert len(opts) > 0

    noneopts = [opt for opt in allowed_args if opt is not None]
    if len(noneopts) == 0:
        print('Give either ' + ', or '.join(opts))
        sys.exit(1)

    if len(noneopts) > 1:
        print('Give either ' + ', or '.join(opts) + ', not all')
        sys.exit(1)

    if allow_frho and args.frhodir is not None:
        kw = dict(frho_fmt=args.frhodir + '/w{freq:05.2f}-{reim}.npy')
    elif allow_wfs and args.wfsfile is not None:
        kw = dict(wfs_fname=args.wfsfile)
    else:
        kw = dict(pulserho_fmt=args.pulserho_dir + '/t{time:09.1f}{tag}.npy')
    kw.update(**kwargs)
    data_files = DataFiles(gpw_unocc_fname=args.gpw_file,
                           ksd_fname=args.ksdfile,
                           **kw)
    return data_files
