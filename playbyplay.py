#!/usr/bin/env python
# coding: utf-8

# # Football Parsing Code



## Python Version
import sys
print("Python: {0}".format(sys.version))

import sys

from espngames import espn, output

import datetime as dt
start = dt.datetime.now()



from playResult import playtextclass
from possession import possessionfromplayer
from playTypes import playtype

from fileUtils import getBaseFilename
from ioUtils import getFile

from debug import debugclass
from changePossession import possessionchangeclass
from gamePlayers import gameplayers
from playStart import playstart
from playClock import playclock
from playTypes import playsummary
from analyzePossession import analyzepossession
from analyzeYards import analyzeyards
from analyzeKicking import analyzekicking

from driveSummary import drivesummary

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


#############################################################################################################
##
## Play-By-Play
##
#############################################################################################################
class playbyplay(espn, output):
    def __init__(self):
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 0*" "
        
        self.name = "playbyplay"
        espn.__init__(self)
        output.__init__(self)
        
        self.hist = None
        self.ptc  = playtextclass()
        
    def setHistorical(self, hist):
        self.hist = hist
    
    
    ########################################################################################################
    ##
    ## Make Maps
    ##
    ########################################################################################################
    def makeFieldMap(self, awayTeamMetaData, homeTeamMetaData):
        fieldMap = {}
        fieldMap[homeTeamMetaData["ID"]]     = homeTeamMetaData["Abbrev"]
        fieldMap[homeTeamMetaData["Abbrev"]] = homeTeamMetaData["ID"]
        fieldMap[awayTeamMetaData["ID"]]     = awayTeamMetaData["Abbrev"]
        fieldMap[awayTeamMetaData["Abbrev"]] = awayTeamMetaData["ID"]
        
        fieldMap["Home"] = homeTeamMetaData["Abbrev"]
        fieldMap["Away"] = awayTeamMetaData["Abbrev"]
        
        self.logger.debug("Field Map:")
        self.logger.debug("  {0}".format(fieldMap))
        
        return fieldMap
        
        
    
    def makeCopMap(self, awayTeamMetaData, homeTeamMetaData):
        copmap = {}
        copmap[homeTeamMetaData["Abbrev"]] = awayTeamMetaData["Abbrev"]
        copmap[awayTeamMetaData["Abbrev"]] = homeTeamMetaData["Abbrev"]  
        
        self.logger.debug("Cop Map:")
        self.logger.debug("  {0}".format(copmap))
        
        return copmap
    
    
    ########################################################################################################
    ##
    ## Team Player Data
    ##
    ########################################################################################################
    def getTeamGameData(self, gameID, seasonData, teamMetaData):
        teamID = teamMetaData["ID"]
        teamSeasonData = seasonData.teams.get(teamID)
        if teamSeasonData is None:
            self.logger.warn("Could not find season data for team ID {0}".format(teamID))
            self.logger.debug("Available Teams: {0}".format(sorted(seasonData.teams.keys())))
            return None
        teamGameData = [x["Game"] for x in teamSeasonData.games if x["Game"].gameID == gameID]
        try:
            teamGameData = teamGameData[0]
            self.logger.debug("Found game data for team ID {0} and game ID {1}".format(teamID, gameID))
        except:
            self.logger.warn("Could not find game data for team ID {0} and game ID {1}".format(teamID, gameID))
            self.logger.debug("Available Teams: {0}".format(sorted(seasonData.teams.keys())))
            return None
        return teamGameData
    
    
    
    
    ################################################################################################################################################
    ##
    ##
    ## Main Loop To Process Games
    ##
    ##
    ################################################################################################################################################
    def parseGames(self, gameID=None, test=False, debug=False, verydebug=False):       
        self.logger.info("Parsing Games")
        
        
        if self.hist is None:
            raise ValueError("Must set historical class!")
            
        sep = "======================================================"
            
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
        
        dc  = debugclass()
            
        files = self.hist.getGamesResultsFiles()
        for ifile in files:
            try:
                year = int(getBaseFilename(ifile).split("-")[0])
            except:
                raise ValueError("Could not get year from {0}".format(ifile))
            
            if year != 2018:
                continue
                
            self.logger.info(" Parsing Games from {0}".format(year))
            
            yearData           = getFile(ifile)
            seasonData         = self.hist.getSeasonResultsData(year)            
            statsData          = self.hist.getStatisticsResultsData(year)
            augmentedStatsData = self.hist.getStatisticsAugmentedData(year)
            
            
            totalGames = 0
            for gameIdent,gameData in yearData.items():
                if gameID is not None:
                    if gameID != gameIdent:
                        continue
                
                if gameIdent in self.hist.noGameData or gameIdent in self.poorlyParsed or gameIdent in self.toughParsing:
                    continue
                
                self.logger.info("  Parsing Game ID {0}".format(gameIdent))
                
                
                teamsMetaData    = gameData["Teams"]
                homeTeamMetaData = teamsMetaData["Home"]
                awayTeamMetaData = teamsMetaData["Away"]
                driveData        = gameData["Plays"]
                
                ################################################################################
                ### Get maps
                ################################################################################
                fieldMap         = self.makeFieldMap(awayTeamMetaData, homeTeamMetaData)
                copmap           = self.makeCopMap(awayTeamMetaData, homeTeamMetaData)
                
                
                ################################################################################
                ### Get team data
                ################################################################################
                homeTeamGameData = self.getTeamGameData(gameIdent, seasonData, homeTeamMetaData)
                if homeTeamGameData is None:
                    continue
                awayTeamGameData = self.getTeamGameData(gameIdent, seasonData, awayTeamMetaData)
                if awayTeamGameData is None:
                    continue
            
                                
                
                ################################################################################
                ### Learn key plays for use in determining possession
                ################################################################################
                players = gameplayers(teamsMap=fieldMap, statsData=statsData)
                players.augmentData(augmentedStatsData)
                
                
                pfp = possessionfromplayer(players)                    
                ps  = playstart()
                pc  = playclock()
                pt  = playtype()
                ap  = analyzepossession(copmap, players)
                ay  = analyzeyards()
                ak  = analyzekicking()
                pcc = possessionchangeclass(copmap)
                
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
                    self.logger.debug("\n\n{0}".format(2*sep))
                    self.logger.debug("{0}Parsing Plays for Drive {1}".format(self.ind, idr))
                    
                    ds = drivesummary(drive, fieldMap)
                    drivePlays = ds.getDrivePlays()
                        
                    postDriveScores["Drives"].append(ds.getPostDriveScore())
            
                
                    ################################################################################
                    ### Iterate over plays in drive
                    ################################################################################
                    driveResults = []
                    for ipl,drivePlay in enumerate(drivePlays):
                        #playNo        = drivePlay['Play']
                        playStartText = drivePlay['Start']
                        playData      = drivePlay['Data']
                        self.logger.debug("\n  {0}".format(sep))
                        self.logger.debug("{0}  Play {1}/{2}: {3}".format(self.ind, ipl, len(drivePlays), playData))
                        

                        ### Determine play starting position
                        startVals = ps.getStart(playStartText)
                        
                        
                        ### Determine play clock and quarter
                        pc.parsePlay(playData)
                        startVals.setClock(pc)
                        playText = pc.getPlayText()
        
        
                        ### Determine play type
                        play  = pt.getPlay(playText)
                        
#                                        
                        ### Determine possession
                        playPossession = pfp.determinePossession(play)
                        if playPossession.isForced() is not None:
                            play.pa.forced = playPossession.isForced()
                
                            
                        ### Result of play
                        playResult = playsummary(possession=playPossession, start=startVals, play=play, valid=play.valid)


                        ### Save and move on                        
                        totalPlays += 1
                        driveResults.append(playResult)
                        continue
                        
                        ### Check if we need to insert a play
                        #newPlay = self.addPlay(gameIdent, idr, ipl, playResult, possData, verydebug)
                        #if newPlay is not None:
                        #    totalPlays += 1
                        #    driveResults.append(newPlay)
                        


                    fullDriveData = ds.getFullDrive()
                    fullDriveData.setPlays(driveResults)
                    #fullDriveData = self.insertMissingData(gameIdent, idr, fullDriveData, debug)
                    #fullDriveData = self.augmentPlayWithScore(fullDriveData, fieldMap, debug)
                    gameResult.append(fullDriveData)


                
                ################################################################################
                ### Show State Before Alterations
                ################################################################################
                self.logger.debug("\n{0}".format(2*sep))
                self.logger.debug("{0}Found {1} Drives For This Game".format(self.ind, len(gameResult)))
                self.logger.debug("\n{0}\n".format(2*sep))
                
                
                
                ################################################################################
                ### Analyze Possession
                ################################################################################ 
                dc.showGame(gameResult)
                
                gameResult = ap.continuity(gameResult)
                gameResult = pcc.splitChangeOfPossession(gameResult)
                
                gameResult = ap.continuity(gameResult)                
                gameResult = ap.returns(gameResult)
                gameResult = ap.pats(gameResult)
                gameResult = ap.endofgame(gameResult, postDriveScores)
                gameResult = ap.noplays(gameResult)
                gameResult = ap.nextplay(gameResult)
                gameResult = ap.endofdrive(gameResult)
                
                

                dc.showGame(gameResult, "Game")
                gameResult = ay.analyze(gameResult)
                
                
                gameResult = ak.kickoffs(gameResult)
                gameResult = ak.returns(gameResult)
                

                scoreResult = ap.gamescore(gameResult, postDriveScores)
                
                if scoreResult is False:
                    if gameID is None:
                        self.badGames[gameIdent] = True
                        continue
                    dc.showGame(gameResult, "Score Is Not Corrent")
                dc.showGame(gameResult, "Good Game")
                
                
                totalGames += 1
                if debug:
                    self.logger.info("Found {0} plays in this game {1}".format(totalPlays, gameID))
                    
            self.logger.info("Found {0} total games for {1}".format(totalGames, ifile))


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
            playResult = playsummary(possession=playPossession, start=playStart, play=play, valid=True)
            if debug:
                print("Adding play [{0}] for team [{1}] with text [{2}]".format(play.name, playPossession.start, text))
            return playResult
        
        return None