getMVRankings <- function(mvdata) {
  writeLines(paste("Running MV-GLM with",nrow(mvdata),"games and",length(levels(mvdata[,"home"])),"teams."))
  method = "PB0"
  firstOrder = T
  homeField = T
  verbose = F
  mvModel <- mvglmmRank(mvdata, method = method, first.order = firstOrder, home.field = homeField, verbose = verbose, max.iter.EM = 1)
  
  score  <- mvModel$b.ratings
  totrdf <- sortRankings(score)
  
  offscore <- mvModel$p.ratings.offense 
  offrdf   <- sortRankings(offscore)
  
  defscore <- mvModel$p.ratings.defense
  defrdf   <- sortRankings(defscore)

  return( list("rank"=totrdf, "offrank"=offrdf, "defrank"=defrdf) )
}