library(PlayerRatings)


pause <- function(){
  stopifnot(FALSE)
}


## Define CSV files
basedir <- "C:/Users/tgadfort/Dropbox/Football"
if ( file.access(basedir) == -1 ) {
  basedir <- "~/Dropbox/Football"
  if ( file.access(basedir) == -1 ) {
    writeLines(paste("Can not find files in",basedir))
    pause()
  }
}
gamecsv <- file.path(basedir, "2015.csv")
confcsv <- file.path(basedir, "2015.conf")
teamcsv <- file.path(basedir, "Teams.csv")
resultscsv <- file.path(basedir, "Results.csv")


##
## Read data
##
gamedata <- read.csv(gamecsv)
confdata <- read.csv(confcsv, sep = "\t", header = FALSE)
teamnames <- read.csv(abrvcsv, sep = "\t", header = FALSE)

## Fix data
gamedata$Date <- as.Date(paste("2015", gamedata$Date, sep="/"))
gamedata$Team1 <- as.character(gamedata$Team1)
gamedata$Team2 <- as.character(gamedata$Team2)
teams <- unique(gamedata$Team1)
nteams <- length(teams)
rownames(confdata) <- as.character(confdata$V1)
teamconfs <- as.character(confdata$V2)
names(teamconfs) <- as.character(confdata$V1)
confnames <- unique(confdata$V2)
confnames <- c(as.character(confnames), "FCS")
nconfs <- length(confnames)
teamcity <- as.character(teamnames$V2)
names(teamcity) <- as.character(teamnames$V1)
teamstate <- as.character(teamnames$V3)
names(teamstate) <- as.character(teamnames$V1)
teammascot <- as.character(teamnames$V4)
names(teammascot) <- as.character(teamnames$V1)
## Score must be between [0,1]
gamedata$Winner <- ifelse(gamedata$Score1 > gamedata$Score2, 1, 0)


## Create PlayerRatings data
stephdata <- data.frame()
seenteams <- c()


## Create Team data
teamcols <- c("Name", "Mascot", "Location", "City", "State", "Abrv", "Rank", "Rating", "Conference", "Games", "Wins", "Losses")
teamcols <- c(teamcols, "Best Win", "Worst Loss")
teamcols <- c(teamcols, "Avg Opp Rank", "Schedule Rank")
teamcols <- c(teamcols, "Conf Record", "Conf Opp Rank", "Conf Rank")
teamcols <- c(teamcols, paste("Vs",confnames,sep="-"))
teamdata <- as.data.frame(matrix(NA,nrow=nteams,ncol=length(teamcols)))
rownames(teamdata) <- teams
colnames(teamdata) <- teamcols
teamdata$Conference <- teamconfs[rownames(teamdata)]


for ( i in seq_along(teams) ) {
  ## Get team data
  team <- teams[[i]]
  teamgamesdata <- gamedata[gamedata$Team1 == team,]

  ## Get Standard Stuff
  teamdata[team,]$Name <- team
  teamdata[team,]$Mascot <- teammascot[team]
  teamdata[team,]$City <- teamcity[team]
  teamdata[team,]$State <- teamstate[team]
  teamdata[team,]$Location <- paste(teamcity[team], teamstate[team], sep=", ")
  

  ## Get aggregated totals
  ngames <- length(teamgamesdata$Winner)
  wins <- sum(teamgamesdata$Winner)
  loss <- ngames - wins
  teamdata[team,]$Rank <- NA
  teamdata[team,]$Rating <- NA
  teamdata[team,]$Games <- ngames
  teamdata[team,]$Wins <- wins
  teamdata[team,]$Losses <- loss

  ## Conference data
  teamgamesdata[["Team2Conf"]] <- teamconfs[teamgamesdata$Team2]
  teamgamesdata[which(is.na(teamgamesdata$Team2Conf)),"Team2Conf"] <- "FCS"
  teamconfgames <- table(teamgamesdata$Team2Conf)
  teamconfwins <- tapply(teamgamesdata$Winner, teamgamesdata$Team2Conf, sum)
  teamconfloss <- teamconfgames - teamconfwins
  for ( conf in names(teamconfgames) ) {
    confelmement <- paste(teamconfwins[conf], teamconfloss[conf], sep="-")
    confcolname <-  paste("Vs",conf,sep="-")
    teamdata[team,confcolname] <- confelmement
  }


  ## Find PlayerRatings data (no overlaps)
  res <- teamgamesdata$Team2 %in% seenteams
  newdata <- teamgamesdata[!res,]
  seenteams <- c(seenteams, team)
  stephdata <- rbind(stephdata, newdata)
}


## Run Stephenson model from PlayerRatings
sdata <- stephdata[,c("Date", "Team1", "Team2", "Winner")]
sdata$Date <- as.numeric(sdata$Date)
sresult <- steph(sdata)
stable <- sresult$ratings
stable <- stable[stable$Games > 5,c("Player", "Rating", "Games", "Win", "Loss")]

rankings <- stable[,"Rating"]
names(rankings) <- stable[,"Player"]




for ( i in 1:nrow(stable) ) {
  ## Get Team Rank/Ranking
  team <- stable[i,"Player"]
  rating <- stable[i,"Rating"]
  teamdata[team,"Rank"] <- i
  teamdata[team,"Rating"] <- rating
#  print(teamdata[team,])
#  pause()
  
  ## Get Best Win/Worst Loss
  games <- gamedata[gamedata$Team1 == team,c("Team2","Winner")]
  games$OpponnetRank <-  match(games$Team2, names(rankings))
  if ( anyNA(games) ) {
    games[is.na(games$OpponnetRank),]["OpponnetRank"] <- length(rankings)+1
  }
  
  winsdf <- games[games$Winner == 1,c("Team2", "OpponnetRank")]
  wins <- winsdf$OpponnetRank
  names(wins) <- winsdf$Team2
  lossdf <- games[games$Winner == 0,c("Team2", "OpponnetRank")]
  loss <- lossdf$OpponnetRank
  names(loss) <- lossdf$Team2

  if ( length(wins) > 0 ) {
    wrange <- wins[which(wins == min(wins))]
    wnames <- paste(names(wrange), wrange, sep=", ")
    bestwin <- wnames[[1]]
  } else {
    bestwin <- NA
  }

  if ( length(loss) > 0 ) {  
    lrange <- loss[which(loss == max(loss))]
    lnames <- paste(names(lrange), lrange, sep=", ")
    worstloss <- lnames[[1]]
  } else {
    worstloss <- NA
  }
  

  confgames <- games[which(teamconfs[games$Team2] == teamconfs[team]),]
  nconfgames <- length(confgames$Winner)
  confwins <- sum(confgames$Winner)
  confloss <- nconfgames - confwins
  confrec <- paste(confwins, confloss, sep="-")
  confopprank <- mean(confgames$OpponnetRank)
  teamdata[team,]$`Conf Record` <- confrec
  teamdata[team,]$`Conf Opp Rank` <- ifelse(nconfgames>0, confopprank, NA)

  teamdata[team,]$`Best Win` <- bestwin
  teamdata[team,]$`Worst Loss` <- worstloss
  teamdata[team,]$`Avg Opp Rank` <- mean(games$OpponnetRank)
}

print(teamdata$Rank)


## Conference info
avgconfrank <- tapply(teamdata$Rank, teamdata$Conference, mean)
teamdata$`Conf Rank` <- avgconfrank[teamdata$Conference]

opprank <- teamdata$`Avg Opp Rank`
names(opprank) <- rownames(teamdata)
opprank <- sort(opprank)
print(opprank)
for ( i in seq_along(opprank) ) {
  team <- names(opprank[i])
  print(paste(i,team))
  teamdata[team,]$`Schedule Rank` <- i
}

write.csv(teamdata, file=resultscsv)