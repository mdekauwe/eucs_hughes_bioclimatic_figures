library(ALA4R)

ss = sites_by_species("genus:Eucalyptus",
                      wkt="POLYGON((110 -45,155 -45,155 -10,110 -10,110 -45))",
                      gridsize=0.5)

# convert coordinates to cell centres
ss$longitude = ss$longitude + 0.25
ss$latitude = ss$latitude + 0.25

# Get bioclimatic stuff
env_layers = c("Precipitation - annual", "Temperature - annual max mean")
ep = intersect_points(ss[, c("latitude","longitude")], env_layers)
df = na.omit(ep)
write.csv(df, file="Eucs_MAP_MAT.csv", sep=",")
