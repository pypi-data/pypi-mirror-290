from __future__ import annotations

import numpy as np

fast_pad_nice_factors = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 8096])


def fast_pad(nt: int) -> int:
    """ Return a length that is at least twice as large as the given input,
    and the FFT of data of such length is fast
    """
    padnt = 2 * nt
    insert = np.searchsorted(fast_pad_nice_factors, padnt)
    if insert <= len(fast_pad_nice_factors):
        padnt = fast_pad_nice_factors[insert]
    assert padnt >= 2 * nt
    return padnt
