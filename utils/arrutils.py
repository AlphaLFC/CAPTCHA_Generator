# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:24:22 2016

@author: alpha
"""

from __future__ import division

from scipy.ndimage import zoom
import numpy as np


def resize(ndarray, shape, dtype=np.float32):
    """Resize an ndarray.

    Parameters
    ----------
    ndarray : list or np.ndarray
    shape : list or tuple or int

    Returns
    -------
    resize np.ndarray
    """
    ndarray = np.array(ndarray, dtype=np.float32)
    arrshape = ndarray.shape
    if len(arrshape) == 1:
        assert type(shape) in [int, long] or len(shape) == 1, \
            '"shape" should be consistent with ndarray!'
    if type(shape) in [int, long] or len(shape) == 1:
        zoom_0 = shape/arrshape[0]
        return zoom(ndarray, zoom_0, output=dtype)
    else:
        assert len(shape) == len(arrshape), \
            '"shape" should be consistent with ndarray!'
        zooms = []
        for i, dim in enumerate(shape):
            zoom_tmp = dim/arrshape[i]
            zooms.append(zoom_tmp)
        return zoom(ndarray, zooms, output=dtype)


if __name__ == '__main__':
    a = np.array([[1, 2, 3, 4], [2, 3, 4, 5]])
    print a
    print resize(a, (3, 4))
