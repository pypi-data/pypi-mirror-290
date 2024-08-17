from __future__ import annotations

import sys
import numpy as np
from numpy.typing import NDArray
from typing import Any
from gpaw.tddft.units import au_to_eV, au_to_fs

from ..calculators.dipole import DipoleCalculator
from ..density_matrices.frequency import FrequencyDensityMatrices
from ..density_matrices.base import BaseDensityMatrices, WorkMetadata
from ..density_matrices.time import TimeDensityMatrices, ConvolutionDensityMatrices
from ..voronoi import EmptyVoronoiWeights, VoronoiWeights
from ..utils import Result
from .writer import Writer, ResultsCollector, FrequencyResultsCollector, TimeResultsCollector


class DipoleWriter(Writer):

    """ Calculate dipole moment contributions, optionally broadened onto
    an energy grid as a transition contribution map

    Parameters
    ----------
    collector
        ResultsCollector object
    """

    def __init__(self,
                 collector: ResultsCollector):
        super().__init__(collector)
        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
            self._ulm_tag = 'Time TCM'
            assert len(self.density_matrices.pulses) == 1, 'Only one pulse allowed'
        elif isinstance(self.density_matrices, FrequencyDensityMatrices):
            self._ulm_tag = 'TCM'
        else:
            assert isinstance(self.density_matrices, TimeDensityMatrices)
            self._ulm_tag = 'Time TCM'

    @property
    def common_arrays(self) -> dict[str, NDArray[np.float64] | int | float]:
        common = super().common_arrays

        if self.calc.sigma is not None:
            # There is an energy grid
            common['sigma'] = self.calc.sigma
            common['energy_o'] = np.array(self.calc.energies_occ)
            common['energy_u'] = np.array(self.calc.energies_unocc)

        if isinstance(self.density_matrices, (ConvolutionDensityMatrices, TimeDensityMatrices)):
            common['time_t'] = self.density_matrices.times * 1e-3
        else:
            assert isinstance(self.density_matrices, FrequencyDensityMatrices)
            common['freq_w'] = self.density_matrices.frequencies
            common['scale_w'] = 4 * common['freq_w'] / np.pi

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
        if self.collector.calc_kwargs.get('yield_total_ou', False):
            writer.fill(result['dm_ouv'])

    def write_empty_arrays_ulm(self, writer):
        if not self.collector.calc_kwargs.get('yield_total_ou', False):
            return
        shape_ou = (len(self.calc.energies_occ), len(self.calc.energies_unocc))
        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
            Nt = len(self.density_matrices.times)
            writer.add_array('dm_touv', (Nt, ) + shape_ou + (3, ), dtype=float)
        else:
            assert isinstance(self.density_matrices, FrequencyDensityMatrices)
            Nw = len(self.density_matrices.frequencies)
            writer.add_array('dm_wouv', (Nw, ) + shape_ou + (3, ), dtype=float)


def calculate_and_save_by_filename(out_fname: str,
                                   **kwargs):
    """ Calculate induced dipole moments and transition contribution maps

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the dipole contributions
        are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    save_matrix
        Whether the transition energy distributions should be computed and saved
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
                           voronoi: VoronoiWeights | None,
                           energies_occ: list[float] | NDArray[np.float64],
                           energies_unocc: list[float] | NDArray[np.float64],
                           sigma: float | None = None,
                           write_extra: dict[str, Any] = dict(),
                           save_matrix: bool = False):
    """ Calculate induced dipole moments and transition contribution maps

    Dipole moments and contributions are saved in an ULM file

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the dipole contributions
        are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    save_matrix
        Whether the transition energy distributions should be computed and saved
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = DipoleCalculator(density_matrices=density_matrices,
                            voronoi=voronoi,
                            energies_occ=energies_occ,
                            energies_unocc=energies_unocc,
                            sigma=sigma,
                            )

    calc_kwargs = dict(yield_total_ou=save_matrix)
    cls = (FrequencyResultsCollector if isinstance(density_matrices, FrequencyDensityMatrices)
           else TimeResultsCollector)
    writer = DipoleWriter(cls(calc, calc_kwargs, exclude=['dm_ouv']))
    writer.calculate_and_save_ulm(out_fname, write_extra=write_extra)


def calculate_and_save_npz(out_fname: str,
                           density_matrices: BaseDensityMatrices,
                           voronoi: VoronoiWeights | None,
                           energies_occ: list[float] | NDArray[np.float64],
                           energies_unocc: list[float] | NDArray[np.float64],
                           sigma: float | None = None,
                           write_extra: dict[str, Any] = dict(),
                           save_matrix: bool = False):
    """ Calculate induced dipole moments and transition contribution maps

    Dipole moments and contributions are saved in a numpy archive

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the dipole contributions
        are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    write_extra
        Dictionary of extra key-value pairs to write to the data file
    save_matrix
        Whether the transition energy distributions should be computed and saved
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = DipoleCalculator(density_matrices=density_matrices,
                            voronoi=voronoi,
                            energies_occ=energies_occ,
                            energies_unocc=energies_unocc,
                            sigma=sigma,
                            )

    calc_kwargs = dict(yield_total_ou=save_matrix)
    cls = (FrequencyResultsCollector if isinstance(density_matrices, FrequencyDensityMatrices)
           else TimeResultsCollector)
    writer = DipoleWriter(cls(calc, calc_kwargs))
    writer.calculate_and_save_npz(out_fname, write_extra=write_extra)
