####
## Download all occurances of Eucs from ALA and get the matching MAP and MAT
## Date: 14/11/2017
## Author: Martin De Kauwe
####
library(ALA4R)

ss = sites_by_species("genus:Eucalyptus",
                      wkt="POLYGON((110 -45,155 -45,155 -10,110 -10,110 -45))",
                      gridsize=0.5)

# convert coordinates to cell centres
ss$longitude = ss$longitude + 0.25
ss$latitude = ss$latitude + 0.25

# Get bioclimatic stuff
env_layers = c("WorldClim: Temperature - annual mean",
               "WorldClim: Precipitation - annual")
ep = intersect_points(ss[, c("latitude","longitude")], env_layers)
ep$worldClimTemperatureAnnualMean = ep$worldClimTemperatureAnnualMean / 10.0

# get just the species names
species_names <- ss[,-c(1,2)]

t_spread <- vector(length=length(species_names))
for(i in 1:ncol(species_names)) {
  ind <- which(species_names[,i] > 0)
  t_range <- range(ep$worldClimTemperatureAnnualMean[ind], na.rm=TRUE)

  if (is.finite(t_range[2])) {
    maxx = t_range[2]
  } else {
      maxx = NA
  }

  if (is.finite(t_range[1])) {
    minx = t_range[1]
  } else {
    minx = NA
  }

  t_spread[i] <- maxx - minx
}


bins <- seq(1, 11, by=1)
bin_count <- vector(length=length(bins))
for (b in 1:length(bins)) {

  if (b == 1) {
    bin_count[b] <- length(which(t_spread <= bins[b]))
  } else if (b==length(bins)) {
    bin_count[b] <- length(which(t_spread > bins[b-1]))
  } else {
    bin_count[b] <- length(which(t_spread > bins[b-1] & t_spread <= bins[b]))
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
