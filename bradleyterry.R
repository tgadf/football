getBradleyTerryRankings <- function(btdata) {
  writeLines(paste("Running Bradley-Terry with",nrow(btdata),"games and",length(levels(btdata[,"home.team"])),"teams."))
  btModel <- BTm(cbind(home.score, away.score), home.team, away.team,
                 data = btdata, id = "team")
  btAbility <- data.frame(BTabilities(btModel))
  abilities <- btAbility[,"ability"]
  sigmas    <- btAbility[,"s.e."]
  names(abilities) <- rownames(btAbility)
  names(sigmas)   <- rownames(btAbility)

  score <- abilities
  rdf <- sortRankings(score)
  
  probs <- getTeamMatchupProbabilities(abilities)
  
  return( list("rank"=rdf, "sigmaRank"=sigmas, "prob"=probs) )
}

getTeamMatchupProbabilities <- function(abilities) {
  require(reshape2)
  probs       <- outer(abilities, abilities, prob_BT)
  diag(probs) <- 0 # set to 0.5 nominally
  probs       <- melt(probs)
  
  colnames(probs) <- c("Team", "Opponent", "Probability")
  return( probs )
}


##############################################################################
##
## Bradley-Terry Model Helpers
##
##############################################################################
btAnalysis <- function(abilities) {
  barplot(sort(abilities, decreasing = T), las=2, cex.names = 0.3)
  probs <- getTeamMatchupProbabilities(abilities)
  heatmap_grid_probs(probs)
  createTeamProbabilityHistogram(probs, "Alabama")
}

inv_logit <- function(p) {
  exp(p) / (1 + exp(p))
}

prob_BT <- function(ability_1, ability_2) {
  inv_logit(ability_1 - ability_2)
}


heatmap_grid_probs <- function(probs, num_breaks = 7, title = "") {
  require(ggplot2)
  breaks <- with(probs, quantile(Probability[Probability > 0],
                                 probs = seq(0, 1, length = num_breaks),
                                 names = FALSE))
  breaks <- c(0, breaks, 1)
  probs$cuts <- cut(probs$Probability, breaks = breaks, dig = 2, ordered = TRUE, right = FALSE)
  p <- ggplot(probs, aes(x = Team, y = Opponent, z = cuts, color = cuts))
  p <- p + geom_tile(aes(fill = cuts))
  p <- p + scale_fill_brewer(palette = "Blues")
  p + ggtitle(title)
}

createTeamProbabilityHistogram <- function(teamProbabilities, teamName) {
  # Probability that the top-ranked team, Alabama, beats each team
  Ala_probs <- subset(teamProbabilities, Team == teamName & Opponent != teamName)
  p <- ggplot(Ala_probs, aes(x = Opponent)) + geom_bar(aes(weight = Probability))
  p <- p + ylab("Probability") + theme_bw()
  p <- p + geom_hline(aes(yintercept = 0.5), color = "red")
  p + ggtitle(paste("Probability of",teamName,"Beating Other Opponents"))
}