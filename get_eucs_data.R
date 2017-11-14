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
x <- ss[,-c(1,2)]

# make a massive object that I can play with in python
df = cbind(ep, x)
#df = na.omit(ep)
write.csv(df, file="Eucs_MAP_MAT.csv", sep=",")


#count =sapply(1:nrow(x), function(y) length(which(x[y,]>0)))

t_spread <- vector(length=ncol(x))
for(s in 1:ncol(x)) {
  ind <- which(x[,s] > 0)
  t_range <- range(ep$worldClimTemperatureAnnualMean[ind], na.rm=TRUE)
  t_spread[s] <- t_range[2] - t_range[1]
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

print(bin_count)

#ep = cbind(ep, count)
#df = na.omit(ep)
#write.csv(df, file="Eucs_MAP_MAT.csv", sep=",")
