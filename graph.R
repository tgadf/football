getTeamPageRank <- function(grModel, samples = 10) {
  writeLines(paste("Running PageRank on a graph with",length(E(grModel)),"edges and",length(V(grModel)),"vertices"))
  
  dampings <- runif(samples)
  ul    <- unlist(sapply(dampings, function(x) page_rank(grModel, directed = T, damping = x))["vector",])
  score <- sort(tapply(ul, names(ul), function(x) mean(x)))
  rdf   <- sortRankings(score)
  return( list("rank"=rdf) )
}

getTeamCloseness <- function(grModel) {
  # Cloness centrality measures how many steps is required to access 
  # every other vertex from a given vertex.
  clIn  <- closeness(grModel, mode = "in")
  clOut <- closeness(grModel, mode = "out")
  return( cl )
}

getTeamBetweenness <- function(grModel) {
  # The vertex and edge betweenness are (roughly) defined by the number of 
  # geodesics (shortest paths) going through a vertex or an edge.
  btn <- betweenness(grModel)
  return( btn )
}

getTeamDegree <- function(grModel) {
  # The degree of a vertex is its most basic structural property, 
  # the number of its adjacent edges.
  # 'total' equals number of games
  # 'in' equals wins
  # 'out' equals losses
  dgTot <- degree(grModel, mode = "total")
  dgIn  <- degree(grModel, mode = "in")
  dgOut <- degree(grModel, mode = "out")
  return( dgIn )
}

getTeamSimilarity <- function(grModel) {
  # These functions calculates similarity scores for vertices based 
  # on their connection patterns.
  # 'total' equals number of games
  # 'in' equals wins
  # 'out' equals losses
  # method <- c("jaccard", "dice", "invlogweighted")
  simDice <- similarity(grModel, method = "dice")
  simJacc <- similarity(grModel, method = "jaccard")
  simInvl <- similarity(grModel, method = "invlogweighted")
  
  simVal <- simDice
  
  # Set diagonal to zero since that is the self term
  diag(simVal) <- 0
  return( simVal )
}

getEigenCentrality <- function(grModel) {
  # eigen_centrality takes a graph (graph) and returns the 
  # eigenvector centralities of positions v within it
  ecent <- eigen_centrality(grModel)
  return( ecent )
}

getAlphaCentrality <- function(grModel) {
  # alpha_centrality calculates the alpha centrality of some (or all) vertices in a graph.
  acent <- alpha_centrality(grModel)
  return( acent )
}

getAuthorityScore <- function(grModel) {
  # The authority scores of the vertices are defined as the principal eigenvector of t(A)*A, 
  # where A is the adjacency matrix of the graph.
  # Kleinberg's authority score
  ascore <- authority.score(grModel)[["vector"]]
  return( ascore )
}

getHubScore <- function(grModel) {
  # The hub scores of the vertices are defined as the principal eigenvector of A*t(A), 
  # where A is the adjacency matrix of the graph.
  # Kleinberg's hub score (low is good)
  hscore <- hub.score(grModel)[["vector"]]
  return( hscore )
}

getReach <- function(grModel, nsize=2) {
  if ( nsize >= 2 ) {
    reach <- vector(length=vcount(grModel))
    for (i in 1:vcount(grModel)){
      n <- neighborhood(grModel, order = nsize, nodes=i)
      ni <- unlist(n)
      l <- length(ni)
      reach[i] <- (l)/vcount(grModel)
    }
  } else {
    # distance-weighted reach:
    distances <- shortest.paths(grModel) #create matrix of geodesic distances
    diag(distances) <- 1 # replace the diagonal with 1s
    weights <- 1/distances # take the reciprocal of distances
    reach <- apply(weights,1,sum) # sum for each node (row)
  }
  names()
  return( reach )
}

getTeamSimRank <- function(grModel) {
  writeLines(paste("Running SimRank on a graph with",length(E(grModel)),"edges and",length(V(grModel)),"vertices"))
  edgeList <- get.edgelist(grModel)
  
  # convert an edgelist to conflict matrix
  writeLines("  Create conflict matrix")
  confmatrix <- as.conflictmat(edgeList)
  
  # find dominance probability matrix
  writeLines("  Create conductance")
  perm <- conductance(confmatrix, maxLength = 2)
  
  # find information gain
  writeLines("  Create information gain")
  infGain <- perm$imputed.conf - confmatrix
  
  # generating a heatmap representing information gained by 
  # using informatio from indirect pathways.
  # plotConfmat(informationGain, ordering = NA, labels = TRUE)
  
  #writeLines("  Create transitivity")
  #conftrans <- transitivity(confmatrix, strict = FALSE)
  
  ## Not run: 
  # Note: It takes a while to run the simRankOrder example.
  writeLines("  Create sim rank order")
  s.rank <- simRankOrder(perm$p.hat, num = 3, kmax = 10)
  #s.rank$BestSimulatedRankOrder
  #s.rank$Costs
  #s.rank$AllSimulatedRankOrder
  
  # plotConfmat(perm$p.hat, ordering = s.rank[[1]]$ID, labels = TRUE)
  
  #Fushing, H., McAssey, M. P., Beisner, B., & McCowan, B. (2011). 
  #Ranking network of a captive rhesus macaque society: 
  #a sophisticated corporative kingdom. PLoS One, 6(3), e17817-e17817.
  
  writeLines("  Create ordered list")
  orderedList <- rev(s.rank$BestSimulatedRankOrder$ID)
  rank <- seq(orderedList)
  names(rank) <- as.character(orderedList)


  # Team Dominance Probability
  teamProb <- individualDomProb(perm$p.hat)
  teamProb <- teamProb[order(teamProb$Mean, decreasing = T),]
  
  rdf   <- sortRankings(rank, rev = T)
  #pdf   <- sortRankings(teamProb)
  
  return( list("rank"=rdf, "prob"=pdf) )
}