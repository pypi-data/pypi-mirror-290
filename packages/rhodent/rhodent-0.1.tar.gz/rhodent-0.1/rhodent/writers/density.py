from __future__ import annotations

import sys
import numpy as np
from typing import Any
from numpy.typing import NDArray
from gpaw.tddft.units import au_to_eV, au_to_fs

from ..calculators.density import DensityCalculator
from ..density_matrices.frequency import FrequencyDensityMatrices
from ..density_matrices.base import BaseDensityMatrices, WorkMetadata
from ..density_matrices.time import TimeDensityMatrices, ConvolutionDensityMatrices
from ..utils import Result
from ..voronoi import VoronoiWeights, EmptyVoronoiWeights
from .writer import Writer, ResultsCollector, FrequencyResultsCollector, TimeResultsCollector


class DensityWriter(Writer):

    """ Calculate density contributions

    Parameters
    ----------
    collector
        ResultsCollector object
    """

    def __init__(self,
                 collector: ResultsCollector):
        super().__init__(collector)
        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
            self._ulm_tag = 'Time Density'
            assert len(self.density_matrices.pulses) == 1, 'Only one pulse allowed'
        elif isinstance(self.density_matrices, FrequencyDensityMatrices):
            self._ulm_tag = 'Frequency Density'
        else:
            assert isinstance(self.density_matrices, TimeDensityMatrices)
            self._ulm_tag = 'Time Density'

    @property
    def voronoi(self) -> VoronoiWeights:
        return EmptyVoronoiWeights()

    @property
    def common_arrays(self) -> dict[str, NDArray[np.float64] | int | float]:
        common = super().common_arrays
        common.pop('eig_i')
        common.pop('eig_a')
        common.pop('eig_n')
        common.pop('imin')
        common.pop('imax')
        common.pop('amin')
        common.pop('amax')

        common['N_c'] = self.calc.N_c
        common['cell_cv'] = self.calc.cell_cv

        atoms = self.density_matrices.ksd.atoms
        common['atom_numbers_i'] = atoms.get_atomic_numbers()
        common['atom_positions_iv'] = atoms.get_positions()

        if isinstance(self.density_matrices, (ConvolutionDensityMatrices, TimeDensityMatrices)):
            common['time_t'] = self.density_matrices.times * 1e-3
        else:
            assert isinstance(self.density_matrices, FrequencyDensityMatrices)
            common['freq_w'] = self.density_matrices.frequencies

        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
            # Frequency (eV)
            pulsefreqs = [pulse.omega0 * au_to_eV for pulse in self.density_matrices.pulses]
            # FWHM in time domain (fs)
            pulsefwhms = [1 / pulse.sigma * (2 * np.sqrt(2 * np.log(2))) * au_to_fs
                          for pulse in self.density_matrices.pulses]

            common['pulsefreq'] = pulsefreqs[0]
            common['pulsefwhm'] = pulsefwhms[0]

        return common

    def fill_ulm(self,
                 writer,
                 work: WorkMetadata,
                 result: Result):
        writer.fill(result['rho_g'])

    def write_empty_arrays_ulm(self, writer):
        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
            Nt = len(self.density_matrices.times)
            writer.add_array('rho_tg', (Nt, ) + self.calc.gdshape, dtype=float)
        else:
            assert isinstance(self.density_matrices, FrequencyDensityMatrices)
            Nw = len(self.density_matrices.frequencies)
            writer.add_array('rho_wg', (Nw, ) + self.calc.gdshape, dtype=float)


def calculate_and_save_by_filename(out_fname: str,
                                   **kwargs):
    """ Calculate density contributions

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    gpw_file
        Filename of ground state file
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    if out_fname[-4:] == '.npz':
        calculate_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.ulm':
        calculate_and_save_ulm(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .ulm, is {out_fname}')
        sys.exit(1)


def calculate_and_save_ulm(out_fname: str,
                           density_matrices: BaseDensityMatrices,
                           gpw_file: str,
                           write_extra: dict[str, Any] = dict()):
    """ Calculate density contributions

    Densities are saved in an ULM file

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    gpw_file
        Filename of ground state file
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    calc = DensityCalculator(density_matrices=density_matrices,
                             gpw_file=gpw_file,
                             filter_occ=[(-np.inf, -1)],
                             filter_unocc=[(1, np.inf)],
                             )

    exclude = ['rho_g', 'occ_rho_rows_fg', 'occ_rho_diag_fg', 'unocc_rho_rows_fg', 'unocc_rho_diag_fg']
    cls = (TimeResultsCollector if isinstance(density_matrices, ConvolutionDensityMatrices)
           else FrequencyResultsCollector)
    writer = DensityWriter(cls(calc, calc_kwargs=dict(), exclude=exclude))
    writer.calculate_and_save_ulm(out_fname, write_extra=write_extra)


def calculate_and_save_npz(out_fname: str,
                           density_matrices: BaseDensityMatrices,
                           gpw_file: str,
                           write_extra: dict[str, Any] = dict()):
    """ Calculate density contributions

    Densities are saved in a numpy archive

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    gpw_file
        Filename of ground state file
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    """
    calc = DensityCalculator(density_matrices=density_matrices,
                             gpw_file=gpw_file,
                             filter_occ=[(-np.inf, -1)],
                             filter_unocc=[(1, np.inf)],
                             )

    exclude = ['occ_rho_rows_fg', 'occ_rho_diag_fg', 'unocc_rho_rows_fg', 'unocc_rho_diag_fg']
    cls = (TimeResultsCollector if isinstance(density_matrices, ConvolutionDensityMatrices)
           else FrequencyResultsCollector)
    writer = DensityWriter(cls(calc, calc_kwargs=dict(), exclude=exclude))
    writer.calculate_and_save_npz(out_fname, write_extra=write_extra)
