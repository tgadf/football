getOffDefRankings <- function(odgames) {
  teams <- levels(odgames[,"home.team"])
  odgames[,"home.team"] <- as.integer(odgames[,"home.team"])
  odgames[,"away.team"] <- as.integer(odgames[,"away.team"])
  odMat <- matrix(0, nrow = length(teams), ncol = length(teams))
  for ( i in seq(nrow(odgames)) ) {
    t1 <- games[i,1]
    t2 <- games[i,2]
    s1 <- games[i,3]
    s2 <- games[i,4]
    odMat[t1,t2] <- s1
    odMat[t2,t1] <- s2
  }
  colnames(odMat) <- teams
  rownames(odMat) <- teams

  rankings <- odRank(score_mtx = odMat)
  offRank <- rankings[,"Off"]
  names(offRank) <- teams
  offRank <- sort(offRank, decreasing = F)
  
  defRank <- rankings[,"Def"]
  names(defRank) <- teams
  defRank <- sort(defRank, decreasing = T)
  
  rank <- rankings[,"Rtg"]
  names(rank) <- teams
  rank <- sort(rank, decreasing = F)
  

  return( list("rank"=rank, "offRank"=offRank, "defRank"=defRank) )
}

#' Compute the Offense-Defense ratings from a score matrix
#'
#' This function computes ratings from a score matrix.
#'
#' @param score_mtx a matrix containing score information. The matrix
#' entry \eqn{A[i,j]} encodes the score for opponent \eqn{i} against \eqn{j}.
#' @param tol the stopping parameter for convergence.  The iterative algorithm
#' stops running once the improvement in an iteration is below the threshold for
#' all ratings.
#' @return a data frame with columns \code{Off}, \code{Def}, and \{Rtg}
#' @export
odRank <- function(score_mtx, tol=1e-6) {
  off_prev <- apply(score_mtx, 1, function(x) mean(x[x>0]))
  def_prev <- apply(score_mtx, 2, function(x) mean(x[x>0]))
  repeat {
    def <- score_mtx %*% (1 / (t(score_mtx) %*% (1 / def_prev)))
    off <- t(score_mtx) %*% (1 / def)
    if (max(abs(c(off - off_prev, def - def_prev))) < tol) {
      break
    } else {
      off_prev <- off
      def_prev <- def
    }
  }
  data.frame(Off=off, Def=def, Rtg=off/def)
}