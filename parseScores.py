# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:27:02 2015

@author: tgadfort
"""


import TeamConv as tc
import teamNum as tn
import getHTML as web
import os
import json


def parseHistoricalScores(scorepath, teampath, histjsonfile):
    
    historicaldata={}
    years=range(1869, 2020)
    for year in years:
        yearid=str(year)
        key = yearid
        
        teamfile  = teampath + "/" + yearid + ".html"
        scorefile = scorepath + "/" + yearid + ".html"

        if os.path.exists(teamfile) and os.path.exists(scorefile):
            teamdata = open(teamfile).readlines()
            teamdata = [x.strip('\r\n') for x in teamdata]

            scoredata = open(scorefile).readlines()
            scoredata = [x.strip('\r\n') for x in scoredata]
        else:
            continue
        

        yearscores=[]
        yearteams={}
        
        conference=None
        for team in teamdata[1:]:
            if str.isalpha(team[0]) == True:
                continue
            if str.isalpha(team[1]) == True:
                conference=team.strip()
                continue
            if str.isalpha(team[2]) == True:
                teamname=tc.TeamConv(team.strip())
                yearteams[teamname] = conference
        
        for score in scoredata:
            vals = score.split()
            
            date = None
            team1 = None
            team2 = None
            score1 = None
            score2 = None
            
            
            ## Date
            date = vals[0]
            vals = vals[1:]

            ## Team1
            team1=[]
            j = 0
            while j < len(vals):
                try:
                    score1 = int(vals[j])
                    team1  = " ".join(team1)
                    vals   = vals[j+1:]
                    break
                except:
                    team1.append(vals[j])
                j += 1

            ## Team2
            team2=[]
            j = 0
            while j < len(vals):
                try:
                    score2 = int(vals[j])
                    team2  = " ".join(team2)
                    vals   = vals[j+1:]
                    break
                except:
                    team2.append(vals[j])
                j += 1
                
            comment = None
            if len(vals) > 0:
                comment = " ".join(vals)

            if score2 == None:
                lastval = vals[-1]
                testscore = lastval[-4:]
                try:
                    testscore = int(testscore)                    
                    team2     = lastval[:-4]
                    score2    = testscore
                    vals      = []
                except:
                    testscore = lastval[-3:]
                if not score2:
                    try:
                        testscore = int(testscore)
                        team2     = lastval[:-3]
                        score2    = testscore
                        vals      = []
                    except:
                        testscore = lastval[-2:]
                if not score2:
                    try:
                        testscore = int(testscore)
                        team2     = lastval[:-2]
                        score2    = testscore
                        vals      = []
                    except:
                        testscore = lastval[-1:]
                                        
                    
            team1 = tc.TeamConv(team1)
            team2 = tc.TeamConv(team2)
            
            sval={}
            sval['date']    = date
            sval['team1']   = team1
            try:
                sval['conf1']   = yearteams[team1]
            except:
                yearteams[team1] = "DivII"
                sval['conf1']   = yearteams[team1]
            sval['score1']  = score1
            sval['team2']   = team2
            try:
                sval['conf2']   = yearteams[team2]
            except:
                yearteams[team2] = "DivII"
                sval['conf2']   = yearteams[team2]
            sval['score2']  = score2
            sval['comment'] = comment
            yearscores.append(sval)


        historicaldata[key] = {}
        historicaldata[key]['teams']  = yearteams
        historicaldata[key]['scores'] = yearscores
        print '\t',key
        
    print '\tWrote',len(historicaldata),"scores to",histjsonfile
    json.dump(historicaldata, open(histjsonfile, "w"))

        

def getHistoricalTeams(basepath, force):
    years=range(1869, 2014)
    for year in years:
        yearid=str(year)
        url="http://wilson.engr.wisc.edu/rsfc/history/howell/cf"+yearid+"tms.txt"
        result = web.checkURL(url)
        if not result:
            continue
        
        if os.path.exists(basepath):
            savehtml=basepath+"/"+yearid+".html"
        else:
            print ' ---> No save path',basepath,'\t',yearid
            return False
        
        if os.path.exists(savehtml) and force == False:
            print ' ---> Save path exists, but force -> FALSE'
            return False
        
        result=web.getHTML(url, savehtml)
        if result:
            print ' --->',url,'  in  ',savehtml
        else:
            print " Did not download",url



def getHistoricalScores(basepath, force):
    years=range(1869, 2014)
    for year in years:
        yearid=str(year)
        url="http://wilson.engr.wisc.edu/rsfc/history/howell/cf"+yearid+"gms.txt"
        result = web.checkURL(url)
        if not result:
            continue
        
        if os.path.exists(basepath):
            savehtml=basepath+"/"+yearid+".html"
        else:
            print ' ---> No save path',basepath,'\t',yearid
            return False
        
        if os.path.exists(savehtml) and force == False:
            print ' ---> Save path exists, but force -> FALSE'
            return False
        
        result=web.getHTML(url, savehtml)
        if result:
            print ' --->',url,'  in  ',savehtml
        else:
            print " Did not download",url



def getScores(basepath, savehtml, yearid, force):
    url = 'http://www.jhowell.net/cf/scores/Sked2015.htm'
    result = web.checkURL(url)
    if result == False:
        print ' --->',url,' = ',result
        return result

    if os.path.exists(savehtml) and force == False:
        print ' ---> Save path exists, but force -> FALSE'
        return False
        
    result=web.getHTML(url, savehtml)
    if result:
        print ' --->',url,'  in  ',savehtml
    else:
        print " Did not download",url
        
    return True


def parseScores(txt):
    fdata = open(txt).readlines()
    fdata = [x.strip('\r\n') for x in fdata]

    yeardata={}

    i=0
    while i < len(fdata):
        line = fdata[i]
        tdata=[]
        if line.find("<table") != -1:
            while line.find("</table>") == -1:
                tdata.append(line)
                i += 1
                line = fdata[i]

            teamdata = parseTable(tdata)
            yeardata[teamdata['name']] = {}
            yeardata[teamdata['name']]['conf'] = teamdata['conf']
            yeardata[teamdata['name']]['games'] = teamdata['games']
        i += 1
    return yeardata



def parseTable(table):
    table = [x.replace("</tr>", "") for x in table]
    table = [x.replace("</td>", "") for x in table]

    teamdata={}
    teamdata["games"] = []
    
    table = table[1:]
    name,conf = getName(table[0])
    teamdata["name"] = name
    teamdata["conf"] = conf

    table = table[1:]

    for line in table:
        gamedata = getGame(line)
        if gamedata:
            teamdata["games"].append(gamedata)

    return teamdata
    f()

    
    
def getName(line):
    pos = line.find("<p align=\"center\">")
    if pos == -1:
        print "Could not parse:",line
        f()
    name = line[pos+18:]
    
    pos = name.rfind("(")
    conf = name[pos:]
    conf = conf.replace("(", "")
    conf = conf.replace(")", "")
    name = name[:pos-1]
    return name,conf


def getGame(line):
    line = line.replace("<td align=\"right\">", ":")
    line = line.replace("<td>", ":")
    line = line.replace("<tr>", "")
    linevals = line.split(":")
    site = None
    if len(linevals) == 8:
        try:
            dummy,date,day,home,opp,res,score,against = linevals
        except:
            print "SPLIT ERROR:",line
            f()
    elif len(linevals) == 9:
        try:
            dummy,date,day,home,opp,res,score,against,site = linevals
        except:
            print "SPLIT ERROR:",line
            f()
    elif len(linevals) == 10:
        try:
            dummy,date,day,home,opp,res,score,against,site,comment = linevals
        except:
            print "SPLIT ERROR:",line
            f()
    
    opp = opp.replace("*", "")
    if home == "vs.":
        home = 1
    elif home == "@":
        home = -1
    else:
        print "ERROR with Home:",home
        f()
    if site != None:
        home = 0

    if len(res) == 0:
        return None

    try:
        game={}
        game['date'] = date
        game['day'] = day
        game['home'] = home
        game['opponent'] = opp
        game['result'] = res
        game['score'] = int(score)
        game['against'] = int(against)
    except:
        print "DICT ERROR\t",date,day,home,opp,res,score,against
        f()
        

    return game
    
    


##########################################
#
# This is the output line to the csv file
#
##########################################
def writeLine(outfile, Date, Team1, Team2, Score1, Score2, Winner):
    lout=[]
    lout.append(Date)
    lout.append(Team1)
    lout.append(Team2)
    lout.append(Score1)
    lout.append(Score2)
    lout.append(Winner)
    lout=[str(x) for x in lout]
    outfile.write(",".join(lout))
    outfile.write("\n")
    


def writeFile(fname, yeardata):
    f=open(fname, "w")
    writeLine(f, "Date", "Team1", "Team2", "Score1", "Score2", "Winner")
    nline=0
    teams=sorted(yeardata.keys())
    for team in teams:
        games = yeardata[team]["games"]
        for game in games:
            if game['result'] == 'W':
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], team)
            elif game['result'] == 'L':
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], game['opponent'])
            else:
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], team)
            nline += 1
    print "\tWrote",nline,"lines to",fname
    f.close()