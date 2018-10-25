#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 21:40:51 2017

@author: tgadfort
"""

import sys
import hashlib
if '/Users/tgadfort/Python' not in sys.path:
    sys.path.insert(0, '/Users/tgadfort/Python')

from fsio import setFile, isFile
from fileio import get
from path import getTeamsDBDir, getSchedulesDBDir, getNetworkDBDir
from strdate import getWeek


def getUniqueGames(schedules, debug = False):
    
    games = {}
    for teamID,teamGames in schedules.iteritems():        
        for game in teamGames["Games"]:
            oppID = game["Opponent"]

            m = hashlib.md5()
            m.update(str(game['Date']))
            m.update(str(min(teamID, oppID)))
            uid = m.hexdigest()
            if games.get(uid) == None:
                games[uid] = game
                     
                     
    games = games.values()
    
    if debug:
        print "Found",len(games),"games in this season."
        
    return games
            


def createNetworkMap(yearID, schedules, teamsData, debug = False):
    
    nodes   = {}
    edges   = []
    
    games   = getUniqueGames(schedules, debug)
 
    for game in games:
        teamID = game["TeamID"]
        oppID  = game["Opponent"]
        
        try:
            teamDiv = teamsData[teamID]["Division"]
            oppDiv  = teamsData[oppID]["Division"]
        except:
            continue
                
        if teamDiv != "FBS" and oppDiv != "FBS":
            continue
            
        if nodes.get(teamID) == None:
            group = teamsData[teamID]["Conference"]
            label = teamsData[teamID]["Team"]
            value = 1
            title  = ""
            nodes[teamID] = {"id": teamID, "label": label,  "group": group, 
                             "value": value, "title": title}
        
        if nodes.get(oppID) == None:
            group = teamsData[oppID]["Conference"]
            label = teamsData[oppID]["Team"]
            value = 1
            title  = ""
            nodes[oppID] = {"id": oppID, "label": label,  "group": group,
                            "value": value, "title": title}

        edges.append([teamID,oppID])


    f = open(getNetworkDBDir()+"/"+yearID+".edges.csv", "w")
    f.write("from,to\n")
    nGames = 0
    for edge in edges:
        nGames += 1
        f.write(str(edge[0])+","+str(edge[1])+"\n")
    f.close()
    print "Wrote",nGames,"games to",f.name

    f = open(getNetworkDBDir()+"/"+yearID+".nodes.csv", "w")
    f.write("id,label,group,value,title\n")
    nTeams = 0
    for node,nodeData in nodes.iteritems():
        nTeams += 1
        group = nodeData["group"]
        group = group.replace(" Conference", "")
        f.write(",".join([str(nodeData["id"]),nodeData["label"],group,
                    str(nodeData["value"]),nodeData["title"]])+"\n")
    f.close()
    print "Wrote",nTeams,"teams to",f.name
    
    
    
def createGameRankingData(yearID, schedules, teamsData, debug = False):

    btdata  = []    
    mvdata  = []
    elodata = []
    grdata  = []
    games   = getUniqueGames(schedules, debug)
    
    for game in games:
        teamID = game["TeamID"]
        oppID  = game["Opponent"]
        date   = game["Date"]
        week   = getWeek(date)
        
        try:
            teamName  = teamsData[teamID]["Team"]
            oppName   = teamsData[oppID]["Team"]
        except:
            continue
        
        location = game["Location"]
        teamScore = game["TeamScore"]
        oppScore  = game["OpponentScore"]
            
        neutral = 0
        if location == 0:
            neutral = 1
        partition = 1
        
        if location == teamID or location == 0:
            homeTeam  = teamName
            awayTeam  = oppName
            homeScore = teamScore
            awayScore = oppScore
        elif location == oppID:
            homeTeam  = oppName
            awayTeam  = teamName
            homeScore = oppScore
            awayScore = teamScore
        else:
            raise ValueError("Not sure about location:",location)
                
        result    = int(homeScore)-int(awayScore)
        if result > 0:
            result = 1
            winTeam  = homeTeam
            lossTeam = awayTeam
            weight   = int(homeScore)-int(awayScore)
        else:
            result = 0
            winTeam  = awayTeam
            lossTeam = homeTeam
            weight   = int(awayScore)-int(homeScore)
            
        btdata.append([homeTeam,awayTeam,homeScore,awayScore])
        mvdata.append([date,awayTeam,homeTeam,neutral,homeScore,awayScore,partition,homeScore,awayScore])
        elodata.append([week,homeTeam,awayTeam,result])
        grdata.append([winTeam,lossTeam,weight])

    f = open(getNetworkDBDir()+"/"+yearID+".btdata.csv", "w")
    f.write("home.team,away.team,home.score,away.score\n")
    nGames = 0
    for game in btdata:
        nGames += 1
        game = [str(x) for x in game]
        f.write(",".join(game)+"\n")
    f.close()
    print "Wrote",nGames,"games to",f.name

    f = open(getNetworkDBDir()+"/"+yearID+".mvdata.csv", "w")
    f.write("Date,away,home,neutral.site,home.score,away.score,partition,home.response,away.response\n")
    nGames = 0
    for game in mvdata:
        nGames += 1
        game = [str(x) for x in game]
        f.write(",".join(game)+"\n")
    f.close()
    print "Wrote",nGames,"games to",f.name

    f = open(getNetworkDBDir()+"/"+yearID+".elodata.csv", "w")
    f.write("Week,HomeTeam,AwayTeam,Score\n")
    nGames = 0
    for game in elodata:
        nGames += 1
        game = [str(x) for x in game]
        f.write(",".join(game)+"\n")
    f.close()
    print "Wrote",nGames,"games to",f.name

    f = open(getNetworkDBDir()+"/"+yearID+".grdata.csv", "w")
    f.write("WinTeam,LossTeam,Weight\n")
    nGames = 0
    for game in grdata:
        nGames += 1
        game = [str(x) for x in game]
        f.write(",".join(game)+"\n")
    f.close()
    print "Wrote",nGames,"games to",f.name
    
        
        

def analyzeSeason(yearID, debug = False):
    savename   = setFile(getSchedulesDBDir(), yearID+".json")
    schedules  = get(savename, debug = True)
    
    savename   = setFile(getTeamsDBDir(), yearID+"-Data.p")
    teamsMap   = get(savename, debug = True)

    createNetworkMap(yearID, schedules, teamsMap, debug)
    createGameRankingData(yearID, schedules, teamsMap, debug)