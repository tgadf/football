library(igraph)
library(graphics)
library(RColorBrewer)

csv <- "C:/Users/tgadfort/Dropbox/Football/2015.graph"
confdata <- "C:/Users/tgadfort/Dropbox/Football/2015.conf"
abrv <- "C:/Users/tgadfort/Dropbox/Football/Teams.csv"
if ( file.exists(csv) ) {
  cdata <- read.csv(csv)
} else {
  csv <- "~/Dropbox/Football/2015.graph"
  confdata <- "~/Dropbox/Football/2015.conf"
  abrv <- "~/Dropbox/Football/Teams.csv"
}

## Read data
confs <- read.csv(confdata, sep = "\t", header = FALSE)
confnames <- unique(confs$V2)
nconfs <- length(confnames)
cgraph <- read.csv(csv, sep = "\t", header = FALSE)
cgraph.network <- graph.data.frame(cgraph, directed=F)
abrvnames <- read.csv(abrv, sep = "\t", header = FALSE)


##
## Abreviations
##
shortnames <- as.character(abrvnames[,2])
names(shortnames) <- as.character(abrvnames[,1])
#shortnames <- as.character(shortnames)


##
## We need to get rid of tangential teams
##
bad.vs <- V(cgraph.network)[degree(cgraph.network) < 8]
cgraph.network <- delete.vertices(cgraph.network, bad.vs)
vertices <- V(cgraph.network)
vertexnames <- shortnames[names(vertices)]
print(names(vertices))
print(shortnames)
print(vertexnames)


## Margins
par(mai=c(0,0,1,1))

#vertex.label=NA,layout=layout.lgl)



## Colors
col=rainbow(nconfs)
#col=topo.colors(nconfs)
#col=cm.colors(nconfs)
#col=terrain.colors(nconfs)
#col=heat.colors(nconfs)
names(col) <- as.character(confnames)
v2 <- as.character(confs$V2)
cols <- col[v2]
#col=set3(nconfs)
#col=brewer.pal(nconfs,"Dark2")
#pause()

textcol <- col
for ( i in seq_along(col) ) {
  cval <- (i + 4) %% length(col) + 1
  textcol[[i]] <- col[[cval]]
  print(paste(i,v2[[i]]))
}
labelcolors <- rep('black', length(cols))
print(labelcolors)
#pause()


print(cols)
#pause()

V(cgraph.network)$color <- cols
V(cgraph.network)$size <- 10
E(cgraph.network)$weight <- edge.betweenness(cgraph.network)
bordercolor <- "blue"
#labelcolor <- "black"
labelsize <- 0.6


sconfnames <- list("MWC", "MAC", "SEC", "Sun", "P12", "Ind", "B12", "ACC", "Ame", "CUSA", "B10")
names(sconfnames) <- confnames


##
## Plot everything
##
plot(cgraph.network, layout=layout.fruchterman.reingold,
     vertex.label=vertexnames,
     vertex.frame.color=bordercolor,
     vertex.label.font=2,
     edge.lty=4,
     vertex.label.color=labelcolors,
     vertex.label.cex=labelsize,
     main="Connectivity of College Football Teams in 2015")

##
## Add legend
##
#legend(1.05, -0.405, unique(confs$V2), cex=1.2, col=col, pch=19, ncol=1, yjust=0, lty=0)
legend(1.25, -.805, unique(confs$V2), cex=1.2, col=col, pch=19, yjust=0, lty=0)
