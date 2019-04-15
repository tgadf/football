#!/usr/bin/env python
# coding: utf-8

# # Football Parsing Code



## Python Version
import sys
print("Python: {0}".format(sys.version))

from os.path import join
from fsUtils import mkSubDir, setFile, isFile, removeFile, isDir
from ioUtils import getFile, saveFile
from timeUtils import clock, elapsed
from fileUtils import getBaseFilename, getBasename, getDirname
from webUtils import getWebData, getHTML
from timeUtils import printDateTime, getDateTime, addMonths
from searchUtils import findExt
from time import sleep
from random import random
import sys
import re
from datetime import timedelta
from collections import Counter

from espngames import output, espn
from espngames import game, team, season
from espngames import historical

import datetime as dt
start = dt.datetime.now()



from penalty import penalty


# # Play Start

# In[ ]:





# # Class Imports

# In[ ]:





# # Play By Play Analysis

# In[73]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '')

from summary import playclass, drivedetailclass, driveclass, playstartclass
from playYards import playyards
from playResult import playtextclass
from possession import possessionclass, mixedpossession, playpossessionclass
from footballPlays import playtype, footballplay, penaltyplay, puntplay, kickoffplay, fieldgoalplay
from footballPlays import patplay, returnplay, downsplay, tbdplay, noplay, safetyplay
from footballPlays import timeoutplay, endplay, beginplay, sackplay, rushingplay, passingplay, fumbleplay, touchdownplay

from debug import debugclass
from changePossession import possessionchangeclass
from teamStatistics import teamstatisticsclass
from gameStatistics import teamplayers, gameplayers



class playbyplay(espn, output):
    def __init__(self):
        self.name = "playbyplay"
        espn.__init__(self)
        output.__init__(self)
        
        self.hist = None
        self.ptc  = playtextclass()
        
    def setHistorical(self, hist):
        self.hist = hist
    
    
    def parsePlayStart(self, playStartText, playNo, numPlays, playData, debug=False):
        if len(playStartText) == 0:
            return None
        
        ps = None
        
        down = "(st|nd|rd|th)"
        num  = "(\d+)"
        word = "(\w+)"
        goal = "(GOAL|goal|Goal)"
        prep = "(on|at)"
        amp  = "(&|and)"
        
        ## Look for match of type [1st and 10 at CAL 19]
        m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}\s{6}".format(num, down, amp, num, prep, word, num), playStartText)
        if m is not None:
            groups = m.groups()
            down   = groups[0]
            togo   = groups[3]
            startY = groups[6]
            side   = groups[5]
            ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
            

        ## Look for match of type [1st and GOAL at CAL 1]
        m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}\s{6}".format(num, down, amp, goal, prep, word, num), playStartText)
        if m is not None:
            groups = m.groups()
            down   = groups[0]
            togo   = groups[6] ## replace goal with distance to goal
            startY = groups[6]
            side   = groups[5]
            ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
            

        ## Look for very near match without side of field [1st and 10 at 50]
        m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}".format(num, down, amp, goal, prep, num), playStartText)
        if m is not None:
            groups = m.groups()
            down   = groups[0]
            togo   = groups[3] ## replace goal with distance to goal
            startY = groups[5]
            side   = None
            ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
            

        return ps
        raise ValueError("Could not parse [{0}] and [{1}]".format(playStartText, playData))
        
        
        
    
    def parseClockAndQuarter(self, playData, debug=False):
        gameclock = None
        quarterNo = None
        
        ## Check for end of quarter/half/game
        if sum([x in playData for x in ["End of the ", "End Of The ", "end of the ", "end of ", "End of "]]) > 0:
            gameclock = timedelta(minutes=0, seconds=0) 
            if sum([x in playData for x in ["1st Quarter", "1st quarter"]]) > 0:
                quarterNo = 1
            elif sum([x in playData for x in ["2nd Quarter", "2nd quarter", "1st Half", "1st half", "half", "Half"]]) > 0:
                quarterNo = 2
            elif sum([x in playData for x in ["3rd Quarter", "3rd quarter"]]) > 0:
                quarterNo = 3
            elif sum([x in playData for x in ["4th Quarter", "4th quarter", "2nd Half", "2nd half", " Game", " game"]]) > 0:
                quarterNo = 4
            elif "OT" in playData:
                quarterNo = "OT"
            else:
                quarterNo = "UNKNOWN END QTR"
                #raise ValueError("Could not determine quarter from {0}".format(playData))

                
        if gameclock is None and quarterNo is None:
            ## Check for start of quarter/half/game
            if sum([x in playData for x in ["Start of the ", "Start Of The ", "start of the ", "start of "]]) > 0:
                gameclock = timedelta(minutes=15, seconds=0) 
                if sum([x in playData for x in ["1st Quarter", "1st quarter"]]) > 0:
                    quarterNo = 1
                elif sum([x in playData for x in ["2nd Quarter", "2nd quarter", "1st Half", "1st half"]]) > 0:
                    quarterNo = 2
                elif sum([x in playData for x in ["3rd Quarter", "3rd quarter", "2nd Half", "2nd half"]]) > 0:
                    quarterNo = 3
                elif sum([x in playData for x in ["4th Quarter", "4th quarter", "2nd Half", "2nd half", " Game", " game"]]) > 0:
                    quarterNo = 4
                elif "OT" in playData:
                    quarterNo = "OT"
                else:
                    quarterNo = "UNKNOWN START QTR"
                    #raise ValueError("Could not determine quarter from {0}".format(playData))

        
        if gameclock is None and quarterNo is None:

            ## Check for specific format (HH:MM - 1st)
            m = re.match(r"\((.*?)\)", playData)
            if m is None:
                raise ValueError("Could not determine time and quarter from {0}".format(playData))

            try:
                text = m.group(0)
            except:
                raise ValueError("Could not extract regex result from {0}".format(playData))

               
            ## Check for overtime
            try:
                result = text[1:-1]
                if "OT" in result:
                    gameclock = timedelta(minutes=0, seconds=0) 
                    quarterNo = "OT"
            except:
                pass
            

            if gameclock is None:
                try:
                    result = text[1:-1]
                    result = result.split(" - ")
                    gameclock,quarter = result
                except:
                    raise ValueError("Could not parse time data: {0}".format(text))


                try:
                    minutes,seconds = gameclock.split(":")
                    gameclock = timedelta(minutes=int(minutes), seconds=int(seconds)) 
                except:
                    raise ValueError("Could not create timedelta for {0}".format(gameclock))


                quarterNo = {"1st":1, "2nd": 2, "3rd": 3, "4th": 4}.get(quarter)
                if quarterNo is None:
                    print("Could not find quarter from [{0}] or [{1}]".format(quarter, text))
                    #raise ValueError("Could not find quarter from [{0}] or [{1}]".format(quarter, text))


                try:
                    playData = playData.replace(text, "").strip()
                except:
                    raise ValueError("Could not remove [{0}] from [{1}]".format(text, playData))
                
        
        return gameclock,quarterNo,playData

        
    def parsePossession(self, possession, fieldMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(possession, list):
            raise ValueError("Possession is not a list: {0}".format(possession))
            
        if len(possession) != 1:
            raise ValueError("Not one element in possession list: {0}".format(possession))
            
        teamID = possession[0]
        
        teamAbbrev = None
        try:
            teamAbbrev = fieldMap[teamID]
        except:
            raise ValueError("Could not find {0} in field map: {1}".format(teamID, fieldMap))
            
        return teamAbbrev
        
        
    def augmentPlayStartWithPossession(self, possession, startVals, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if isinstance(startVals, playstartclass):
            
            ## Check for a team having the ball on their own side of the field (common)
            try:
                startY = int(startVals.startY)
            except:
                raise ValueError("Starting line {0} is not an integer".format(startVals.startY))

            if possession == startVals.side:
                distToEndZone = 100 - startY
            else:
                distToEndZone = startY                
                
            startVals.setStartY(startY)
            startVals.setDistToEndZone(distToEndZone)

        return startVals
    

    def parseHeadline(self, headline, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        pltype = None
        
        if isinstance(headline, list):
            if len(headline) >= 1:
                ptype  = playtype(headline[0])
                pltype = ptype.getPlay()
                
                if pltype is None:
                    raise ValueError("Could not determine headline play type: {0}".format(headline[0]))
            else:
                print("Not one headline entry: {0}".format(headline))
        else:
            raise ValueError("Headline is not a list: {0}".format(headline))
            
        return pltype
    
    
    def parseScore(self, score, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(score, list):
            raise ValueError("Could not determine score type: {0}".format(score))
            
        if len(score) != 1:
            raise ValueError("Not one detail entry: {0}".format(score))
            
        scoredata = score[0]
        
        try:
            scoredata = int(scoredata)
        except:
            raise ValueError("Could not find an integer score for {0}".format(scoredata))
            
        return scoredata
    
    
    def parseDetail(self, detail, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(detail, list):
            raise ValueError("Could not determine detail play type: {0}".format(detail))
            
        if len(detail) != 1:
            raise ValueError("Not one detail entry: {0}".format(detail))
            
        detaildata = detail[0]
        
        
        yards = "(yards|yard|Yds|yds|Yd|yd)"
        plays = "(play|plays)"        
        num  = "([+-?]\d+|\d+)"
        
        totalplays = None
        totalyards = None
        totalclock = None

        m = re.search(r"{0}\s{1},\s{2}\s{3},\s{4}:{5}".format(num, plays, num, yards, num, num), detaildata)
        if m is not None:
            groups = m.groups()
            totalplays = int(groups[0])
            totalyards = int(groups[2])
            totalclock = timedelta(minutes=int(groups[4]), seconds=int(groups[5]))

            
        if totalplays is None and totalyards is None and totalclock is None:
            m = re.search(r"{0}\s{1},\s{2}\s{3}".format(num, plays, num, yards), detaildata)
            if m is not None:
                groups = m.groups()
                totalplays = int(groups[0])
                totalyards = int(groups[2])
                totalclock = timedelta(minutes=0, seconds=0)
                
            
        if totalplays is None and totalyards is None and totalclock is None:
            raise ValueError("Could not parse drive detail: {0}".format(detaildata))

        drivedetail = drivedetailclass(plays=totalplays, yards=totalyards, gametime=totalclock)
            
        return drivedetail
    
    
    
        
        
        
    
    ########################################################################################################
    ##
    ## Analyze Possession For Every Play
    ##
    ########################################################################################################
    def analyzePossession(self, gameData, players, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(gameData, list):
            raise ValueError("Game data is not a list!")
            
        unknown = False

        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            prevStart  = None
            for ipl,drivePlay in enumerate(drivePlays):
                play       = drivePlay.play
                valid      = drivePlay.valid
                if valid is False:
                    continue
                possession = drivePlay.possession
                text       = possession.text
                status     = ""
                if possession.isUnknownStart():
                    unknown = True
                    status  = "<---- UNKNOWN"
                if possession.isPreviousStart():
                    if ipl == 0:
                        unknown = True
                        status  = "<---- UNKNOWN"
                    else:
                        try:
                            nextStart = drivePlays[ipl+1].possession.start
                        except:
                            nextStart = None
                        
                        if nextStart == prevStart:
                            possession.start = prevStart
                            status  = "<---- PREV/NXT"
                        else:
                            status  = "<---- PREV/UNK"
                            
                if isinstance(play, (rushingplay, passingplay)):
                    prevStart = possession.start
                keys = ",".join([k for k,v in play.pa.__dict__.items() if v is True])
                if status == "":
                    status = keys
                if debug:
                    print("{0}\t{1}\t{2}\t{3: <15}{4: <15}{5: <5}{6: <40}{7}".format(idr,ipl,str(possession.start),str(play.name),str(possession.player),str(possession.position),str(status),str(text)))
            if debug:
                print("")

        if unknown is True:
            if debug:
                print("UNKNOWN PLAY START IN GAME")
            
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
    
    
                        
    ######################################################
    ## Save Augmented Stats Data
    ######################################################
    def saveAugmentedStatsData(self, players, homeTeamMetaData, awayTeamMetaData, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        augmentedStatsFilename = setFile(self.hist.getStatisticsResultsDir(), "{0}-stats-extra.json".format(year))
        if isFile(augmentedStatsFilename) and False:
            augmentedStatsData = getFile(augmentedStatsFilename)
        else:
            augmentedStatsData = {}

        if augmentedStatsData.get(homeTeamMetaData["ID"]) is None:
            augmentedStatsData[homeTeamMetaData["ID"]] = {}
        if augmentedStatsData[homeTeamMetaData["ID"]].get('Kickers') is None:
            augmentedStatsData[homeTeamMetaData["ID"]]['Kickers'] = {}
        if augmentedStatsData[homeTeamMetaData["ID"]].get('Punters') is None:
            augmentedStatsData[homeTeamMetaData["ID"]]['Punters'] = {}

        for name in players.homeTeamPlayers.kickers:
            augmentedStatsData[homeTeamMetaData["ID"]]['Kickers'][name] = "K"
        for name in players.homeTeamPlayers.punters:
            augmentedStatsData[homeTeamMetaData["ID"]]['Punters'][name] = "P"


        if augmentedStatsData.get(awayTeamMetaData["ID"]) is None:
            augmentedStatsData[awayTeamMetaData["ID"]] = {}
        if augmentedStatsData[awayTeamMetaData["ID"]].get('Kickers') is None:
            augmentedStatsData[awayTeamMetaData["ID"]]['Kickers'] = {}
        if augmentedStatsData[awayTeamMetaData["ID"]].get('Punters') is None:
            augmentedStatsData[awayTeamMetaData["ID"]]['Punters'] = {}

        for name in players.awayTeamPlayers.kickers:
            augmentedStatsData[awayTeamMetaData["ID"]]['Kickers'][name] = "K"
        for name in players.awayTeamPlayers.punters:
            augmentedStatsData[awayTeamMetaData["ID"]]['Punters'][name] = "P"

        if debug:
            print("Saving augmented stats to {0}".format(augmentedStatsFilename))
        saveFile(idata=augmentedStatsData, ifile=augmentedStatsFilename, debug=True)                        
        
        
    
    
    
    
    
    
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
    
    
    
    ################################################################################################################################################
    ##
    ##
    ## Main Loop To Process Games
    ##
    ##
    ################################################################################################################################################
    def parseGames(self, gameID=None, test=False, debug=False, verydebug=False):
        if self.hist is None:
            raise ValueError("Must set historical class!")
            
        if verydebug:
            debug = True

        self.unknownPlays = []
        
        self.toughParsing  = ['400547724']
        self.poorlyParsed  = ['401012731', '400547781', '400547808', '400548070', '400548428', '400610207', '400547822']
        self.poorlyParsed += ['400547970', '400547835', '400548026', '400548167', '400547827', '400548458']
        self.poorlyParsed += ['400547901', '400547976', '400548246', '400548278', '400548292', '400548448']


        
        self.statsToGet = {}
        self.badGames   = {}
        self.goodGames  = {}
        
        pcc = possessionchangeclass()
        dc  = debugclass()
            
        files    = findExt(self.hist.getGamesResultsDir(), ext=".p", debug=debug)
        for ifile in files:
            print(ifile)
            try:
                year = int(getBaseFilename(ifile).split("-")[0])
            except:
                raise ValueError("Could not get year from {0}".format(ifile))
            
            if year != 2018:
                continue
                
            yearData = getFile(ifile)
            
            seasonFilename = setFile(self.hist.getSeasonResultsDir(), "{0}.p".format(year))
            seasonData     = getFile(seasonFilename)
            
            statsFilename = setFile(self.hist.getStatisticsResultsDir(), "{0}-stats.json".format(year))
            statsData     = getFile(statsFilename)
            
            augmentedStatsFilename = setFile(self.hist.getStatisticsResultsDir(), "{0}-stats-extra.json".format(year))
            augmentedStatsData     = getFile(augmentedStatsFilename)
                

            if len(self.unknownPlays) > 75:
                break


            
            
            totalGames = 0
            for gameIdent,gameData in yearData.items():
                if gameID is not None:
                    if gameID != gameIdent:
                        continue
                
                teamsMetaData    = gameData["Teams"]
                homeTeamMetaData = teamsMetaData["Home"]
                awayTeamMetaData = teamsMetaData["Away"]
                driveData        = gameData["Plays"]
                
                
                print("GAME ID: {0}".format(gameIdent))

                fieldMap = {}
                fieldMap[homeTeamMetaData["ID"]]     = homeTeamMetaData["Abbrev"]
                fieldMap[homeTeamMetaData["Abbrev"]] = homeTeamMetaData["ID"]
                fieldMap[awayTeamMetaData["ID"]]     = awayTeamMetaData["Abbrev"]
                fieldMap[awayTeamMetaData["Abbrev"]] = awayTeamMetaData["ID"]
                
                fieldMap["Home"] = homeTeamMetaData["Abbrev"]
                fieldMap["Away"] = awayTeamMetaData["Abbrev"]
                
                copmap = {}
                copmap[homeTeamMetaData["Abbrev"]] = awayTeamMetaData["Abbrev"]
                copmap[awayTeamMetaData["Abbrev"]] = homeTeamMetaData["Abbrev"]

                
                homeTeamSeasonData = seasonData.teams.get(homeTeamMetaData["ID"])
                if homeTeamSeasonData is None:
                    continue
                    raise ValueError("There is no home team season data for {0}, {1}".format(homeTeamMetaData["Abbrev"], homeTeamMetaData["ID"]))
                homeTeamGameData = [x["Game"] for x in homeTeamSeasonData.games if x["Game"].gameID == gameIdent]
                try:
                    homeTeamGameData = homeTeamGameData[0]
                except:
                    continue
                    raise ValueError("There is no home team game data")

                awayTeamSeasonData = seasonData.teams.get(awayTeamMetaData["ID"])
                if awayTeamSeasonData is None:
                    continue
                    raise ValueError("There is no away team season data for {0}, {1}".format(awayTeamMetaData["Abbrev"], awayTeamMetaData["ID"]))
                awayTeamGameData = [x["Game"] for x in awayTeamSeasonData.games if x["Game"].gameID == gameIdent]
                try:
                    awayTeamGameData = awayTeamGameData[0]
                except:
                    continue
                    raise ValueError("There is no away team game data")

                
                


                if gameIdent in self.hist.noGameData:
                    continue
                    
                if gameIdent in self.poorlyParsed:
                    continue
                    
                if gameIdent in self.toughParsing:
                    continue
                                
                
                ################################################################################
                ### Learn key plays for use in determining possession
                ################################################################################
                players = gameplayers(teamsMap=fieldMap, statsData=statsData)
                players.augmentData(augmentedStatsData)
                
                possData = possessionclass(players)
                
                if debug:
                    print("")
                    print("  Home Team: {0}".format(homeTeamMetaData))
                    print("\tPassers\t",players.homeTeamPlayers.passers)
                    print("\tRunners\t",players.homeTeamPlayers.runners)
                    print("\tKickers\t",players.homeTeamPlayers.kickers)
                    print("\tFGKickers\t",players.homeTeamPlayers.fgkickers)
                    print("\tPunters\t",players.homeTeamPlayers.punters)
                    print("")
                    print("  Away Team: {0}".format(awayTeamMetaData))
                    print("\tPassers\t",players.awayTeamPlayers.passers)
                    print("\tRunners\t",players.awayTeamPlayers.runners)
                    print("\tKickers\t",players.awayTeamPlayers.kickers)
                    print("\tFGKickers\t",players.awayTeamPlayers.fgkickers)
                    print("\tPunters\t",players.awayTeamPlayers.punters)
                    print("")


                
                if test:
                    saveFile(idata=driveData, ifile="testDriveData.p", debug=True)
                    saveFile(idata=fieldMap,  ifile="testFieldMap.p",  debug=True)
                    saveFile(idata=statsData,  ifile="testGameStats.p", debug=True)
                    saveFile(idata=augmentedStatsData,  ifile="testAugStats.p", debug=True)
                    1/0

                if len(self.unknownPlays) > 75:
                    break
                    
                
                gameResult = []
                totalPlays = 0
                
                
                ################################################################################
                ### Collect Post Drive Scores
                ################################################################################
                postDriveScores = {"Drives": [], "Final": []}
                postDriveScores["Final"] = [awayTeamGameData.teamAScore, homeTeamGameData.teamAScore]
                
                
                ################################################################################
                ### Iterate over drives
                ################################################################################
                for idr,drive in enumerate(driveData):
                    ### Fix known drive problems
                    #drive = self.fixDrive(gameIdent, idr, drive)
                    
                    driveNo    = drive['Drive']
                    headline   = drive['Headline']
                    detail     = drive['Detail']
                    ### For whatever reason home/away scores are reversed on the webpage...
                    homescore  = drive['AwayScore']
                    awayscore  = drive['HomeScore']
                    possession = drive['Posession'] ## note this needs to change later
                    drivedata  = drive['Data']
                    
                    
                    
                    if debug:
                        print("Drive: {0} \t{1} (H) - {2} (A)".format(idr,homescore, awayscore))
                    
    
                    ## Determine possession as defined in the play start fields later
                    possession = self.parsePossession(possession, fieldMap)
                    headline   = self.parseHeadline(headline)
                    detail     = self.parseDetail(detail)
                    homescore  = self.parseScore(homescore)
                    awayscore  = self.parseScore(awayscore)
                    
                    postDriveScores["Drives"].append([awayscore, homescore])
            
        
                    fullDriveData = driveclass(headline=headline, detail=detail, possession=possession,
                                              postdrivehomescore=homescore, postdriveawayscore=awayscore)
                    
                    drivePlays = []
            
                
                    ################################################################################
                    ### Iterate over plays in drive
                    ################################################################################
                    for ipl,play in enumerate(drivedata):
                        playNo        = play['Play']
                        playStartText = play['Start']
                        playData      = play['Data']
                        

                        ### Determine play starting position and clock
                        startVals = self.parsePlayStart(playStartText, playNo, len(drivedata), playData, debug=verydebug)
                        startVals = self.augmentPlayStartWithPossession(possession, startVals, debug=False)
                        
                        ### Determine type of play
                        playResult = self.parsePlayData(startVals, playData, fieldMap, possData, gameIdent, idr, ipl, debug=False, verydebug=verydebug)
                        if playResult is None:
                            continue
                        
                        if playResult.possession.start is None and playResult.valid is True:
                            raise ValueError("ERROR WITH POSSESSION:",playResult.play.name,'\t',playResult.play.text)
                        
                        totalPlays += 1
                        drivePlays.append(playResult)
                        
                        ### Check if we need to insert a play
                        newPlay = self.addPlay(gameIdent, idr, ipl, playResult, possData, verydebug)
                        if newPlay is not None:
                            totalPlays += 1
                            drivePlays.append(newPlay)
                        


                    
                    fullDriveData.setPlays(drivePlays)
                    #fullDriveData = self.insertMissingData(gameIdent, idr, fullDriveData, debug)
                    #fullDriveData = self.augmentPlayWithScore(fullDriveData, fieldMap, debug)
                    gameResult.append(fullDriveData)


                
                
                ################################################################################
                ### Analyze Possession
                ################################################################################ 
                dc.showGame(gameResult, debug=debug)
                gameResult = self.analyzePossession(gameResult, players, debug=debug)
                #gameResult = self.analyzeKickoffs(gameResult, players, copmap, debug=debug)
                #gameResult = self.analyzeInterceptions(gameResult, players, debug=debug)
                gameResult = pcc.splitChangeOfPossession(gameResult, players, copmap, debug=debug)
                gameResult = self.analyzePenaltiesAndTOs(gameResult, players, debug=debug)
                gameResult = self.analyzePossession(gameResult, players, debug=debug)
                gameResult = self.analyzeReturns(gameResult, players, copmap, debug=debug)
                gameResult = self.analyzePATs(gameResult, players, copmap, debug=debug)
                gameResult = self.analyzeEndOfGame(gameResult, players, postDriveScores, debug=debug)
                
                dc.showGame(gameResult, debug=debug)
                
                scoreResult = self.analyzeGameScore(gameResult, players, homeTeamGameData, awayTeamGameData, debug=True)
                if scoreResult is False:
                    if gameID is None:
                        self.badGames[gameIdent] = True
                        continue
                    dc.showGame(gameResult, debug=True)
                    
                    saveFile(idata=driveData, ifile="testDriveData.p", debug=True)
                    saveFile(idata=fieldMap,  ifile="testFieldMap.p",  debug=True)
                    saveFile(idata=statsData,  ifile="testGameStats.p", debug=True)
                    saveFile(idata=augmentedStatsData,  ifile="testAugStats.p", debug=True)
                    
                    raise ValueError("There was a problem parsing the scores for this game {0}!".format(gameIdent))
                else:
                    self.goodGames[gameIdent] = True
                #self.saveAugmentedStatsData(players, homeTeamMetaData, awayTeamMetaData, debug)
                
                
                #self.analyzeGameData(gameResult)


                    
                totalGames += 1
                if debug:
                    print("Found {0} plays in this game {1}".format(totalPlays, gameID))
                    
            print("Found {0} total games for {1}".format(totalGames, ifile))


    ########################################################################################################
    ## Necessary Edits To The Text
    ########################################################################################################
        
        
    def editText(self, text, gameID, driveNo, playNo):
        newtext = text
        keep    = True
        if gameID == "400547673":
            if driveNo == 15 and playNo == 14:
                newtext = "Lazedrick Thompson run for 4 yds for a TD, (Andrew DiRocco MISSED)"
        if gameID == "400547680":
            if driveNo == 29 and playNo == 3:
                newtext = "(3OT) Terrence Franks 2 Yd Run for a TD"
        if gameID == "400547693":
            if driveNo == 9 and playNo == 2:
                newtext = "Garrett Krstich sacked by Jeff Luc for a loss of 6 yards Garrett Krstich fumbled, recovered by Cincy Nick Temple , return for 0 yards , return for 27 yds (Two-Point Pass Conversion Failed)"
            if driveNo == 9 and playNo > 2:
                keep = False
        if gameID == '400548197':
            if driveNo == 6 and playNo == 12-1:
                keep = False
        if gameID == '400547890':
            #print(gameID,driveNo,playNo,'\t',text)
            if driveNo == 21 and playNo == 9-1:
                newtext = "Dylan Cantrell 39 Yd pass from Patrick Mahomes for a TD"
        if gameID == '400548388':
            if driveNo == 31 and playNo == 3-1:
                newtext = "(3OT) Matt Jones 1 Yd Run for a TD"
        if gameID == '400548061':
            if driveNo == 1 and playNo == 2-1:
                keep = False
        if gameID == "400548315":
            if driveNo == 15 and playNo == 0:
                keep = False
        if gameID == "400547757":
            if driveNo == 21 and playNo == 3:
                newtext = "(2OT) Thomas Sirk 5 Yd Run for a TD"
        if gameID == '400548151':
            if driveNo == 0 and playNo == 2:
                newtext = "Joe Licata pass intercepted for a TD DeAndre Scott return for 37 yds for a TD (PAT)"
        if gameID == '400547710':
            if driveNo == 30 and playNo == 1:
                newtext = "Terrell Hartsfield 27 Yd Fumble Return for a TD"                
        if gameID == '400547816':
            if driveNo == 14 and playNo == 11:
                keep = False     
        if gameID == '400548301':
            if driveNo == 6 and playNo == 2:
                newtext = "Sefo Liufau sacked by Anthony Lopez for a loss of 7 yards Sefo Liufau fumbled, recovered by Ariz Tra'Mayne Bondurant , return for 0 yards , return for 22 yds for a TD (PAT)"                
        if gameID == '400609076':
            if driveNo == 30 and playNo == 0:
                newtext = "Jerrard Randall 25 Yd Run for a TD"  
        if gameID == '400548444':
            if driveNo == 15 and playNo == 7:
                keep = True
                newtext = "Teldrick Morgan 42 Yd pass from Tyler Rogers for a TD (Defensive PAT)"
        if gameID == '400548000':
            if driveNo == 11 and playNo == 4:
                newtext = "Melvin Gordon run for 14 yds for a TD (PAT)"   
            if driveNo == 23 and playNo == 7:
                newtext = "Anthony Jennings pass complete to John Diarse for 35 yds for a TD (Two pt pass, Anthony Jennings pass to Trey Quinn GOOD)"                
        if gameID == '400547966':
            if driveNo == 3 and playNo == 0:
                newtext = "Ryan Santoso kickoff for 61 yds , De'Mornay Pierson-El return for 16 yds to the Neb 20."    
        if gameID == '400547827':
            if driveNo == 0 and playNo == 0:
                newtext = "Mitchell Ludwig kickoff , Andrew Motuapuaka 11 Yd Fumble Return (Joey Slye PAT blocked)"     
        if gameID == '400548109':
            if driveNo == 9 and playNo == 0:
                newtext = "Adam Butler 0 Yd Fumble Return for a TD"               
        if gameID == '400547980':
            if driveNo == 3 and playNo == 5:
                newtext = "Austin Collinsworth 32 Yd Fumble Return for a TD (Defensive PAT)"
        if gameID == '401021670':
            if driveNo == 22 and playNo == 3:
                newtext = "Cephus Johnson pass intercepted for a TD Alvin Ward Jr. return for 28 yds for a TD, (Tyler Bass KICK)"
                
        return newtext,keep    
    

    def addPlay(self, gameID, driveNo, prevPlayNo, prevPlay, possData, debug=False):
        debug = True
        text = None
        if gameID == "401012282":
            if driveNo == 8 and prevPlayNo == 11:
                text = "Tyrel Dodson 78 Yd Return of Blocked Field Goal (Seth Small Kick)"
                print(prevPlay)

        if text is not None:
            ptype = playtype(text)
            play  = ptype.getPlay()
            play.analyze(debug=debug)
            playPossession = possData.determinePossession(play, debug=debug)
            playStart = prevPlay.start
            playResult = playclass(possession=playPossession, start=playStart, play=play, valid=True)
            if debug:
                print("Adding play [{0}] for team [{1}] with text [{2}]".format(play.name, playPossession.start, text))
            return playResult
        
        return None
            
_, _ = clock("Last Run")


# In[74]:


#tsc = teamstatisticsclass()
#tsc.collect(hist, test=False, debug=True)


# In[76]:

