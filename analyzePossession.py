#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:50:14 2019

@author: tgadfort
"""

from debug import debugclass

from playTypes import returnplay, patplay
#from copy import deepcopy, copy

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
## Drive Class
############################################################################################################
class analyzepossession:
    def __init__(self, copMap, players):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        self.sep    = "======================================================"
        
        self.copMap  = copMap
        self.players = players
        
        self.dc = debugclass()
        
        
    ########################################################################################################
    ## Check Continuity
    ########################################################################################################
    def continuity(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Continuity".format(self.ind))
        changes = []
        #saved   = copy(gameData)
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            self.logger.debug("{0}  Checking Drive {1}".format(self.ind, idr))
            for ipl,drivePlay in enumerate(drivePlays):
                possession = drivePlay.possession
                if not possession.isKnownStart():
                    try:
                        prevStart = drivePlays[ipl-1].possession
                        nextStart = drivePlays[ipl+1].possession
                        if prevStart.start == nextStart.start and prevStart.isKnownStart():
                            text = drivePlay.play.text
                            self.logger.debug("{0}    Setting Play {1} from {2} to {3}: {4}".format(self.ind, ipl, possession.start, prevStart.start, text))
                            possession.start = prevStart.start
                            changes.append(idr)
                            continue
                    except:
                        pass
                    
                if not possession.isKnownStart():
                    try:
                        prevStart     = drivePlays[ipl-1].possession
                        nextStart     = drivePlays[ipl+1].possession
                        nextnextStart = drivePlays[ipl+2].possession
                        if not nextStart.isKnownStart():
                            if prevStart.start == nextnextStart.start and prevStart.isKnownStart():
                                text = drivePlay.play.text
                                self.logger.debug("{0}    Setting Play {1} from {2} to {3}: {4}".format(self.ind, ipl, possession.start, prevStart.start, text))
                                possession.start = prevStart.start
                                self.logger.debug("{0}    Setting Play {1} from {2} to {3}: {4}".format(self.ind, ipl+1, possession.start, prevStart.start, text))
                                nextStart.start  = prevStart.start
                                changes.append(idr)
                                continue
                    except:
                        pass
            
        self.logger.debug("{0}Analyzing Continuity -> {1} Changes".format(self.ind, len(changes)))

        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
        
        
        return gameData
        
    
    ########################################################################################################
    ## Check Returns Structure
    ########################################################################################################
    def returns(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Returns".format(self.ind))
        
        changes = []
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,playData in enumerate(drivePlays):
                valid      = playData.valid
                if valid is False:
                    continue
                if isinstance(playData.play, returnplay):
                    self.logger.debug("{0}  Drive {1}, Play {2}\tReturn Play  --> {3}: {4}".format(self.ind,idr,ipl,playData.possession.start,playData.play.text))
                    if not playData.possession.isKnownStart():
                        try:
                            prevPlay = drivePlays[ipl-1]
                        except:
                            continue
                        if prevPlay.possession.isKnownStart():
                            playData.possession.start = self.copMap[prevPlay.possession.start]
                            self.logger.debug("{0}    Drive {1}, Play {2}\tNew Return Play  --> {3}: {4}".format(self.ind,idr,ipl,playData.possession.start,playData.play.text))
                    
                            for ipl2 in range(ipl+1, len(drivePlays)):
                                if not drivePlays[ipl2].possession.isKnownStart():
                                    drivePlays[ipl2].possession.start = drivePlays[ipl2-1].possession.start
                                    self.logger.debug("{0}    Drive {1}, Play {2}\tAfter Return Play  --> {3}: {4}".format(self.ind,idr,ipl,drivePlays[ipl2].possession.start,drivePlays[ipl2].play.text))                                        
            
        self.logger.debug("{0}Analyzing Returns -> {1} Changes".format(self.ind, len(changes)))

        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))

                    
        return gameData
        
    
    ########################################################################################################
    ## Analyze PAT Structure
    ########################################################################################################
    def pats(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing PATs".format(self.ind))
        
        changes = []
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,playData in enumerate(drivePlays):
                valid      = playData.valid
                if valid is False:
                    continue
                if isinstance(playData.play, patplay):
                    self.logger.debug("{0}  Drive {1}, Play {2}\tPAT Play  --> {3}: {4}".format(self.ind,idr,ipl,playData.possession.start,playData.play.text))
                    if not playData.possession.isKnownStart():
                        if playData.play.pa.getKey("defpat"):
                            prevPlay = drivePlays[ipl-1]
                            if prevPlay.possession.isKnownStart():
                                playData.possession.start = self.copMap[prevPlay.possession.start]
                                self.logger.debug("{0}    Drive {1}, Play {2}\tNew PAT Play  --> {3}: {4}".format(self.ind,idr,ipl,playData.possession.start,playData.play.text))
                    
                                for ipl2 in range(ipl+1, len(drivePlays)):
                                    if not drivePlays[ipl2].possession.isKnownStart():
                                        drivePlays[ipl2].possession.start = drivePlays[ipl2-1].possession.start
                                        self.logger.debug("{0}    Drive {1}, Play {2}\tAfter PAT Play  --> {3}: {4}".format(self.ind,idr,ipl,drivePlays[ipl2].possession.start,drivePlays[ipl2].play.text))                                        
                                        
        self.logger.debug("{0}Analyzing PATs -> {1} Changes".format(self.ind, len(changes)))

        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData

    
    ########################################################################################################
    ## Analyze End Of Game Structure
    ########################################################################################################
    def endofgame(self, gameData, postDriveScores):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing End Of Game".format(self.ind))
        
        homeTeam = self.players.homeTeamName
        awayTeam = self.players.awayTeamName

        runningHomeScore = 0
        runningAwayScore = 0
        
        postDriveScores["Analysis"] = []
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for drivePlay in drivePlays:
                if drivePlay.valid is False:
                    continue
                play       = drivePlay.play
                possession = drivePlay.possession
                score      = play.pa.isScore()
                if score > 0:
                    if possession.start == homeTeam:
                        runningHomeScore += score
                    elif possession.start == awayTeam:
                        runningAwayScore += score
                    else:
                        self.logger.debug("{0}Possession {1} is neither home {2} or away {3}".format(self.ind, possession.start, homeTeam, awayTeam))
                                    
            postDriveScores["Analysis"].append([runningAwayScore, runningHomeScore])
    
    
        ## Get penultimate drive
        penultKnownDrive = postDriveScores["Drives"][-2]
        penultAnalyDrive = postDriveScores["Analysis"][-2]
        if penultKnownDrive == penultAnalyDrive:
            lastKnownDrive = postDriveScores["Drives"][-1]
            lastAnalyDrive = postDriveScores["Analysis"][-1]
            finalScore = postDriveScores["Final"]
            if lastKnownDrive == lastAnalyDrive and lastKnownDrive == finalScore:
                self.logger.debug("{0}Score is correct for this game".format(self.ind))
            else:
                if finalScore[0] - lastAnalyDrive[0] == 6:
                    ## Away Team
                    self.logger.debug("{0}  Away team ({1}) needs a TD".format(self.ind, awayTeam))
                    self.dc.showDrive(gameData[-1], len(gameData))
                    for i in range(1,len(gameData[-1].plays)+1):
                        if gameData[-1].plays[-1*i].valid is False:
                            continue
                        lastPoss = gameData[-1].plays[-1*i].possession.start
                        self.logger.debug("{0}  Last Possession goes to {1}".format(self.ind, lastPoss))

                        if lastPoss == awayTeam:
                            gameData[-1].plays[-1*i].play.pa.touchdown = True
                        else:
                            self.logger.debug("{0}    Problem with possession. Not sure....".format(self.ind))
                        break
                elif finalScore[1] - lastAnalyDrive[1] == 6:
                    ## Home Team
                    self.logger.debug("{0}  Home team ({1}) needs a TD".format(self.ind, homeTeam))
                    self.dc.showDrive(gameData[-1], len(gameData))
                    for i in range(1,len(gameData[-1].plays)+1):
                        if gameData[-1].plays[-1*i].valid is False:
                            continue
                        lastPoss = gameData[-1].plays[-1*i].possession.start
                        self.logger.debug("{0}  Last Possession goes to {1}".format(self.ind, lastPoss))

                        if lastPoss == homeTeam:
                            gameData[-1].plays[-1*i].play.pa.touchdown = True
                        else:
                            self.logger.debug("{0}    Problem with possession. Not sure....".format(self.ind))
                        break                        
                else:
                    self.logger.debug("{0}Problems with the scores...".foramt(self.ind))
                    self.logger.debug("{0}  KNOWN: {0}".format(self.ind, lastKnownDrive))
                    self.logger.debug("{0}  ANALY: {0}".format(self.ind, lastAnalyDrive))
                    self.logger.debug("{0}  FINAL: {0}".format(self.ind, finalScore))
        else:
            scores = zip(postDriveScores["Drives"], postDriveScores["Analysis"])
            self.logger.warn("Not sure what is going on with scores....")
            for i,score in enumerate(scores):
                self.logger.warn("{0}\t{1}".format(i,score))
            
        return gameData
    
    
    
    ########################################################################################################
    ##
    ## Analyze Game Score After Each Drive
    ##
    ########################################################################################################
    def gamescore(self, gameData, postDriveScores):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Game Score".format(self.ind))
        
        homeTeam = self.players.homeTeamName
        awayTeam = self.players.awayTeamName
        
        
        finalScore = postDriveScores["Final"]
        awayTeamFinalScore = finalScore[0]
        homeTeamFinalScore = finalScore[1]

        driveScore = postDriveScores["Drives"]
        
        runningHomeScore = 0
        runningAwayScore = 0
        finalHomeScore   = None
        finalAwayScore   = None
        
        postDriveScores["Analysis"] = []
        
        for idr,driveData in enumerate(gameData):
            scoringplays = []
            drivePlays = driveData.plays
            awayscore,homescore = driveScore[idr]
            #homescore  = driveData.postdrivehomescore
            #awayscore  = driveData.postdriveawayscore
            finalAwayScore = awayscore
            finalHomeScore = homescore
            for drivePlay in drivePlays:
                if drivePlay.valid is False:
                    continue
                play       = drivePlay.play
                possession = drivePlay.possession
                score      = play.pa.isScore()
                if score > 0:
                    scoringplays.append(play.text)
                    if possession.start == homeTeam:
                        runningHomeScore += score
                    elif possession.start == awayTeam:
                        runningAwayScore += score
                    else:
                        self.logger.warn("{0}Possession {1} is neither home {2} or away {3}".format(self.ind, possession.start, homeTeam, awayTeam))
                    
            
            postDriveScores["Analysis"].append([runningAwayScore, runningHomeScore])
        
            self.logger.debug("{0}{1: <7}{2: <4}{3: <4}{4: <4}{5: <4}{6}".format(self.ind, idr, runningHomeScore, homescore, runningAwayScore, awayscore, " ; ".join(scoringplays)))
    
        self.logger.debug("{0}{1: <7}{2: <4}{3: <4}{4: <4}{5: <4}{6}".format(self.ind, "----", "---", "---", "---", "---", ""))
        self.logger.debug("{0}{1: <7}{2: <4}{3: <4}{4: <4}{5: <4}{6}".format(self.ind, "END", runningHomeScore, finalHomeScore, runningAwayScore, finalAwayScore, ""))
        self.logger.debug("{0}{1: <7}{2: <4}{3: <4}{4: <4}{5: <4}{6}".format(self.ind, "TRUE", homeTeamFinalScore, "", awayTeamFinalScore, "", ""))
        
        diffHomeScore = homeTeamFinalScore - runningHomeScore
        diffAwayScore = awayTeamFinalScore - runningAwayScore

        self.logger.debug("{0}{1: <7}{2: <4}{3: <4}{4: <4}{5: <4}{6}".format(self.ind, "DIFF", diffHomeScore, "", diffAwayScore, "", ""))
            
        if diffHomeScore != 0 or diffAwayScore != 0:
            return False
        return True
    
    
    
    