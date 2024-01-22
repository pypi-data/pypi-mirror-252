#! /usr/bin/env python

# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

from detkit.datasets import electrocardiogram
import os
import sys

import warnings
warnings.resetwarnings()
warnings.filterwarnings("error")


# ===========
# remove file
# ===========

def remove_file(filename):
    """
    Remove file.
    """

    if os.path.exists(filename):
        os.remove(filename)


# ======================
# test electrocardiogram
# ======================

def test_electrocardiogram():
    """
    Test for `electrocardiogram` function.

    Note that this test can only be done on Python 3.8 and above.
    """

    # Find Python version
    py_major = sys.version_info.major
    py_minor = sys.version_info.minor

    # This test can only be done on Python 3.8 and above.
    if (py_major < 3) or (py_minor < 8):
        return

    electrocardiogram(start=0.0, end=10.0, bw_window=0.5, freq_cut=45,
                      plot=True, plot_bw=False)
    electrocardiogram(start=0.0, end=10.0, bw_window=0.5, freq_cut=45,
                      plot=True, plot_bw=True)

    remove_file('electrocardiogram.svg')
    remove_file('electrocardiogram.pdf')


# ===========
# Script main
# ===========

if __name__ == "__main__":
    test_electrocardiogram()
