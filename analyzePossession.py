#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:50:14 2019

@author: tgadfort
"""

from debug import debugclass
#from copy import deepcopy, copy

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
## Drive Class
############################################################################################################
class analyzepossession:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        
        self.dc = debugclass()
        
        
    ########################################################################################################
    ## Check Continuity
    ########################################################################################################
    def continuity(self, gameData):
        self.logger.debug("{0}Analyzing Continuity".format(self.ind))
        changes = []
        #saved   = copy(gameData)
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            self.logger.debug("{0}  Checking Drive {1}".format(self.ind, idr))
            for ipl,drivePlay in enumerate(drivePlays):
                self.logger.debug("{0}{1},{2}".format(self.ind, idr, ipl))
                possession = drivePlay.possession
                if not possession.isKnownStart():
                    self.logger.debug("{0}    Not known play ({1}): {2}".format(self.ind, ipl, drivePlay.play.text))
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
                    self.logger.debug("{0}    Still not known play ({1}): {2}".format(self.ind, ipl, drivePlay.play.text))
                    try:
                        prevStart     = drivePlays[ipl-1].possession
                        nextStart     = drivePlays[ipl+1].possession
                        nextnextStart = drivePlays[ipl+2].possession
                        if not nextStart.isKnownStart():
                            self.logger.debug("{0}    Double not knowns".format(self.ind))
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
    ##
    ## Analyze Kickoff Structure
    ##
    ########################################################################################################
    def analyzeKickoffs(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
                        
        unknown = False
        
        kickers = {}
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            prevStart  = None
            if sum([isinstance(x.play, kickoffplay) for x in drivePlays]) > 0:
                posCntr = Counter()
                for playData in drivePlays:
                    if isinstance(playData.play, (rushingplay, passingplay, sackplay, fieldgoalplay)):
                        posCntr[playData.possession.start] += 1
                        
                if len(posCntr) == 0:
                    continue
                
                for ipl,playData in enumerate(drivePlays):
                    if isinstance(playData.play, (kickoffplay)):
                        playText = playData.play.text
                        keys = [" kickoff ", " Kickoff", " KICKOFF "]
                        pos = max([playText.find(x) for x in keys])
                        if pos > 0:
                            text = playText[:pos].strip()
                            if kickers.get(text) is None:
                                kickers[text] = Counter()
                            try:
                                team = copMap[posCntr.most_common(1)[0][0]]
                            except:
                                if debug:
                                    print("Unknown team: {0} in {1}".format(team, fname))
                                continue
                                
                            try:
                                kickers[text][team] += 1
                            except:
                                pass
                            
                        
        for kicker in kickers.keys():
            kickers[kicker] = kickers[kicker].most_common(1)[0][0]
            if debug:
                print("Kicker: {0} ---> {1}".format(kicker,kickers[kicker]))
        players.addKickers(kickers, debug)
        
        
        for idr,driveData in enumerate(gameData):
            for ipl,playData in enumerate(driveData.plays):
                if isinstance(playData.play, (kickoffplay)):
                    poss, self.determinePossession(playData.play, players)
                    gameData[idr].plays[ipl].possession = poss

        gameData = self.analyzePossession(gameData, players, debug)
            
        return gameData
        
    
    ########################################################################################################
    ##
    ## Analyze Returns Structure
    ##
    ########################################################################################################
    def analyzeReturns(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,playData in enumerate(drivePlays):
                valid      = playData.valid
                if valid is False:
                    continue
                if isinstance(playData.play, returnplay):
                    if debug:
                        print("Return play {0},{1} --> {2}: {3}".format(idr,ipl,playData.possession.start,playData.play.text))
                    if not playData.possession.isKnownStart():
                        prevPlay = drivePlays[ipl-1]
                        if prevPlay.possession.isKnownStart():
                            playData.possession.start = copMap[prevPlay.possession.start]
                            if debug:
                                print("\tReturn play {0},{1} --> {2}: {3}".format(idr,ipl,playData.possession.start,playData.play.text))
                    
                            for ipl2 in range(ipl+1, len(drivePlays)):
                                if not drivePlays[ipl2].possession.isKnownStart():
                                    drivePlays[ipl2].possession.start = drivePlays[ipl2-1].possession.start
                                    if debug:
                                        print("\tSetting {0},{1} start to {2}".format(idr, ipl2, playData.possession.start))

                    
        return gameData
        
    
    ########################################################################################################
    ##
    ## Analyze PAT Structure
    ##
    ########################################################################################################
    def analyzePATs(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,playData in enumerate(drivePlays):
                valid      = playData.valid
                if valid is False:
                    continue
                if isinstance(playData.play, patplay):
                    if debug:
                        print("PAT play {0},{1} --> {2}: {3}".format(idr,ipl,playData.possession.start,playData.play.text))
                    if not playData.possession.isKnownStart():
                        if playData.play.pa.getKey("defpat"):
                            prevPlay = drivePlays[ipl-1]
                            if prevPlay.possession.isKnownStart():
                                playData.possession.start = copMap[prevPlay.possession.start]
                                if debug:
                                    print("\tPAT play {0},{1} --> {2}: {3}".format(idr,ipl,playData.possession.start,playData.play.text))
                    
                                for ipl2 in range(ipl+1, len(drivePlays)):
                                    if not drivePlays[ipl2].possession.isKnownStart():
                                        drivePlays[ipl2].possession.start = drivePlays[ipl2-1].possession.start
                                        if debug:
                                            print("\tSetting {0},{1} start to {2}".format(idr, ipl2, playData.possession.start))

                    
        return gameData
        
    
    ########################################################################################################
    ##
    ## Analyze Interception Structure
    ##
    ########################################################################################################
    def analyzeInterceptions(self, gameData, players, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,playData in enumerate(drivePlays):
                valid      = playData.valid
                if valid is False:
                    continue
                if playData.play.pa.getKey("interception") is True:                    
                    if playData.possession.isPreviousStart() is True or playData.possession.isUnknownStart() is True:
                        try:
                            if gameData[idr].plays[ipl-1].valid is True:
                                gameData[idr].plays[ipl].possession.start = gameData[idr].plays[ipl-1].possession.start
                        except:
                            pass
                        
        return gameData
        
    
    ########################################################################################################
    ##
    ## Analyze Penalties and Timeouts
    ##
    ########################################################################################################
    def analyzePenaltiesAndTOs(self, gameData, players, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
        
        lastPlayPoss = None
        
        for idr,driveData in enumerate(gameData):
            if lastPlayPoss is not None:
                if len(driveData.plays) == 0:
                    if debug:
                        print("There are no plays in drive number {0}".format(idr))
                    continue
                firstPlayPoss = driveData.plays[0]
                if not firstPlayPoss.possession.isKnownStart():
                    if debug:
                        print("Setting possession for first play to {0}".format(lastPlayPoss.start))
                    driveData.plays[0].possession.start = lastPlayPoss.start
                
            for ipl,playData in enumerate(driveData.plays):
                if isinstance(playData.play, (penaltyplay,timeoutplay)):
                    if playData.possession.isPreviousStart() is True or playData.possession.isUnknownStart() is True:
                        try:
                            if gameData[idr].plays[ipl-1].possession.start == gameData[idr].plays[ipl+1].possession.start:
                                gameData[idr].plays[ipl].possession.start = gameData[idr].plays[ipl-1].possession.start
                        except:
                            pass
                    
                    if playData.possession.isPreviousStart() is True or playData.possession.isUnknownStart() is True:

                        try:
                            if gameData[idr].plays[ipl+1].possession.isPreviousStart() is False and gameData[idr].plays[ipl+1].valid is True:
                                gameData[idr].plays[ipl].possession.start = gameData[idr].plays[ipl+1].possession.start
                        except:
                            pass
                    
                    if playData.possession.isPreviousStart() is True or playData.possession.isUnknownStart() is True:
                        try:
                            if gameData[idr].plays[ipl-1].valid is True:
                                gameData[idr].plays[ipl].possession.start = gameData[idr].plays[ipl-1].possession.start
                        except:
                            pass

            lastPlayPoss = driveData.plays[-1].possession



        gameData = self.analyzePossession(gameData, players, debug)
                        
        return gameData
        
    
    ########################################################################################################
    ##
    ## Analyze Interception Structure
    ##
    ########################################################################################################
    def analyzeEndOfGame(self, gameData, players, postDriveScores, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
             
        homeTeam = players.homeTeamName
        awayTeam = players.awayTeamName

        runningHomeScore = 0
        runningAwayScore = 0
        
        dc  = debugclass()

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
                        print("Possession {0} is neither home {1} or away {2}".format(possession.start, homeTeam, awayTeam))
                                    
            postDriveScores["Analysis"].append([runningAwayScore, runningHomeScore])
    
        ## Get penultimate drive
        penultKnownDrive = postDriveScores["Drives"][-2]
        penultAnalyDrive = postDriveScores["Analysis"][-2]
        if penultKnownDrive == penultAnalyDrive:
            lastKnownDrive = postDriveScores["Drives"][-1]
            lastAnalyDrive = postDriveScores["Analysis"][-1]
            finalScore = postDriveScores["Final"]
            if lastKnownDrive == lastAnalyDrive and lastKnownDrive == finalScore:
                if debug:
                    print("SCORE is CORRECT")
            else:
                if finalScore[0] - lastAnalyDrive[0] == 6:
                    ## Away Team                    
                    if debug:
                        print("  Away team ({0}) needs a TD".format(awayTeam))
                        dc.showDrive(gameData[-1], len(gameData), debug=debug)
                    for i in range(1,len(gameData[-1].plays)+1):
                        if gameData[-1].plays[-1*i].valid is False:
                            continue
                        lastPoss = gameData[-1].plays[-1*i].possession.start
                        print("  Last Possession goes to {0}".format(lastPoss))

                        if lastPoss == awayTeam:
                            gameData[-1].plays[-1*i].play.pa.touchdown = True
                        else:
                            print("    Problem with possession. Not sure....")
                        break
                elif finalScore[1] - lastAnalyDrive[1] == 6:
                    ## Home Team                
                    if debug:
                        print("  Home team ({0}) needs a TD".format(homeTeam))
                        dc.showDrive(gameData[-1], len(gameData), debug=debug)
                    for i in range(1,len(gameData[-1].plays)+1):
                        if gameData[-1].plays[-1*i].valid is False:
                            continue
                        lastPoss = gameData[-1].plays[-1*i].possession.start
                        print("  Last Possession goes to {0}".format(lastPoss))

                        if lastPoss == homeTeam:
                            gameData[-1].plays[-1*i].play.pa.touchdown = True
                        else:
                            print("    Problem with possession. Not sure....")
                        break                        
                else:
                    if debug:
                        print("Problems with the scores...")
                        print("KNOWN: {0}".format(lastKnownDrive))
                        print("ANALY: {0}".format(lastAnalyDrive))
                        print("FINAL: {0}".format(finalScore))
        else:
            if debug:
                scores = zip(postDriveScores["Drives"], postDriveScores["Analysis"])
                for i,score in enumerate(scores):
                    print(i,'\t',score)
            
        return gameData
    
    
    
    ########################################################################################################
    ##
    ## Analyze Game Score After Each Drive
    ##
    ########################################################################################################
    def analyzeGameScore(self, gameData, players, homeTeamGameData, awayTeamGameData, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is {0}".format(type(gameData)))

        homeTeam = players.homeTeamName
        awayTeam = players.awayTeamName

        finalHomeScore = None
        runningHomeScore = 0
        finalAwayScore = None
        runningAwayScore = 0
        if debug:
            print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}\t(Post Drive Score)".format("Drive", "H", "(H)", "A", "(A)"))
            
        for idr in range(len(gameData)):
            driveData  = gameData[idr]
            homescore  = driveData.postdrivehomescore
            awayscore  = driveData.postdriveawayscore
            finalAwayScore = awayscore
            finalHomeScore = homescore

            drivePlays = driveData.plays
            if isinstance(drivePlays, list) is False:
                raise ValueError("Drive Plays is not a list object!")

            scoringplays = []
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
                        print("Possession {0} is neither home {1} or away {2}".format(possession.start, homeTeam, awayTeam))
                        
            if debug:
                print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}{5}".format(idr, runningHomeScore, homescore, runningAwayScore, awayscore, scoringplays))
                
                
        if debug:
            print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}{5}".format("----", "---", "---", "---", "---", ""))
            print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}{5}".format("END", runningHomeScore, finalHomeScore, runningAwayScore, finalAwayScore, ""))
            print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}{5}".format("TRUE", homeTeamGameData.teamAScore, "", awayTeamGameData.teamAScore, "", ""))
        
        diffHomeScore = homeTeamGameData.teamAScore - runningHomeScore
        diffAwayScore = awayTeamGameData.teamAScore - runningAwayScore

        if debug:
            print("{0: <7}{1: <4}{2: <4}{3: <4}{4: <4}{5}".format("DIFF", diffHomeScore, "", diffAwayScore, "", ""))
            
        if diffHomeScore != 0 or diffAwayScore != 0:
            return False
        return True
    
    

    ########################################################################################################
    ##
    ## Combine all play data data together
    ##
    ########################################################################################################
    def parsePlayData(self, playStart, playData, fieldMap, possData, gameID, driveNo, playNo, debug=False, verydebug=False):
        if verydebug:
            fname = sys._getframe().f_code.co_name
            print("\n  FUNC {0}({1},{2}: {3})".format(fname, driveNo, playNo, playData))
        
        
        ##########################
        ## Find clock and quarter
        ##########################
        gameclock, quarter, playText = self.parseClockAndQuarter(playData, debug=verydebug)

        
        ### Must fix corrupt text from time to time...
        playText,keep = self.editText(playText, gameID, driveNo, playNo)
        if keep is False:
            return None
        
        
        ##########################
        ## Determine play type
        ##########################
        ptype = playtype(playText)
        play  = ptype.getPlay()
        if ptype.valid is True:
            if play is None:
                raise ValueError("Could not determine play type from {0}".format(playText))
            play.analyze(debug=debug)
        if debug:
            if play is not None:
                print("\tPlay: {0} \t{1}".format(play.name, play.text))

        
        ##########################
        ## Check for valid play
        ##########################
        if ptype.valid is True and play is not None:
            validPlay = play.pa.getKey("noplay") != True
            if isinstance(play, (beginplay, endplay, timeoutplay)):
                validPlay = False
        else:
            validPlay = False
        
        
        
        ##########################
        ## Determine possession
        ##########################        
        if ptype.valid is True and play is not None and validPlay is True:
            playPossession = possData.determinePossession(play, debug=debug, verydebug=verydebug)
            if playPossession.start is None:
                raise ValueError("Possession for play of type [{0}] with text [{1}] was set to NONE!".format(play.name,playText))
        else:
            playPossession = playpossessionclass(start=None, end=None)
            playPossession.valid = False
        
        if playPossession.isForced() is not None:
            play.pa.forced = playPossession.isForced()            
        
        if playPossession.valid is False:
            validPlay = False
        
        if playPossession.valid is True:
            if playPossession.start is None:
                raise ValueError("Possession for play of type [{0}] with text [{1}] was set to NONE!".format(play.name,playText))
            
        
        ##########################
        ## Insert Clock/Quarter
        ##########################
        if playStart is None:
            playStart = playstartclass()
            
        if isinstance(playStart, playstartclass):
            playStart.setQuarter(quarter)
            playStart.setGameClock(gameclock)

            
        ### Result of play
        playResult = playclass(possession=playPossession, start=playStart, play=play, valid=validPlay)
        return playResult
    