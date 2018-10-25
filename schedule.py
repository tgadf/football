#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 07:26:05 2017

@author: tgadfort
"""

import sys
from collections import Counter
if '/Users/tgadfort/Python' not in sys.path:
    sys.path.insert(0, '/Users/tgadfort/Python')

from fsio import setFile
from fileio import save
from path import getTeamsDBDir, getSchedulesDBDir
from db import getTeamsDB, addTeam
from htmlParser import getHTML, removeTag
from strdate import parseDateWithoutYear,getYear
from download import getURL


def getTeamBaseURL():
    return "http://espn.go.com/college-football/team/_/id/"
def getTeamScheduleBaseURL():
    return "http://espn.go.com/college-football/team/schedule/_/id/"


def downloadTeamURL(teamID, yearID = None, teamName = None, debug = False):
    teamsDBDir = getTeamsDBDir()
    if yearID:
        savename = setFile(teamsDBDir, teamID+"-"+yearID+".p")
        url      = getTeamScheduleBaseURL()+teamID+"/year/"+yearID+"/"
    else:
        savename = setFile(teamsDBDir, teamID+".p")
        url        = getTeamBaseURL()+teamID

    if debug:
        print "Downloading",teamID,"team (",teamName,yearID,") file."
        
    getURL(url, savename, debug)
    
    
def downloadTeamURLs(debug = False):
    teamsDB = getTeamsDB(debug)
    for teamName,teamID in teamsDB.iteritems():
        downloadTeamURL(teamID, yearID = None, teamName = teamName, debug = debug)


def downloadTeamSchedule(teamID, yearID, teamName = None, debug = False):
    downloadTeamURL(str(teamID), yearID = yearID, teamName = teamName, debug = debug)
    
    
def downloadTeamSchedules(yearID = None, debug = False):
    teamsDB = getTeamsDB(debug)
    if yearID == None:
        years = [str(x) for x in range(2016,2002,-1)]
    else:
        years = [str(yearID)]
        
    for year in years:
        for teamName,teamID in teamsDB.iteritems():
            downloadTeamSchedule(teamID, year, teamName, debug)
        

def getTeamSchedule(teamID, yearID = None, debug = False):
    schedulesDBDir = getSchedulesDBDir()
    if yearID:
        savename = setFile(schedulesDBDir, teamID+"-"+yearID+".p")
    else:
        savename = setFile(schedulesDBDir, teamID+".p")
        
    data = []

    teamsDB = getTeamsDB(debug)
    teamIDs = {v: k for k,v in teamsDB.iteritems()}

    bsdata = getHTML(savename)
    for table in bsdata.findAll("table"):
        for tr in table.findAll("tr"):
            tds = tr.findAll("td")
            if len(tds) == 4:
                dte  = tds[0]
                opp  = tds[1]
                res  = tds[2]

                if dte.text.find(", Jan ") != -1:
                    iYear = int(yearID)+1
                else:
                    iYear = int(yearID)
                gameDate = parseDateWithoutYear(dte.text, iYear)
                #print dte,'\t',yearID,'\t',iYear,'\t',gameDate
                if gameDate == None:
                    continue
                
                status  = opp.find("li", {"class": "game-status"})
                gameLoc = status.text
                
                oppname = opp.find("li", {"class": "team-name"})

                result  = res.find("li", {"class": "game-status"})
                score   = res.find("li", {"class": "score"})
                
                try:
                    oppData = oppname.find("a").attrs['href']
                    oppID   = oppData.split("/")[-2]
                except:
                    if debug:
                        print "Unknown team",oppname
                        print "Skipping..."
                    continue
                
                isFBS = True
                if teamIDs.get(oppID) == None:
                    oppTeamName = oppData.split("/")[-1]                    
                    downloadTeamSchedule(oppID, yearID, oppTeamName, debug = True)
                    addTeam(oppID, oppTeamName, debug = True)
                    

                ref        = score.find("a")
                try:
                    recapData = ref.attrs['href']
                    recapID = recapData.split("/")[-1]
                except:
                    recapID = None
                gameScore  = score.text.split("-")
                
                if len(gameScore) == 1:
                    continue
                
                try:
                    gameResult = result.text
                except:                    
                    raise ValueError("Unknown Result",res)
                
                try:
                    extra = gameScore[1].split()[1]
                    gameScore[1] = gameScore[1].split()[0]
                except:
                    extra = None
                
                if gameResult == "W":
                    teamScore = gameScore[0]
                    oppScore  = gameScore[1]
                elif gameResult == "L":
                    teamScore = gameScore[1]
                    oppScore  = gameScore[0]
                elif gameResult == "T":
                    teamScore = gameScore[1]
                    oppScore  = gameScore[0]
                else:
                    raise ValueError("Unknown result:",gameResult)
                
                if gameLoc == "vs":
                    location = teamID
                elif gameLoc == "@":
                    location = oppID
                else:
                    raise ValueError("Unknown location:",location)

                locCheck = removeTag(oppname, 'a', debug)
                if locCheck.text.find("*") != -1:
                    location = 0
                
                game = {"Location": location, "Date": gameDate, "TeamID": teamID, 
                        "Opponent": oppID,  "TeamScore": teamScore, "Extra": extra,
                        "FBS": isFBS, "OpponentScore": oppScore, "RecapID": recapID}
                
                
                data.append(game)
                if debug:
                    print game
                    print ''
                
    return data


def getTeamScheduleMetadata(schedule, debug = False):
    if not isinstance(schedule, list):
        raise ValueError("Schedule is not a dict!")
    
    games   = len(schedule)
    season  = None
    wins    = {"Total": 0, "Home": 0, "Away": 0, "Neutral": 0}
    losses  = {"Total": 0, "Home": 0, "Away": 0, "Neutral": 0}
    ties    = {"Total": 0, "Home": 0, "Away": 0, "Neutral": 0}

    
    yearCntr = Counter()
    for game in schedule:
        year = getYear(game["Date"])        
        yearCntr[year] += 1
        
        if game["TeamScore"] > game["OpponentScore"]:
            if game["Location"] == game["TeamID"]:
                wins["Home"] += 1
            elif game["Location"] == game["Opponent"]:
                wins["Away"] += 1
            elif game["Location"] == 0:
                wins["Neutral"] += 1
            else:
                raise ValueError("Could not understand game location:",game["Location"])
        elif game["TeamScore"] < game["OpponentScore"]:
            if game["Location"] == game["TeamID"]:
                losses["Home"] += 1
            elif game["Location"] == game["Opponent"]:
                losses["Away"] += 1
            elif game["Location"] == 0:
                losses["Neutral"] += 1
            else:
                raise ValueError("Could not understand game location:",game["Location"])
        else:
            if game["Location"] == game["TeamID"]:
                ties["Home"] += 1
            elif game["Location"] == game["Opponent"]:
                ties["Away"] += 1
            elif game["Location"] == 0:
                ties["Neutral"] += 1
            else:
                raise ValueError("Could not understand game location:",game["Location"])

    if len(yearCntr) > 0:
        season = yearCntr.most_common(1)[0][0]
    wins["Total"]   = wins["Home"]   + wins["Away"]   + wins["Neutral"]
    losses["Total"] = losses["Home"] + losses["Away"] + losses["Neutral"]
    ties["Total"]   = ties["Home"]   + ties["Away"]   + ties["Neutral"]

    home    = {"Total": 0, "Wins": wins["Home"], "Losses": losses["Home"], "Ties": ties["Home"]}
    away    = {"Total": 0, "Wins": wins["Away"], "Losses": losses["Away"], "Ties": ties["Away"]}
    neutral = {"Total": 0, "Wins": wins["Neutral"], "Losses": losses["Neutral"], "Ties": ties["Neutral"]}

    home["Total"] = home["Wins"] + home["Losses"] + home["Ties"]
    away["Total"] = away["Wins"] + away["Losses"] + away["Ties"]
    neutral["Total"] = neutral["Wins"] + neutral["Losses"] + neutral["Ties"]
    
    metaData = {"Games": games, "Season": season, "Wins": wins["Total"], 
                "Losses": losses["Total"], "Ties": ties["Total"], 
                "Home": home["Total"], "Away": away["Total"], "Neutral": neutral["Total"],
                "Details": {}}
    del wins["Total"]
    del losses["Total"]
    del ties["Total"]
    del home["Total"]
    del away["Total"]
    del neutral["Total"]
    metaData["Details"]["Wins"] = wins
    metaData["Details"]["Losses"] = losses
    metaData["Details"]["Ties"] = ties
    metaData["Details"]["Home"] = home
    metaData["Details"]["Away"] = away
    metaData["Details"]["Neutral"] = neutral
            
    return metaData


def createTeamSchedules(yearID, debug = False):
    yearID = str(yearID)
    teamsDB = getTeamsDB(debug)
    data    = {}
    for teamName,teamID in teamsDB.iteritems():
        if debug:
            print teamID,'\t',teamName
        games = getTeamSchedule(teamID, yearID, debug)
        data[teamID]  = getTeamScheduleMetadata(games)
        data[teamID]["Games"] = games
            
    savename   = setFile(getSchedulesDBDir(), yearID+".json")
    save(savename, data, debug = True)