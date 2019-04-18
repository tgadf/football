from os.path import join
from fsUtils import mkSubDir, setFile, isFile, removeFile, isDir
from ioUtils import getFile, saveFile
from fileUtils import getBaseFilename, getBasename, getDirname
from webUtils import getWebData, getHTML
from timeUtils import printDateTime, getDateTime, addMonths
from searchUtils import findExt
from time import sleep
from random import random
import re

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))



class output:
    def __init__(self):
        self.name   = "output"
        self.dirval = "/Volumes/Blue/Football"
        if not isDir(self.dirval):
            self.dirval = "/Users/tgadfort/Documents/football"


        
    def getSaveDir(self):
        return self.dirval

    
class espn:
    def __init__(self):
        self.name = "espn"
        self.baseurl = "http://www.espn.com"
        
    def getBase(self):
        return self.baseurl


############################################################################################################
# Game Class
############################################################################################################
class game:
    def __init__(self, gameID, date, teamA, teamB, teamAResult, teamBResult, teamAScore, teamBScore, location, extra={}):
        self.gameID = gameID
        self.date   = date
        self.teamA  = teamA
        self.teamB  = teamB
        self.teamAScore  = teamAScore
        self.teamBScore  = teamBScore
        self.teamAResult  = teamAResult
        self.teamBResult  = teamBResult
        self.location = location
        
        self.OT   = extra.get('OT')
        self.Bowl = extra.get('Bowl')

    def getWinner(self):
        if self.teamAScore > self.teamBScore:
            return self.teamA
        elif self.teamAScore < self.teamBScore:
            return self.teamB
        else:
            return "T"

        
    def getGame(self):
        retval = {"GameID": self.gameID}
        return retval

        
        
############################################################################################################
# Team Class
############################################################################################################
class team:
    def __init__(self, year, teamName, teamMascot, teamID):
        self.year       = year
        self.teamName   = teamName
        self.teamMascot = teamMascot
        self.teamID     = teamID
        self.games      = []

        
    def getTeamID(self):
        return self.teamID
    
        
    def addGame(self, game):
        result = game.teamAResult
        self.games.append({"Result": result, "Game": game})

            
    def setStatistics(self):
        wins   = sum([x["Result"] == "W" for x in self.games])
        losses = sum([x["Result"] == "L" for x in self.games])
        ties   = sum([x["Result"] == "T" for x in self.games])
        ngames = len(self.games)
        if ngames != wins+losses+ties:
            raise ValueError("The sum of wins, losses, and ties does not match total number of games!")
        self.wins   = wins
        self.losses = losses
        self.ties   = ties
        self.ngames = ngames

        
    def summary(self):
        print("{0: <6}{1: <50}{2: <5}{3: <5}{4: <5}{5: <5}".format(self.year, self.teamName, 
                                                                   self.wins, self.losses, self.ties, self.ngames))
        
        
    def getGames(self):
        return self.games
        
        
############################################################################################################
# Season Class
############################################################################################################
class season:
    def __init__(self, year):
        self.year  = year
        self.teams = {}
        self.games = {}
        
    def getYear(self):
        return self.year
    
    def addTeam(self, team):
        teamID = team.getTeamID()
        self.teams[teamID] = team