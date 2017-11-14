#!/usr/bin/env python

"""
Make Fig 1 & 2 from Hughes et al. (1996) Global Ecology and
Biogeography Letters, 5, 23-29.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (14.11.2017)"
__email__ = "mdekauwe@gmail.com"

import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np
import os


def main(fname):

    df = pd.read_csv(fname)
    #print(df)
    #print(list(df))

    print(df["eucalyptusMarginata"])

if __name__ == "__main__":

    fname = "Eucs_MAP_MAT.csv"
    main(fname)
