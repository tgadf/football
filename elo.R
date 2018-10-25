getELORankings <- function(elodata) {
  writeLines(paste("Running ELO with",nrow(elodata),"games and",length(unique(elodata[,"HomeTeam"])),"teams."))
  eloModel <- elo(x = elodata, history = T)
  
  score        <- eloModel$ratings$Rating
  names(score) <- eloModel$ratings$Player
  
  rdf <- sortRankings(score)
  return( list("rank"=rdf) )
}

getFideRankings <- function(fidedata) {
  writeLines(paste("Running Fide with",nrow(fidedata),"games and",length(unique(fidedata[,"HomeTeam"])),"teams."))
  fideModel <- fide(x = fidedata, history = T)

  fideRank    <- fideModel$ratings$Rating
  fideOppRank <- fideModel$ratings$Opponent
  names(fideRank) <- fideModel$ratings$Player
  names(fideOppRank) <- fideModel$ratings$Player
  
  rdf    <- sortRankings(fideRank)
  opprdf <- sortRankings(fideOppRank)
  return( list("rank"=rdf, "opprank"=opprdf) )
}