require(BradleyTerry2)
require(ProjectTemplate)
require(mvglmmRank)
require(PlayerRatings)
#require(sna)
#install_github("mhahsler/rMSA")
require(igraph)
require(Perc)

setwd("~/Documents/football/")
files <- c("massey.R", "colley.R", "offdef.R", "graph.R", "bradleyterry.R", "elo.R", "mvglm.R", "helper.R")
for ( file in files ) {
  fname <- file.path(getwd(), file)
  stopifnot(file.exists(fname))
  source(fname)
}


##############################################################################
##
## Bradley-Terry Model
##
##############################################################################
loadBTGames <- function(yearID) {
  filename <- file.path(paste(getwd(), "/data/network/", yearID, ".btdata.csv",sep = ""))
  writeLines(paste("Reading data from",filename))
  games    <- read.csv(filename, header = T)
  writeLines(paste("  Found",nrow(games),"games."))
  return( games )
}

setBTOutcomes <- function(games) {
  return( games )
}

createBTModel <- function(btdata) {
  rankings <- getBradleyTerryRankings(btdata)
  return( rankings )
}


##############################################################################
##
## MV GLM mRank Model
##
##############################################################################
loadMVGames <- function(yearID) {
  filename <- file.path(paste(getwd(), "/data/network/", yearID, ".mvdata.csv",sep = ""))
  writeLines(paste("Reading data from",filename))
  games    <- read.csv(filename, header = T)
  writeLines(paste("  Found",nrow(games),"games."))
  return( games )
}

setMVOutcomes <- function(games) {
  return( games )
}

createMVModel <- function(mvdata) {
  rankings <- getMVRankings(mvdata)
  return( rankings )
}






##############################################################################
##
## ELO Model
##
##############################################################################
loadELOGames <- function(yearID) {
  filename <- file.path(paste(getwd(), "/data/network/", yearID, ".elodata.csv",sep = ""))
  writeLines(paste("Reading data from",filename))
  games    <- read.csv(filename, header = T)
  games[,"HomeTeam"] <- as.character(games[,"HomeTeam"])
  games[,"AwayTeam"] <- as.character(games[,"AwayTeam"])
  writeLines(paste("  Found",nrow(games),"games."))
  return( games )
}

createELOModel <- function(elodata) {
  rankings <- getELORankings(elodata)
}

createFideModel <- function(fidedata) {
  rankings <- getFideRankings(fidedata)
}


##############################################################################
##
## Graph Model
##
##############################################################################
loadGrGames <- function(yearID) {
  filename <- file.path(paste(getwd(), "/data/network/", yearID, ".grdata.csv",sep = ""))
  writeLines(paste("Reading data from",filename))
  games    <- read.csv(filename, header = T)
  games[,"WinTeam"] <- as.character(games[,"WinTeam"])
  games[,"LossTeam"] <- as.character(games[,"LossTeam"])
  writeLines(paste("  Found",nrow(games),"games."))
  return( games )
}

createGrModel <- function(grdata) {
  writeLines(paste("Running graph with",nrow(grdata),"games."))
  grModel <- graph_from_edgelist(cbind(grdata[,"LossTeam"], grdata[,"WinTeam"]))
  E(grModel)$weights <- grdata[,"Weight"]
  return( grModel )
}





##############################################################################
##
## Massey Model
##
##############################################################################
loadMsyGames <- function(yearID) {
  msydata <- loadBTGames(yearID)
  colnames(msydata) <- c("team1", "team2", "team1_goals", "team2_goals")
  ## Correct team names to ensure character
  msydata$team1 <- as.character(msydata$team1)
  msydata$team2 <- as.character(msydata$team2)
  return( msydata )
}

createMsyModel <- function(msygames) {
  rankings <- getMasseyRankings(msygames)
  return( rankings )
}


##############################################################################
##
## Colley Matrix Model
##
##############################################################################
loadClyGames <- function(yearID) {
  clygames <- loadGrGames(yearID)
  return( clygames )
}

createClyModel <- function(clygames) {
  rankings <- getColleyRankings(clygames)
  return( rankings )
}


##############################################################################
##
## Offense/Defence Model
##
##############################################################################
loadODGames <- function(yearID) {
  odgames <- loadBTGames(yearID)
  return( odgames )
}

createODModel <- function(clygames) {
  writeLines(paste("Running Colley with",nrow(odgames),"games."))
  rankings <- getOffDefRankings(odgames)
}


##############################################################################
##
## Merge All Rankings
##
##############################################################################
mergeRankings <- function(rankings, name) {
  writeLines(paste("Merging rankings (",name,") with",length(rankings),"models."))
  
  modelnames <- names(rankings)
  mRankings  <- rankings[[1]][name]
  mRankings[,"TeamName"] <- rownames(mRankings)
  print(mRankings)
  print(paste(modelnames[1],paste(dim(mRankings), collapse = "x")))
  for ( mNum in seq(2,length(rankings)) ) {
    modelDF <- rankings[[mNum]][name]
    modelDF[,"TeamName"] <- rownames(modelDF)
    mRankings <- merge(mRankings,modelDF,by="TeamName")
    print(paste(modelnames[mNum],paste(dim(mRankings), collapse = "x")))
  }
  colnames(mRankings) <- c("TeamName", modelnames)
  return(mRankings)  
}

yearID  <- '2016'
btgames <- loadBTGames(yearID)
btdata  <- setBTOutcomes(btgames)
btModel <- createBTModel(btdata)
btRank  <- btModel[["rank"]]


mvgames    <- loadMVGames(yearID)
mvdata     <- setMVOutcomes(mvgames)
mvModel    <- createMVModel(mvdata)
mvRank     <- mvModel[["rank"]]
mvOffRank  <- mvModel[["offrank"]]
mvDefRank  <- mvModel[["defrank"]]


elogames  <- loadELOGames(yearID)
eloModel  <- createELOModel(elogames)
eloRank   <- eloModel[["rank"]]


fideModel   <- createFideModel(elogames)
fideRank    <- fideModel[["rank"]]
fideOppRank <- fideModel[["opprank"]]


msygames   <- loadMsyGames(yearID)
msyModel   <- createMsyModel(msygames)
msyRank    <- msyModel[["rank"]]
msyOffRank <- msyModel[["offrank"]]
msyDefRank <- msyModel[["defrank"]]


clygames <- loadClyGames(yearID)
clyModel <- createClyModel(clygames)
clyRank  <- clyModel[["rank"]]

#odgames  <- loadODGames(yearID)
#odModel  <- createODModel(odgames)
#odRank   <- odModel[["rank"]]


grgames  <- loadGrGames(yearID)
weights  <- grgames[,"Weight"]
grModel  <- createGrModel(grgames)
prModel  <- getTeamPageRank(grModel, weights/mean(weights))
prRank   <- prModel[["rank"]]
srModel  <- getTeamSimRank(grModel)
srRank   <- srModel[["rank"]]


models <- list("BradleyTerry"=btRank,
               "MVglm"=mvRank,"MVglmOff"=mvOffRank,"MVglmDef"=mvDefRank,
               "ELO"=eloRank,"Fide"=fideRank,"FideOpp"=fideOppRank,
               "Massey"=msyRank,"MasseyOff"=msyOffRank,"MasseyDef"=msyDefRank,
               "Colley"=clyRank,
               "PageRank"=prRank,
               "SimRank"=srRank)

mRankings <- mergeRankings(models, "score")
oRankings <- mergeRankings(models, "rank")
filename <- file.path(paste(getwd(), "/data/rankings/", yearID, ".rData",sep = ""))
save(mRankings, oRankings, file = filename, compress = T)