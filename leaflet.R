getGeoData <- function(teamData) {
  require(ggmap)
  test    <- geocode(location = teamData[,"FullName"], output = "all")
  results <- as.data.frame(t(sapply(test, function(x) c(x[["results"]][[1]][["geometry"]][["location"]], x[["results"]][[1]][["formatted_address"]]))))
  colnames(results) <- c("Latitude", "Longitude", "Address")
  
  name      <- as.character(teamData[,"FullName"])
  address   <- as.character(unlist(results[,"Address"]))
  longitude <- unlist(results[,"Longitude"])
  latitude  <- unlist(results[,"Latitude"])
  results   <- data.frame(name,latitude,longitude,address)
  return( results )
}

### Draw map of US
library(maps)
mapStates = map("state", fill = TRUE, plot = FALSE)
leaflet(data = mapStates) %>% addTiles() %>%
  addPolygons(fillColor = topo.colors(10, alpha = NULL), stroke = FALSE)


if ( !exists("dfFBS") ) {
  fbs    <- fread("~/Documents/football/data/teams/fbsGeoData.csv", stringsAsFactors = F, data.table = F)
  fcs    <- fread("~/Documents/football/data/teams/fcsGeoData.csv", stringsAsFactors = F, data.table = F)
  divII  <- fread("~/Documents/football/data/teams/divIIGeoData.csv", stringsAsFactors = F, data.table = F)
  divIII <- fread("~/Documents/football/data/teams/divIIIGeoData.csv", stringsAsFactors = F, data.table = F)
  #fbs <- read.csv("~/Documents/football/data/teams/fbsGeoData.csv")
  
  #m = leaflet() %>% addTiles()
  dfFBS = data.frame(lat = fbs$latitude, lng = fbs$longitude, size = 3, color = 'red', name = fbs$name)
  dfFCS = data.frame(lat = fcs$latitude, lng = fcs$longitude, size = 2, color = 'blue', name = fcs$name)
  dfDII = data.frame(lat = divII$latitude, lng = divII$longitude, size = 1, color = 'green', name = divII$name)
  dfDIII = data.frame(lat = divIII$latitude, lng = divIII$longitude, size = 1, color = 'black', name = divIII$name)
  df <- rbind(dfFBS,dfFCS,dfDII,dfDIII)
}
m = leaflet(df) %>% addTiles()
#m %>% addCircleMarkers(radius = ~size, color = ~color, fill = FALSE)
m %>% addCircleMarkers(lng = ~lng, lat = ~lat,
                       label = ~name,
                       options = markerOptions(riseOnHover = T),
                       labelOptions = labelOptions(noHide = F),
                       radius = ~size, color = ~color)
#m %>% addMarkers(lng = ~lng, lat = ~lat, label = ~name,
#                 options = markerOptions(riseOnHover = T),
#                 labelOptions = labelOptions(noHide = F))
#m %>% addPopups(lng = ~lng, lat = ~lat, ~name, options = popupOptions(closeButton = FALSE))