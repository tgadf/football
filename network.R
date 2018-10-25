library(tidyr)
library(dplyr)
library(tibble)
library(igraph)
library(visNetwork)
library(RColorBrewer)


loadNodes <- function(yearID) {
  filename <- file.path(paste("~/Documents/football/data/network/", yearID, ".nodes.csv",sep = ""))
  nodes    <- read.csv(filename, header = T)
  # colnames(nodes) <- "id"
  ## "id" : id of the node, needed in edges information
  ## "label" : label of the node
  ## "group" : group of the node. Groups can be configure with visGroups
  ## "value" : size of the node
  ## "title" : tooltip of the node
  writeLines(paste("Found",nrow(nodes),"nodes."))
  return( nodes )
}


loadEdges <- function(yearID) {
  filename <- file.path(paste("~/Documents/football/data/network/", yearID, ".edges.csv",sep = ""))
  edges    <- read.csv(filename, header = T)
  # colnames(edges) <- c("from", "to")
  ## "from" : node id of begin of the edge
  ## "to" : node id of end of the edge
  ## "label" : label of the edge
  ## "value" : size of the node
  ## "title" : tooltip of the node
  writeLines(paste("Found",nrow(edges),"edges."))
  return( edges )
}

yearID <- '2016'
edges  <- loadEdges(yearID)
nodes  <- loadNodes(yearID)

domains <- unique(nodes$group)
lnodes <- data.frame(label = domains, shape = c("dot"))
shape <- "square"
domainshape <- "dot"

if ( F ) {
visEdges(width=4, color = list(color = "lightblue", highlight = "navy"))
}

visNetwork(nodes = nodes, edges = edges, main = "2016 FBS Network",
           height = "725", width = "1150") %>%
  visNodes(font = list(size = 48)) %>%
  visLegend() %>%
  addFontAwesome() %>%
  visLayout(randomSeed =21, improvedLayout = TRUE) %>%
  visOptions(highlightNearest = list(enabled = F, degree = 1, hover = T), nodesIdSelection = F) %>%
  visPhysics(solver = "forceAtlas2Based", forceAtlas2Based = list(gravitationalConstant = -50)) %>%
  visInteraction(navigationButtons = TRUE)
#addNodes = lnodes, useGroups = T)