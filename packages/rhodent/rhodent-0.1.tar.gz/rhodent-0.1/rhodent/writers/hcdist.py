from __future__ import annotations

import sys
from typing import cast
import numpy as np
from numpy.typing import NDArray
from gpaw.mpi import world
from gpaw.tddft.units import au_to_eV, au_to_fs

from ..calculators.hotcarriers import HotCarriersCalculator
from ..density_matrices.time import (ConvolutionDensityMatrices, TimeDensityMatrices)
from ..voronoi import EmptyVoronoiWeights, VoronoiWeights
from .writer import (Writer, ResultsCollector, TimeAverageResultsCollector,
                     TimeResultsCollector,
                     PulseConvolutionAverageResultsCollector)


class HotCarriersWriter(Writer):

    """ Calculate hot-carrier totals, and optionally broadened hot-carrier energy distributions

    Parameters
    ----------
    collector
        ResultsCollector object
    only_one_pulse
        False if the resulting outputs should have one dimension corresponding
        to different pulses. True if there should be no such dimension. If True,
        then the calculator must only hold one pulse.
    """

    def __init__(self,
                 collector: ResultsCollector,
                 only_one_pulse: bool):
        super().__init__(collector)
        self.only_one_pulse = only_one_pulse
        if only_one_pulse:
            if isinstance(self.density_matrices, ConvolutionDensityMatrices):
                assert len(self.density_matrices.pulses) == 1, 'Only one pulse allowed'
        else:
            assert isinstance(self.density_matrices, ConvolutionDensityMatrices)

    @property
    def common_arrays(self) -> dict[str, NDArray[np.float64] | int | float]:
        common = super().common_arrays
        assert isinstance(self.density_matrices, (TimeDensityMatrices, ConvolutionDensityMatrices))

        if isinstance(self.collector, (TimeAverageResultsCollector, PulseConvolutionAverageResultsCollector)):
            # Averages over time are taken
            common['avgtime_t'] = self.density_matrices.times * 1e-3
        else:
            common['time_t'] = self.density_matrices.times * 1e-3

        if isinstance(self.density_matrices, ConvolutionDensityMatrices):
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

        if self.calc.sigma is not None:
            # There is an energy grid
            common['sigma'] = self.calc.sigma
            common['energy_o'] = np.array(self.calc.energies_occ)
            common['energy_u'] = np.array(self.calc.energies_unocc)

        return common


def calculate_hcdist_and_save_by_filename(out_fname: str, **kwargs):
    """ Calculate broadened hot-carrier energy distributions, optionally averaged over time

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time domain
    voronoi
        Optional Voronoi weights object. If given, then the hot-carrier
        distributions are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    average_times
        If true, an average over the given times will be taken. If false, then
        hot-carrier distributions are computed separately over the times, and
        each output is written separately for each time
    """
    if out_fname[-4:] == '.npz':
        calculate_hcdist_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.dat':
        calculate_hcdist_and_save_dat(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .dat, is {out_fname}')
        sys.exit(1)


def calculate_hcsweeppulse_and_save_by_filename(out_fname: str, **kwargs):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of pulses

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if out_fname[-4:] == '.npz':
        calculate_hcsweeppulse_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.dat':
        calculate_hcsweeppulse_and_save_dat(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .dat, is {out_fname}')
        sys.exit(1)


def calculate_hcsweeptime_and_save_by_filename(out_fname: str, **kwargs):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of times

    The ground state including all unoccupied states and KohnShamDecomposition file are loaded.
    The delta-kick response density matrix in frequency space is loaded,
    convoluted with a pulse in frequency space, and inverse Fourier transformed to real time.
    Then number of generated HCs are computed for each of the atom projections.

    The file format of the resulting data file is inferred from the file name

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if out_fname[-4:] == '.npz':
        calculate_hcsweeptime_and_save_npz(out_fname=out_fname, **kwargs)
    elif out_fname[-4:] == '.dat':
        calculate_hcsweeptime_and_save_dat(out_fname=out_fname, **kwargs)
    else:
        print(f'output-file must have ending .npz or .dat, is {out_fname}')
        sys.exit(1)


def calculate_hcdist_and_save_dat(out_fname: str,
                                  density_matrices: TimeDensityMatrices | ConvolutionDensityMatrices,
                                  voronoi: VoronoiWeights | None = None,
                                  energies_occ: list[float] | NDArray[np.float64] = [],
                                  energies_unocc: list[float] | NDArray[np.float64] = [],
                                  *,
                                  sigma: float,
                                  average_times: bool = True):
    """ Calculate broadened hot-carrier energy distributions, optionally averaged over time

    HC distributions are saved in a text file

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time domain
    voronoi
        Optional Voronoi weights object. If given, then the hot-carrier
        distributions are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    average_times
        If true, an average over the given times will be taken. If false, then
        hot-carrier distributions are computed separately over the times, and
        each output is written separately for each time
    """
    zerostr = 'relative to Fermi level'

    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    # Calculate
    if len(energies_occ) == 0 and len(energies_unocc) == 0:
        raise ValueError('Either occupied or unoccupied energies grid must be given')

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=energies_occ,
                                 energies_unocc=energies_unocc,
                                 sigma=sigma,
                                 )

    calc_kwargs = dict(yield_total_hcdists=True, yield_proj_hcdists=True)
    cls = TimeAverageResultsCollector if average_times else TimeResultsCollector
    writer = HotCarriersWriter(cls(calc, calc_kwargs), only_one_pulse=True)
    _data = dict(**writer.common_arrays)
    _data.update(writer.calculate_data()._data)

    if world.rank > 0:
        return

    pulsefreq = _data.pop('pulsefreq', None)
    pulsefwhm = _data.pop('pulsefwhm', None)

    data = cast(dict[str, NDArray[np.float64]], _data)

    # Set up array to be written in the data file.
    # Rows are energies, columns are projections and/or times
    nI = len(voronoi)
    ne = max(len(energies_occ), len(energies_unocc))  # Longest length of energies

    eh_labels = []
    if len(energies_occ) > 0:
        # Compute hole distributions
        eh_labels.append('H')
    if len(energies_unocc) > 0:
        # Compute electron distributions
        eh_labels.append('E')

    if average_times:
        nt = 1
    else:
        nt = len(data['time_t'])

    ncolspertime = len(eh_labels) * (1 + nI)

    savedata = np.full((ne, len(eh_labels) + nt * ncolspertime), np.nan)
    savedata_by_times = [savedata[:, col:col + ncolspertime]
                         for col in range(len(eh_labels), savedata.shape[1], ncolspertime)]

    # Set up format string
    fmt = len(eh_labels) * ['%15.6f'] + nt * ncolspertime * ['%18.8e']

    # Set up header contents
    header_lines = [f'Hot carrier (H=hole, E=electron) distributions {zerostr}']

    if pulsefreq is not None:
        header_lines.append(f'Response to pulse with frequency {pulsefreq:.2f}eV, '
                            f'FWHM {pulsefwhm:.2f}fs')

    if average_times:
        avgtimes = data['avgtime_t']
        header_lines.append(f'Averaged for {len(avgtimes)} times between '
                            f'{avgtimes[0]:.1f}fs-{avgtimes[-1]:.1f}fs')
    else:
        times = data['time_t']
        header_lines.append(f'Computed for the following {len(times)} times (in fs)')
        header_lines += [f'  {time:.4f}' for t, time in enumerate(times)]

    if nI > 0:
        header_lines.append('Atomic projections')
        header_lines += [f'  {i:4.0f}: {str(proj)}' for i, proj in enumerate(voronoi.atom_projections)]

    header_lines.append(f'Gaussian folding, Width {sigma:.4f}eV')
    desc_entries = ([f'{label} energy (eV)' for label in eh_labels] +
                    [f'Total {label} (1/eV)' for label in eh_labels] +
                    [f'Proj {s} {i:2.0f} (1/eV)' for i in range(nI) for s in eh_labels])
    desc_entries = ([f'{s:>15}' for s in desc_entries[:len(eh_labels)]] +
                    [f'{s:>18}' for s in desc_entries[len(eh_labels):]])
    desc_entries[0] = desc_entries[0][2:]  # Remove two spaces to account for '# '
    if not average_times:
        desc_entries.append(' ... repeated for next times')
    header_lines.append(' '.join(desc_entries))

    # Write the data to the array
    if average_times:
        if len(eh_labels) == 2:
            # Computed both electron and hole distributions
            savedata[:len(energies_occ), 0] = energies_occ
            savedata[:len(energies_unocc), 1] = energies_unocc

            savedata[:len(energies_occ), 2] = data['hcdist_o']
            savedata[:len(energies_unocc), 3] = data['hcdist_u']

            if nI > 0:
                savedata[:len(energies_occ), 4::2] = data['hcdist_proj_Io'].T
                savedata[:len(energies_unocc), 5::2] = data['hcdist_proj_Iu'].T
        elif 'H' in eh_labels:
            # Only hole distributions
            savedata[:, 0] = energies_occ
            savedata[:, 1] = data['hcdist_o']

            if nI > 0:
                savedata[:, 2:] = data['hcdist_proj_Io'].T
        else:
            # Only electron distributions
            savedata[:, 0] = energies_unocc
            savedata[:, 1] = data['hcdist_u']

            if nI > 0:
                savedata[:, 1:] = data['hcdist_proj_Iu'].T
    else:
        if len(eh_labels) == 2:
            # Computed both electron and hole distributions
            savedata[:len(energies_occ), 0] = energies_occ
            savedata[:len(energies_unocc), 1] = energies_unocc

            for t, sdata in enumerate(savedata_by_times):
                sdata[:len(energies_occ), 0] = data['hcdist_to'][t]
                sdata[:len(energies_unocc), 1] = data['hcdist_tu'][t]

                if nI > 0:
                    sdata[:len(energies_occ), 2::2] = data['hcdist_proj_tIo'][t].T
                    sdata[:len(energies_unocc), 3::2] = data['hcdist_proj_tIu'][t].T
        elif 'H' in eh_labels:
            # Only hole distributions
            savedata[:, 0] = energies_occ

            for t, sdata in enumerate(savedata_by_times):
                sdata[:, 0] = data['hcdist_to'][t]

                if nI > 0:
                    sdata[:, 1:] = data['hcdist_proj_tIo'][t].T
        else:
            # Only electron distributions
            savedata[:, 0] = energies_unocc

            for t, sdata in enumerate(savedata_by_times):
                sdata[:, 0] = data['hcdist_tu'][t]

                if nI > 0:
                    sdata[:, 1:] = data['hcdist_proj_tIu'][t].T

    np.savetxt(out_fname, savedata, fmt, header='\n'.join(header_lines))
    print(f'Written {out_fname}', flush=True)


def calculate_hcsweeppulse_and_save_dat(out_fname: str,
                                        density_matrices: ConvolutionDensityMatrices,
                                        voronoi: VoronoiWeights | None):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of pulses

    HC distributions are saved in a text file

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    Np = len(density_matrices.pulses)

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=[],
                                 energies_unocc=[],
                                 sigma=None,
                                 )
    calc_kwargs = dict(yield_total_hcdists=False, yield_proj_hcdists=False)
    collector = PulseConvolutionAverageResultsCollector(calc, calc_kwargs)
    writer = HotCarriersWriter(collector, only_one_pulse=False)
    data = dict(**writer.common_arrays)
    data.update(writer.calculate_data()._data)

    if world.rank > 0:
        return

    nI = len(voronoi)
    avgtimes = data['avgtime_t']
    assert isinstance(avgtimes, np.ndarray)

    savedata = np.full((Np, 2*(2+nI)), np.nan)
    savedata[:, 0] = data['pulsefreq_p']
    savedata[:, 1] = data['pulsefwhm_p']
    savedata[:, 2] = data['sumocc_p']
    savedata[:, 3] = data['sumunocc_p']
    savedata[:, 4::2] = data['sumocc_proj_pI']
    savedata[:, 5::2] = data['sumunocc_proj_pI']

    projectionsstr = '\n'.join([f'  {i:4.0f}: {str(proj)}'
                                for i, proj in enumerate(voronoi.atom_projections)])
    desc_entries = (['Pulse freq (eV)', 'Pulse FWHM (fs)', 'Total H', 'Total E'] +
                    [f'Proj {s} {i:2.0f}' for i in range(nI) for s in 'HE'])
    desc_entries = ([f'{s:>17}' for s in desc_entries[:2]] +
                    [f'{s:>15}' for s in desc_entries[2:]])
    desc_entries[0] = desc_entries[0][2:]  # Remove two spaces to account for '# '

    header = (f'Hot carrier (H=hole, E=electron) numbers\n'
              f'Averaged for {len(avgtimes)} times between '
              f'{avgtimes[0]:.1f}fs-{avgtimes[-1]:.1f}fs\n'
              'Atomic projections:\n'
              f'{projectionsstr}\n'
              f'{" ".join(desc_entries)}')
    fmt = 2*['%17.6f'] + (2*(nI + 1))*['%15.8e']
    np.savetxt(out_fname, savedata, fmt, header=header)
    print(f'Written {out_fname}', flush=True)


def calculate_hcsweeptime_and_save_dat(out_fname: str,
                                       density_matrices: TimeDensityMatrices | ConvolutionDensityMatrices,
                                       voronoi: VoronoiWeights | None):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of times

    The ground state including all unoccupied states and KohnShamDecomposition file are loaded.
    The delta-kick response density matrix in frequency space is loaded,
    convoluted with a pulse in frequency space, and inverse Fourier transformed to real time.
    Then number of generated HCs are computed for each of the atom projections.

    HC distributions are saved in a text file

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    Nt = len(density_matrices.times)

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=[],
                                 energies_unocc=[],
                                 sigma=None,
                                 )
    calc_kwargs = dict(yield_total_hcdists=False, yield_proj_hcdists=False)
    collector = TimeResultsCollector(calc, calc_kwargs)
    writer = HotCarriersWriter(collector, only_one_pulse=True)
    data = dict(**writer.common_arrays)
    data.update(writer.calculate_data()._data)

    if world.rank > 0:
        return

    nI = len(voronoi)

    savedata = np.full((Nt, 1 + 2*(1+nI)), np.nan)
    savedata[:, 0] = data['time_t']
    savedata[:, 1] = data['sumocc_t']
    savedata[:, 2] = data['sumunocc_t']
    savedata[:, 3::2] = data['sumocc_proj_tI']
    savedata[:, 4::2] = data['sumunocc_proj_tI']

    projectionsstr = '\n'.join([f'  {i:4.0f}: {str(proj)}'
                                for i, proj in enumerate(voronoi.atom_projections)])
    desc_entries = (['Time (fs)', 'Total H', 'Total E'] +
                    [f'Proj {s} {i:2.0f}' for i in range(nI) for s in 'HE'])
    desc_entries = ([f'{s:>17}' for s in desc_entries[:1]] +
                    [f'{s:>15}' for s in desc_entries[1:]])
    desc_entries[0] = desc_entries[0][2:]  # Remove two spaces to account for '# '

    header_lines = ['Hot carrier (H=hole, E=electron) numbers\n']
    if isinstance(density_matrices, ConvolutionDensityMatrices):
        header_lines += [f'Response to pulse with frequency {data["pulsefreq"]:.2f}eV, '
                         f'FWHM {data["pulsefwhm"]:.2f}fs']
    header_lines += ['Atomic projections:',
                     f'{projectionsstr}\n',
                     ' '.join(desc_entries)]
    header = '\n'.join(header_lines)
    fmt = ['%17.6f'] + (2*(nI + 1))*['%15.8e']
    np.savetxt(out_fname, savedata, fmt, header=header)
    print(f'Written {out_fname}', flush=True)


def calculate_hcdist_and_save_npz(out_fname: str,
                                  density_matrices: TimeDensityMatrices | ConvolutionDensityMatrices,
                                  voronoi: VoronoiWeights | None,
                                  energies_occ: list[float] | NDArray[np.float64] = [],
                                  energies_unocc: list[float] | NDArray[np.float64] = [],
                                  *,
                                  sigma: float,
                                  average_times: bool = True):
    """ Calculate broadened hot-carrier energy distributions, optionally averaged over time

    HC distributions are saved in a compressed numpy archive

    Parameters
    ----------
    out_fname
        File name of the resulting data file
    density_matrices
        Collection of density matrices in the time domain
    voronoi
        Optional Voronoi weights object. If given, then the hot-carrier
        distributions are additonally projected according to the weights.
    energies_occ
        Energy grid in eV for occupied levels (hole carriers). If given,
        hole distributions are computed and saved.
    energies_unocc
        Energy grid in eV for unoccupied levels (excited electrons). If given,
        electron distributions are computed and saved.
    sigma
        Gaussian broadening width in eV for the broadened distributions.
    average_times
        If true, an average over the given times will be taken. If false, then
        hot-carrier distributions are computed separately over the times, and
        each output is written separately for each time
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    if len(energies_occ) == 0 and len(energies_unocc) == 0:
        raise ValueError('Either occupied or unoccupied energies grid must be given')

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=energies_occ,
                                 energies_unocc=energies_unocc,
                                 sigma=sigma,
                                 )
    calc_kwargs = dict(yield_total_hcdists=True, yield_proj_hcdists=True)
    cls = TimeAverageResultsCollector if average_times else TimeResultsCollector
    writer = HotCarriersWriter(cls(calc, calc_kwargs), only_one_pulse=True)
    writer.calculate_and_save_npz(out_fname)


def calculate_hcsweeppulse_and_save_npz(out_fname: str,
                                        density_matrices: ConvolutionDensityMatrices,
                                        voronoi: VoronoiWeights | None):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of pulses

    HC distributions are saved in a text file

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=[],
                                 energies_unocc=[],
                                 sigma=None,
                                 )
    calc_kwargs = dict(yield_total_hcdists=False, yield_proj_hcdists=False)
    collector = PulseConvolutionAverageResultsCollector(calc, calc_kwargs)
    writer = HotCarriersWriter(collector, only_one_pulse=False)
    writer.calculate_and_save_npz(out_fname)


def calculate_hcsweeptime_and_save_npz(out_fname: str,
                                       density_matrices: TimeDensityMatrices | ConvolutionDensityMatrices,
                                       voronoi: VoronoiWeights | None):
    """ Calculate the number of generated hot carriers, projected on groups of atoms, for
    a list of times

    The ground state including all unoccupied states and KohnShamDecomposition file are loaded.
    The delta-kick response density matrix in frequency space is loaded,
    convoluted with a pulse in frequency space, and inverse Fourier transformed to real time.
    Then number of generated HCs are computed for each of the atom projections.

    HC distributions are saved in a text file

    Parameters
    ----------
    out_fname
       File name of data file where data is to be saved
    density_matrices
        Object that gives the density matrix in the time domain
    voronoi
        Voronoi weights object
    """
    if voronoi is None:
        voronoi = EmptyVoronoiWeights()

    calc = HotCarriersCalculator(density_matrices=density_matrices,
                                 voronoi=voronoi,
                                 energies_occ=[],
                                 energies_unocc=[],
                                 sigma=None,
                                 )
    calc_kwargs = dict(yield_total_hcdists=False, yield_proj_hcdists=False)
    collector = TimeResultsCollector(calc, calc_kwargs)
    writer = HotCarriersWriter(collector, only_one_pulse=True)
    writer.calculate_and_save_npz(out_fname)
