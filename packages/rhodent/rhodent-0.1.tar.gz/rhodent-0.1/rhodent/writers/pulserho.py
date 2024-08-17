from __future__ import annotations

import numpy as np

from os import makedirs
from os.path import dirname

from gpaw.mpi import world
from gpaw.tddft.units import au_to_eV, au_to_fs

from ..density_matrices.time import ConvolutionDensityMatrices


def calculate_pulserho_and_save(pulserho_fmt: str,
                                density_matrices: ConvolutionDensityMatrices):
    """ Read density matrices in frequency space from disk, convolve with
    Gaussian laser pulse, and inverse Fourier transform to get a time domain response.

    Save the pulse density matrces for selected times in the simulation
    Read density matrices in frequency space from disk

    Parameters
    ----------
    pulserho_fmt
        The pulserho_fmt is a formatting string for the density matrices
        saved to disk. Example:

        pulserho_fmt =  'pulserho/t{time:09.1f}{tag}.npy'
    density_matrices
        Object that gives the density matrix in the time domain
    """
    dname = dirname(pulserho_fmt.format(time=0, tag='', pulsefreq=0, pulsefwhm=0))
    # Output directory
    if world.rank == 0:
        makedirs(dname, exist_ok=True)
    world.barrier()

    calc_comm = density_matrices.calc_comm
    log = density_matrices.log
    nlocaltot = len(density_matrices.local_work_plan)

    if world.rank == 0:
        log('Read frequency density matrix', flush=True)

    tags_keys = [(tag, key) for s, (tag, key) in enumerate(
        [('', 'rho_p'), ('-Iomega', 'drho_p'), ('-omega2', 'ddrho_p')]) if s in density_matrices.derivative_order_s]

    # Do convolution time-by-time
    for ndone, (work, dm) in enumerate(density_matrices, 1):
        pulse = work.pulse
        avg = log.elapsed('read')/ndone
        estrem = avg * (nlocaltot - ndone)
        log(f'Calculated t{work.time:09.1f} '
            f'Avg: {avg:10.3f}s ETA: {estrem:10.3f}s', flush=True)
        for tag, key in tags_keys:
            fname_kw = dict(time=work.time, tag=tag,
                            pulsefreq=pulse.omega0 * au_to_eV,
                            pulsefwhm=1 / pulse.sigma * au_to_fs * (2 * np.sqrt(2 * np.log(2))))
            fname = pulserho_fmt.format(**fname_kw)
            rho_p = getattr(dm, key)
            if calc_comm.rank == 0:
                assert isinstance(rho_p, np.ndarray)
                np.save(fname, rho_p)
