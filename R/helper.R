sortRankings <- function(score, rev=F) {
  scoreOrder <- !rev
  tmp   <- names(score)[order(score, decreasing = scoreOrder)]
  rank <- seq(length(tmp))
  names(rank) <- tmp
  rank <- rank[sort(names(rank))]
  score <- score[sort(names(score))]
  rdf <- data.frame(score, rank)
  return( rdf )
}

makeShortNames <- function(fullNames) {
  shortNames <- fullNames
  shortNames <- gsub(replacement = "NC State", pattern = "North Carolina State", shortNames)
  shortNames <- gsub(replacement = "Ole Miss University", pattern = "University of Mississippi", shortNames)
  shortNames <- gsub(replacement = "UNLV University", pattern = "Nevada-Las Vegas University", shortNames)
  shortNames <- gsub(replacement = "TCU University", pattern = "Texas Christian University", shortNames)
  shortNames <- gsub(replacement = "Bowling Green University", pattern = "Bowling Green State University", shortNames)
  shortNames <- gsub(replacement = "BYU University", pattern = "Brigham Young University", shortNames)
  shortNames <- gsub(replacement = "Middle Tennessee University", pattern = "Middle Tennessee State University", shortNames)
  shortNames <- gsub(replacement = "Hawai\\\\'i University", pattern = "University of Hawaii", shortNames)
  shortNames <- gsub(replacement = "Kent State University", pattern = "Kent University", shortNames)
  shortNames <- gsub(replacement = "LSU University", pattern = "Louisiana State University", shortNames)
  shortNames <- gsub(replacement = "SMU University", pattern = "Southern Methodist University", shortNames)
  shortNames <- gsub(replacement = "UCF University", pattern = "Central Florida University", shortNames)
  shortNames <- gsub(replacement = "Miami University", pattern = "Miami (Florida) University", shortNames)
  shortNames <- gsub(replacement = "Miami \\(OH\\) University", pattern = "Miami (Ohio) University", shortNames)
  shortNames <- gsub(replacement = "Florida Intl University", pattern = "Florida International University", shortNames)
  shortNames <- gsub(replacement = "UT San Antonio University", pattern = "Texas-San Antonio University", shortNames)
  shortNames <- gsub(replacement = "UTEP University", pattern = "Texas-El Paso University", shortNames)
  shortNames <- gsub(replacement = "UCLA University", pattern = "UCLA", shortNames)
  shortNames <- gsub(replacement = "USC", pattern = "University of Southern California", shortNames)
  shortNames <- gsub(replacement = "Louisiana Monroe University", pattern = "Louisiana-Monroe University", shortNames)
  shortNames <- gsub(replacement = "University of Louisiana", pattern = "Louisiana-Lafayette University", shortNames)
  shortNames <- gsub(replacement = "LSU", pattern = "Louisiana State University", shortNames)
  shortNames <- gsub(replacement = "UMass University", pattern = "University of Massachusetts", shortNames)
  shortNames <- gsub("University of ", "", shortNames)
  shortNames <- gsub(" University", "", shortNames)
  return( shortNames )
}

makeFullNames <- function(shortNames) {
  fullNames <- ifelse(shortnames %in% state.name, 
                      paste("University of",shortnames),
                      paste(shortnames,"University"))
  fullNames <- gsub("NC State", "North Carolina State", fullNames)
  fullNames <- gsub("Ole Miss University", "University of Mississippi", fullNames)
  fullNames <- gsub("UNLV University", "Nevada-Las Vegas University", fullNames)
  fullNames <- gsub("TCU University", "Texas Christian University", fullNames)
  fullNames <- gsub("Bowling Green University", "Bowling Green State University", fullNames)
  fullNames <- gsub("BYU University", "Brigham Young University", fullNames)
  fullNames <- gsub("Middle Tennessee University", "Middle Tennessee State University", fullNames)
  fullNames <- gsub("Hawai\\\\'i University", "University of Hawaii", fullNames)
  fullNames <- gsub("Kent State University", "Kent University", fullNames)
  fullNames <- gsub("LSU University", "Louisiana State University", fullNames)
  fullNames <- gsub("SMU University", "Southern Methodist University", fullNames)
  fullNames <- gsub("UCF University", "Central Florida University", fullNames)
  fullNames <- gsub("Miami University", "Miami (Florida) University", fullNames)
  fullNames <- gsub("Miami \\(OH\\) University", "Miami (Ohio) University", fullNames)
  fullNames <- gsub("Florida Intl University", "Florida International University", fullNames)
  fullNames <- gsub("UT San Antonio University", "Texas-San Antonio University", fullNames)
  fullNames <- gsub("UTEP University", "Texas-El Paso University", fullNames)
  fullNames <- gsub("UCLA University", "UCLA", fullNames)
  fullNames <- gsub("USC University", "University of Southern California", fullNames)
  fullNames <- gsub("Louisiana Monroe University", "Louisiana-Monroe University", fullNames)
  fullNames <- gsub("University of Louisiana", "Louisiana-Lafayette University", fullNames)
  fullNames <- gsub("LSU", "Louisiana State University", fullNames)
  fullNames <- gsub("UMass University", "University of Massachusetts", fullNames)
  return( fullNames )
}