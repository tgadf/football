getMasseyRankings <- function(msydata) {
  writeLines(paste("Running Massey with",nrow(msydata),"games and",length(unique(msydata[,"team1"])),"teams."))

  ## Get season data
  num_teams <- length(unique(c(msydata$team1, msydata$team2)))
  num_games <- nrow(msydata)
  teams <- unique(c(msydata$team1, msydata$team2))
  
  ## Construct matchup matrix
  X <- matrix(0, nrow=num_teams, ncol=num_teams)
  for(i in 1:nrow(msydata)){
    h <- match(msydata$team1[i], teams)
    a <- match(msydata$team2[i], teams)
    X[h, a] <- X[h, a] - 1
    X[a, h] <- X[a, h] - 1
  }
  
  for(i in 1:nrow(X)){
    X[i, i] <- abs(sum(X[i, ]))
  }
  X[nrow(X), ] <- 1
  
  ## Construct results vector
  y <- sapply(teams, function(x, msydata){
    home <- subset(msydata, team1 == x)
    away <- subset(msydata, team2 == x)
    goals_for <- sum(home$team1_goals) + sum(away$team2_goals)
    goals_away <- sum(home$team2_goals) + sum(away$team1_goals)
    goals_for - goals_away
  }, msydata=msydata)
  y[length(y)] <- 0
  
  goals_for <- sapply(teams, function(x, msydata){
    home <- subset(msydata, team1 == x)
    away <- subset(msydata, team2 == x)
    home_goals <- sum(home$team1_goals)
    away_goals <- sum(away$team2_goals)
    home_goals + away_goals
  }, msydata=msydata)
  
  ratings <- solve(X, y)
  names(ratings) <- teams
  
  g <- matrix(0, nrow=num_teams, ncol=num_teams)
  for(i in 1:nrow(msydata)){
    h <- match(msydata$team1[i], teams)
    a <- match(msydata$team2[i], teams)
    g[h, a] <- g[h, a] + 1
    g[a, h] <- g[a, h] + 1
  }
  for(i in 1:nrow(g)){
    g[i, i] <- sum(g[i, ])
  }
  
  grpf <- as.data.frame((diag(g) * ratings) - goals_for)
  row.names(grpf) <- teams
  
  def_ratings <- solve(g, grpf[ ,1])
  off_ratings <- ratings - def_ratings
  names(def_ratings) <- teams

  score <- ratings
  rdf   <- sortRankings(score)
  
  offscore <- off_ratings
  offrdf   <- sortRankings(offscore)
  
  defscore <- def_ratings
  defrdf   <- sortRankings(defscore)
  
  return( list("rank"=rdf, "offrank"=offrdf, "defrank"=defrdf) )
}