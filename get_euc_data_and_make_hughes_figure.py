#!/usr/bin/env python

"""
Download all occurances of Eucs from ALA and get the matching  MAT
Then remake Fig 1 in Hughes et al. (1996) Climatic Range Sizes of
Eucalyptus Species in Relation to Future Climate Change. Global Ecology and
Biogeography Letters, 5, 23-29

Search query:
http://biocache.ala.org.au/ws/occurrences/index/download?reasonTypeId=10&q=text%3AEucalyptus+country%3AAustralia+basis_of_record%3AHumanObservation&fq=geospatial_kosher%3A%22true%22


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

    (matx, latitudes, longitudes) = get_mat_data()

    fname = "data.csv"
    df = pd.read_csv(fname)

    df = df[df['Occurrence status assumed to be present'] == True]

    # Bin the locations into 0.5-degree grid cells
    #df["Latitude - processed"] = round(df["Latitude - processed"]*2.) / 2.
    #df["Longitude - processed"] = round(df["Longitude - processed"]*2.) / 2.

    df.rename(columns={'Species - matched': 'Species',
                       'Latitude - processed': 'Latitude',
                       'Longitude - processed': 'Longitude',}, inplace=True)

    df = df[["Species", "Latitude", "Longitude"]]

    # clean up dataframe
    df = df[df['Species'] != '']
    df.dropna(subset=['Species'], inplace=True)
    search_for = ['Eucalyptus']
    df = df[df.Species.str.contains('|'.join(search_for))]

    #df.to_csv("eucs.csv", index=False)

    names = np.unique(df.Species)

    total_count = 0
    species_count = {}
    speices_range = {}
    speices_names = []
    for spp in names:
        df_sp = df[df["Species"] == spp]
        spp_count = len(df_sp)

        if spp_count > 1:
            vals = []
            lats_needed = df_sp["Latitude"].values
            lons_needed = df_sp["Longitude"].values
            Tmin = 99999.
            Tmax = -99999.
            for i in range(len(df_sp)):
                latx = float(x_round(float(lats_needed[i])))
                lonx = float(x_round(float(lons_needed[i])))
                r = np.where(latitudes==latx)
                c = np.where(longitudes==lonx)
                mat = matx[r,c][0][0]
                vals.append(mat)
                if mat > Tmax:
                    Tmax = mat
                if mat < Tmin:
                    Tmin = mat
            Trange = Tmax - Tmin

            vals = np.asarray(vals)
            #P = np.percentile(vals, [2.5, 97.5])
            #vals = vals[(P[0] < vals) & (P[1] > vals)]

            # tests for outliers use the median absolute deviation rather than
            # percentile
            vals = vals[~is_outlier(vals)]
            if len(vals) == 0:
                continue
            else:
                Trange = np.max(vals) - np.min(vals)
                spp_count = len(vals)

                if Trange > 10:

                    from mpl_toolkits.basemap import Basemap
                    m = Basemap(projection='cyl', llcrnrlon=110., llcrnrlat=-45.,
                                urcrnrlon=155.,urcrnrlat=-10., resolution='c')


                    m.drawcoastlines()
                    x,y = m(lons_needed, lats_needed)
                    m.plot(x, y, 'bo', markersize=5)
                    ofname = spp.replace(" ", "_") + ".png"
                    plt.savefig(os.path.join("/Users/mdekauwe/Desktop", ofname),
                                dpi=100)
                    #plt.show()
                    plt.gcf().clear()

                # Exclude values of zero
                if (Trange > 0.00001):
                    speices_names.append(spp)
                    species_count[spp] = {}
                    speices_range[spp] = {}
                    species_count[spp] = spp_count
                    total_count += spp_count
                    speices_range[spp] = Trange

    #for spp in speices_names:
    #    print(spp, species_count[spp], speices_range[spp])

    # Figure out the histogram
    bin_count = np.zeros(11)

    for spp in speices_names:
        Trange = speices_range[spp]

        if Trange <= 1.0:
            bin_count[0] += species_count[spp]
        elif Trange > 1.0 and Trange <= 2.0:
            bin_count[1] += species_count[spp]
        elif Trange > 2.0 and Trange <= 3.0:
            bin_count[2] += species_count[spp]
        elif Trange > 3.0 and Trange <= 4.0:
            bin_count[3] += species_count[spp]
        elif Trange > 4.0 and Trange <= 5.0:
            bin_count[4] += species_count[spp]
        elif Trange > 5.0 and Trange <= 6.0:
            bin_count[5] += species_count[spp]
        elif Trange > 6.0 and Trange <= 7.0:
            bin_count[6] += species_count[spp]
        elif Trange > 7.0 and Trange <= 8.0:
            bin_count[7] += species_count[spp]
        elif Trange > 8.0 and Trange <= 9.0:
            bin_count[8] += species_count[spp]
        elif Trange > 9.0 and Trange <= 10.0:
            bin_count[9] += species_count[spp]
        #elif Trange > 10.0:
        #    bin_count[10] += species_count[spp]

    bin_count = bin_count / total_count * 100.

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
    plt.bar(ind, bin_count)
    ax.set_xticks(ind)
    ax.set_xticklabels(["<1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
                        "8-9", "9-10", ">10"])
    ax.set_ylabel(r'% Species')
    ax.set_xlabel("Mean annual temperature range ($^\circ$C)")
    plt.show()

def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh

def get_mat_data():
    # Get MAT data
    nrows = 360
    ncols = 720
    latitudes = np.linspace(-89.75, 89.75, nrows)
    longitudes = np.linspace(-179.75, 179.75, ncols)
    fname = "/Users/mdekauwe/research/CRU_TS_v4_bioclim_MAT_MAP_AI/MAT_1960_2010.bin"
    matx = np.fromfile(fname).reshape(nrows, ncols)

    return (matx, latitudes, longitudes)

def x_round(x):
    # Need to round to nearest .25 or .75 to match the locations in CRU
    val = round(x * 4.0) / 4.0
    valx = str(val).split(".")
    v1 = valx[0]
    v2 = valx[1]

    if v2 <= "25":
        v2 = "25"
    else:
        v2 = "75"
    valx = float("%s.%s" % (v1, v2))

    return (valx)


if __name__ == "__main__":

    main()
