# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:36:45 2015

@author: tgadfort
"""

import TeamConv as tc
import teamNum as tn
import getHTML as web
import os
import glob
import random


def getURL(basepath, url, htmlid, force):
#    result = web.checkURL(url)
#    if result == False:
#        print ' --->',url,' = ',result
#        return result


    if os.path.exists(basepath):
        savehtml=basepath+"/"+str(htmlid)+".html"
    else:
        print ' ---> No save path'
        print basepath
        print htmlid
        return False
    
    if os.path.exists(savehtml) and force == False:
        print ' ---> Save path exists, but force -> FALSE'
        return False
        
    result=web.getHTML(url, savehtml)
    if result:
        print ' --->',url,'  in  ',savehtml
    else:
        print " Did not download",url



def parseHistoricalSchedule(schedule):
    vals = schedule.split("recap?id=")
    games={}
    for val in vals:
        pos    = val.find("\">")
        gameid = val[:pos]
        try:
            games[gameid] = int(gameid)
        except:
            continue
        
    return games
    
    


def parseSchedule(base, schedule):
    vals = schedule.split("<li>")
    games={}
    for val in vals:
        if val.find("gameId=") != -1:
            idval="href=\"/college-football/game?gameId="
            pos1=val.find(idval)
            pos2=val.find("\">", pos1+1)
            gamehtml=val[pos1+6:pos2]
            gameid=gamehtml.split("=")[1]
            gamehtml = base + gamehtml
            if games.get(gameid) == None:
                games[gameid] = gamehtml
    return games
    
 
def getHistoricalSchedule(basepath, teamid, force):
    years=range(2002, 2015)
    for year in years:
        yearid = str(year)
        url="http://espn.go.com/college-football/team/schedule/_/id/"+teamid+"/year/"+yearid + "/"
        htmlid = teamid + "-" + yearid
        getURL(basepath, url, htmlid, force)

    
def getTeamURL(teamnum):
    ttypes={}
    ttypes["Team"] = "team"
    urls=[]
    for k,v in ttypes.iteritems():
        url="http://espn.go.com/college-football/"+v+"/_/id/"+str(teamnum)
        urls.append([k,url])
    return urls


def getGameURLs(gameid):
    gtypes={}
    gtypes["Plays"]    = "playbyplay"
    gtypes["Matchup"]  ="matchup"
    gtypes["BoxScore"] = "boxscore"
    urls=[]
    for k,v in gtypes.iteritems():
        url="http://scores.espn.go.com/college-football/"+v+"?gameId="+str(gameid)
        urls.append([k,url])
    return urls



def getTeam(teamnum, locbase, test=False, force=False):
    urls = getTeamURL(teamnum)
    for url in urls:
        basepath = locbase + "/" + url[0]
        getURL(basepath, url[1], teamnum, force)
    
    
def getGame(gameid, locbase, test=False, force=False):
    urls = getGameURLs(gameid)
    for url in urls:
        basepath = locbase + "/" + url[0]
        getURL(basepath, url[1], gameid, force)
        


def getTeamHistoricalGames(schedulebase, teamnum):
    teamhtmls = glob.glob(schedulebase + "/" + str(teamnum) + "-*")
    teamgames={}
    for teamhtml in teamhtmls:
        teamyear  = os.path.basename(teamhtml).split(".")[0]
        team,year = teamyear.split("-")

        #print team,year
        #print teamhtml

        fdata = open(teamhtml).readlines()
        fdata = [x.strip('\r\n') for x in fdata]
        fdata = [x.strip('\t') for x in fdata]
        for line in fdata:
            if line.find("<ul class=\"game-schedule\">") != -1:
                games = parseHistoricalSchedule(line)
                teamgames.update(games)
#                for k,v in games.iteritems():
#                    teamgames[k] = getGameURLs(k)
                    
    return teamgames
    

def getTeamGames(locbase, webbase, teamnum):
    teamhtml=locbase + "/" + str(teamnum) + ".html"
    if not os.path.exists(teamhtml):
        print "No team file:",teamhtml
        return False
    fdata = open(teamhtml).readlines()
    fdata = [x.strip('\r\n') for x in fdata]
    fdata = [x.strip('\t') for x in fdata]
    for line in fdata:
        if line.find("<section class=\"club-schedule\" data-module=\"schedule\"") != -1:
            games = parseSchedule(webbase, line)
            return games
    return None


def parseTeam(base, teamhtml, fbsteams):
    fdata = open(teamhtml).readlines()
    fdata = [x.strip('\r\n') for x in fdata]
    fdata = [x.strip('\t') for x in fdata]

    
    for line in fdata:
        if line.find("<meta property=\"og:title\" content=\"") != -1:
            pos1=line.find("content=")
            pos2=line.find("College Football")
            name=line[pos1+9:pos2].strip()
            vals=name.split()
            fbsteam=False
            test1=vals[0]
            test1=tc.TeamConv(test1)
            test2=" ".join(vals[:2])
            test2=tc.TeamConv(test2)
            test3=test2+" State"
            test3=tc.TeamConv(test3)
            if fbsteams.get(test1):
                fbsteam = True
                print test1,"is an FBS team"
            if fbsteams.get(test2):
                fbsteam = True
                print test2,"is an FBS team"
            if fbsteams.get(test3):
                fbsteam = True
                print test3,"is an FBS team"
            if not fbsteam:
                print "I don't think [",name,"] is an FBS team"
                return
                
        if line.find("<section class=\"club-schedule\" data-module=\"schedule\"") != -1:
            games = parseSchedule(base, line)
            for game in games:
                idval = game.split("=")[1]
                playbyplay = game.replace("game?", "playbyplay?")
                saveval="Games/Plays/"+idval+".html"
                if os.path.exists(saveval):
                    #print "Already have",saveval
                    continue
                gamehtml = playbyplay
                print gamehtml,'--->',saveval
                getHTML(gamehtml, saveval)
