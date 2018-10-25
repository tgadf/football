getColleyRankings <- function(clygames) {
  writeLines(paste("Running Colley with",nrow(clygames),"games and",length(unique(c(clygames[,"WinTeam"],clygames[,"LossTeam"]))),"teams."))

  # Construct undirected graph
  clygames[,"WinTeam"] <- as.character(clygames[,"WinTeam"])
  clygames[,"LossTeam"] <- as.character(clygames[,"LossTeam"])
  gr <- graph_from_edgelist(cbind(clygames[,"WinTeam"], clygames[,"LossTeam"]), directed = T)
  
  
  # Construct colley matrix
  #   C_{ij} = -1 if played, 0 if not played
  #   C_{ii} = 2 + games played
  adjMat <- as.matrix(as_adjacency_matrix(as.undirected(gr), type = "both"))
  colleyMat <- replace(adjMat, adjMat == 1, -1)
  diag(colleyMat) <- 2 + degree(gr)
  
  
  # Contruct results vector
  #   b_{i} = 1 + nW_{i} − nL_{i})/2
  b <- 1 + (degree(gr, mode = "in") - degree(gr, mode = "out"))/2.0

  
  # Solve for rankings
  score <- solve(colleyMat, b)
  #rankings <- sort(rankings, decreasing = F)
  rdf <- sortRankings(score, rev=T)
  
  return( list("rank"=rdf) )
}