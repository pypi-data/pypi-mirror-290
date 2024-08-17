from __future__ import annotations

import sys
import numpy as np
from numpy.typing import NDArray
from typing import Any
from gpaw.tddft.units import au_to_eV, au_to_fs

from ..calculators.energy import EnergyCalculator
from ..density_matrices.time import ConvolutionDensityMatrices, ConvolutionDensityMatrixMetadata
from ..voronoi import EmptyVoronoiWeights, VoronoiWeights
from .writer import Writer, ResultsCollector, TimeResultsCollector, PulseConvolutionResultsCollector
from ..utils import Result


class EnergyWriter(Writer):

    """ Calculate energy contributions

    Parameters
    ----------
    collector
        ResultsCollector object
    """

    def __init__(self,
                 collector: ResultsCollector,
                 only_one_pulse: bool):
        super().__init__(collector)
        self.only_one_pulse = only_one_pulse
        self._ulm_tag = 'EnergyDecomposition'
        if only_one_pulse:
            if isinstance(self.density_matrices, ConvolutionDensityMatrices):
                assert len(self.density_matrices.pulses) == 1, 'Only one pulse allowed'
        else:
            assert isinstance(self.density_matrices, ConvolutionDensityMatrices)

    @property
    def common_arrays(self) -> dict[str, NDArray[np.float64] | int | float]:
        common = super().common_arrays

        if self.calc.sigma is not None:
            # There is an energy grid
            common['sigma'] = self.calc.sigma
            common['energy_o'] = np.array(self.calc.energies_occ)
            common['energy_u'] = np.array(self.calc.energies_unocc)

        assert isinstance(self.density_matrices, ConvolutionDensityMatrices)
        common['time_t'] = self.density_matrices.times * 1e-3
        # Frequency (eV)
        pulsefreqs = [pulse.omega0 * au_to_eV for pulse in self.density_matrices.pulses]
        # FWHM in time domain (fs)
        pulsefwhms = [1 / pulse.sigma * (2 * np.sqrt(2 * np.log(2))) * au_to_fs
                      for pulse in self.density_matrices.pulses]

        if self.only_one_pulse:
            common['pulsefreq'] = pulsefreqs[0]
            common['pulsefwhm'] = pulsefwhms[0]
        else:
            common['pulsefreq_p'] = np.array(pulsefreqs)
            common['pulsefwhm_p'] = np.array(pulsefwhms)

        return common

    def fill_ulm(self,
                 writer,
                 work: ConvolutionDensityMatrixMetadata,
                 result: Result):
        assert self.only_one_pulse
        if self.collector.calc_kwargs['yield_total_E_ou']:
            writer.fill(result['E_ou'])

    def write_empty_arrays_ulm(self, writer):
        assert self.only_one_pulse
        if not self.collector.calc_kwargs['yield_total_E_ou']:
            return
        shape_ou = (len(self.calc.energies_occ), len(self.calc.energies_unocc))
        Nt = len(self.density_matrices.times)
        writer.add_array('E_tou', (Nt, ) + shape_ou, dtype=float)


def calculate_and_save_by_filename(out_fname: str,
                                   **kwargs):
    """ Calculate energy contributions

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the energy contributions
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
        Whether the electron-hole map matrix should be computed and saved
    save_dist
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
                           density_matrices: ConvolutionDensityMatrices,
                           voronoi: VoronoiWeights | None,
                           energies_occ: list[float] | NDArray[np.float64],
                           energies_unocc: list[float] | NDArray[np.float64],
                           sigma: float | None = None,
                           write_extra: dict[str, Any] = dict(),
                           save_matrix: bool = False,
                           save_dist: bool = False):
    """ Calculate energy contributions

    Energies and contributions are saved in an ULM file

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the energy contributions
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
        Whether the electron-hole map matrix should be computed and saved
    save_dist
        Whether the transition energy distributions should be computed and saved
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = EnergyCalculator(density_matrices=density_matrices,
                            voronoi=voronoi,
                            energies_occ=energies_occ,
                            energies_unocc=energies_unocc,
                            sigma=sigma,
                            )

    calc_kwargs = dict(yield_total_E_ou=save_matrix, yield_total_dists=save_dist)
    writer = EnergyWriter(TimeResultsCollector(calc, calc_kwargs, exclude=['E_ou']), only_one_pulse=True)
    writer.calculate_and_save_ulm(out_fname, write_extra=write_extra)


def calculate_and_save_npz(out_fname: str,
                           density_matrices: ConvolutionDensityMatrices,
                           voronoi: VoronoiWeights | None,
                           energies_occ: list[float] | NDArray[np.float64],
                           energies_unocc: list[float] | NDArray[np.float64],
                           sigma: float | None = None,
                           write_extra: dict[str, Any] = dict(),
                           save_matrix: bool = False,
                           save_dist: bool = False,
                           only_one_pulse: bool = True):
    """ Calculate energy contributions

    Energies and contributions are saved in a numpy archive

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time or frequency domain
    voronoi
        Optional Voronoi weights object. If given, then the energy contributions
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
        Whether the electron-hole map matrix should be computed and saved
    save_dist
        Whether the transition energy distributions should be computed and saved
    only_one_pulse
        If False, group arrays by pulse
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = EnergyCalculator(density_matrices=density_matrices,
                            voronoi=voronoi,
                            energies_occ=energies_occ,
                            energies_unocc=energies_unocc,
                            sigma=sigma,
                            )

    calc_kwargs = dict(yield_total_E_ou=save_matrix, yield_total_dists=save_dist)
    cls = TimeResultsCollector if only_one_pulse else PulseConvolutionResultsCollector
    writer = EnergyWriter(cls(calc, calc_kwargs), only_one_pulse=only_one_pulse)
    writer.calculate_and_save_npz(out_fname, write_extra=write_extra)
