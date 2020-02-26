library(shiny)
library(leaflet)
library(data.table)

source(file.path(getwd(),"helper.R"))

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

fbs    <- fread("~/Documents/football/data/teams/fbsGeoData.csv", stringsAsFactors = F, data.table = F)
fcs    <- fread("~/Documents/football/data/teams/fcsGeoData.csv", stringsAsFactors = F, data.table = F)
divII  <- fread("~/Documents/football/data/teams/divIIGeoData.csv", stringsAsFactors = F, data.table = F)
divIII <- fread("~/Documents/football/data/teams/divIIIGeoData.csv", stringsAsFactors = F, data.table = F)
dfFBS  <- data.frame(lat = fbs$latitude, lng = fbs$longitude, div = "FBS", 
                     size = 3, color = 'red', name = fbs$name)
dfFCS  <- data.frame(lat = fcs$latitude, lng = fcs$longitude, div = "FCS", 
                     size = 2, color = 'blue', name = fcs$name)
dfDII  <- data.frame(lat = divII$latitude, lng = divII$longitude, div = "DII", 
                     size = 1, color = 'green', name = divII$name)
dfDIII <- data.frame(lat = divIII$latitude, lng = divIII$longitude, div = "DIII",
                     size = 1, color = 'black', name = divIII$name)
df <- rbind(dfFBS,dfFCS,dfDII,dfDIII)

filename <- file.path(paste(getwd(), "/data/rankings/", yearID, ".rData",sep = ""))
load(file = filename)
rankings <- oRankings
df[,"TeamName"] <- makeShortNames(df[,"name"])
df <- merge(df, rankings, by="TeamName")

#df    <- rbind(dfFBS,dfFCS)
  #df    <- dfFBS


ui <- fluidPage(
  leafletOutput("mymap"),
  absolutePanel(top = 10, right = 10,
                selectInput(inputId = "division", label = "Football Division",
                            choices = c("FBS", "FCS", "DII", "DIII")),
                checkboxInput("legend", "Show legend", TRUE)
  )
)

server <- function(input, output, session) {

  # Reactive expression for the data subsetted to what the user selected
  filteredData <- reactive({
    df[df$div == input$division,]
  })
  
  output$mymap <- renderLeaflet({
    fdata <- filteredData()
    tmp <- as.vector(fdata)
    print(dim(fdata))
    context <- paste(tail(paste(names(tmp),unname(tmp), sep = ": "), n=-7), collapse = "<BR>")
    leaflet(df) %>% addTiles() %>%
    fitBounds(~min(lng), ~min(lat), ~max(lng), ~max(lat)) %>%
    addCircleMarkers(lng = ~lng, lat = ~lat,
                     options = markerOptions(riseOnHover = T),
                     labelOptions = labelOptions(noHide = F),
                     radius = ~size, color = ~color)
  })
  
  # Incremental changes to the map (in this case, replacing the
  # circles when a new color is chosen) should be performed in
  # an observer. Each independent set of things that can change
  # should be managed in its own observer.
  
  observe({
    fdata <- filteredData()
    tmp <- as.vector(fdata)
    context <- paste(tail(paste(names(tmp),unname(tmp), sep = ": "), n=-7), collapse = "<BR>")
    print(context)
    leafletProxy("mymap", data = filteredData()) %>%
      clearShapes() %>%
      clearMarkers() %>%
      clearPopups() %>%
      addTiles() %>%
      fitBounds(~min(lng), ~min(lat), ~max(lng), ~max(lat)) %>%
      addCircleMarkers(lng = ~lng, lat = ~lat, popup = context,
                       popupOptions(zoomAnimation = T),
                       options = markerOptions(riseOnHover = T),
                       labelOptions = labelOptions(noHide = F),
                       radius = ~size, color = ~color)
  })
  
  # Show a popup at the given location
  showZipcodePopup <- function(zipcode, lat, lng) {
    print(zipcode)
    selectedZip <- df[df$name == zipcode,]
    content <- as.character(tagList(
      tags$h4("Score:", as.integer(selectedZip$size)),
      tags$strong(HTML(sprintf("%s, %s",
                               selectedZip$color, selectedZip$div))), tags$br(),
      sprintf("Median household income: %s", dollar(selectedZip$lat)), tags$br(),
      sprintf("Percent of adults with BA: %s%%", as.integer(selectedZip$lng)), tags$br(),
      sprintf("Adult population: %s", selectedZip$name)
    ))
    leafletProxy("mymap") %>% addPopups(lng, lat, content, layerId = zipcode)
  }
  
  # When map is clicked, show a popup with city info
  observe({
    leafletProxy("mymap") %>% clearPopups()
    event <- input$map_shape_click
    print(event)
    if (is.null(event))
      return()
    
    isolate({
      showZipcodePopup(event$id, event$lat, event$lng)
    })
  })
  
  observe({
    if (is.null(input$goto))
      return()
    isolate({
      map <- leafletProxy("mymap")
      map %>% clearPopups()
      dist <- 0.5
      zip <- input$goto$zip
      lat <- input$goto$lat
      lng <- input$goto$lng
      showZipcodePopup(zip, lat, lng)
      map %>% fitBounds(lng - dist, lat - dist, lng + dist, lat + dist)
    })
  })
  
}

shinyApp(ui, server)