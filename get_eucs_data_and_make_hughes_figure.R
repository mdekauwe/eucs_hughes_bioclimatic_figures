####
## Download all occurances of Eucs from ALA and get the matching MAP and MAT
## Then remake Fig 1 in Hughes et al. (1996) Climatic Range Sizes of
## Eucalyptus Species in Relation to Future Climate Change. Global Ecology and
## Biogeography Letters, 5, 23-29
##
## Date: 15/11/2017
## Author: Martin De Kauwe
####

library(ALA4R)
library(dplyr)
library(stringi)

# for every species, get range of MAT
get_MAT_range <- function(species_name, sep){

  # extract MAT where the species occurs at all
  counts <- sep[,species_name]
  mats <- sep$worldClimTemperatureAnnualMean[which(counts > 1)]
  #print(c(sum(counts), min(mats, na.rm=TRUE), max(mats, na.rm=TRUE)))
  if(length(mats)){
    #print(c(stri_trim_both(species_name), min(mats, na.rm=TRUE), max(mats, na.rm=TRUE)))
    # Return temp range of species
    if (min(mats, na.rm=TRUE) < 0.001) {
      NA
    } else {
      max(mats, na.rm=TRUE) - min(mats, na.rm=TRUE)
      #print(min(mats, na.rm=TRUE))
    }
  } else {
    NA
  }

}

# Get all the counts of Eucs occurrences
ss = sites_by_species("genus:Eucalyptus",
                      wkt="POLYGON((110 -45,155 -45,155 -10,110 -10,110 -45))",
                      gridsize=0.5)

ss <- mutate(ss, longitude = longitude + 0.25,
             latitude = latitude + 0.25)

# Get bioclimatic stuff
env_layers = c("WorldClim: Temperature - annual mean",
               "WorldClim: Precipitation - annual")
ep = intersect_points(ss[, c("latitude","longitude")], env_layers)
ep$worldClimTemperatureAnnualMean = ep$worldClimTemperatureAnnualMean / 10.0

# For each species figure out the temperature range it occurs in
sep <- cbind(ss, ep)
species_names <- grep("eucalyptus", names(sep), value=TRUE)
temp_range <- sapply(species_names, get_MAT_range, sep=sep)

# Exclude crap data
temp_range <- temp_range[is.finite(temp_range)]

# Exclude single point data, where there is no range
temp_range <- temp_range[temp_range > 0.0]

# Figure out the histogram
bins <- seq(1, 11, by=1)
bin_count <- vector(length=length(bins))
for (b in 1:length(bins)) {

  if (b == 1) {
    bin_count[b] <- length(temp_range[temp_range <= 1.0])
  } else if (b==length(bins)) {
    bin_count[b] <- length(temp_range[temp_range > bins[b-1]])
  } else {
    bin_count[b] <- length(temp_range[(temp_range > bins[b-1]) &
                                      (temp_range <= bins[b])])
  }

}

total <- sum(bin_count)
bin_count <- bin_count / total * 100.

pdf("Hughes_figure_ALA.pdf", width=9, height=6)
names(bin_count) <- c("<1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
                      "8-9", "9-10", ">10")
xlab <- expression("Mean annual temperature range " ( degree~C))
ylab <- "% Species"
barplot(bin_count, xlab=xlab, ylab=ylab)
dev.off()
