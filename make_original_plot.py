#!/usr/bin/env python

"""
Remake Fig 1 in Hughes et al. (1996) Climatic Range Sizes of
Eucalyptus Species in Relation to Future Climate Change. Global Ecology and
Biogeography Letters, 5, 23-29. I've extracted the points using datathief

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (20.11.2017)"
__email__ = "mdekauwe@gmail.com"

import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

def main():

    fname = "hughes_datathief.csv"
    df = pd.read_csv(fname)

    fig = plt.figure(figsize=(9,6))
    fig.subplots_adjust(hspace=0.3)
    fig.subplots_adjust(wspace=0.2)
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['font.size'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12

    ax = fig.add_subplot(111)
    ind = np.arange(11)
    plt.bar(ind, df.percent, color="grey")

    plt.plot(ind, np.cumsum(df.percent), "k-o")
    ax.set_xticks(ind)
    ax.set_xticklabels(["<1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
                        "8-9", "9-10", ">10"])
    ax.set_ylabel(r'% Species')
    ax.set_xlabel("Mean annual temperature range ($^\circ$C)")
    fig.savefig("hughes_fig.pdf", bbox_inches='tight', pad_inches=0.1)


if __name__ == "__main__":

    main()
