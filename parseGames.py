# This Python file uses the following encoding: utf-8
import argparse

import os, sys
import glob
import requests
from collections import Counter
import json
import datetime

import parsePlayByPlay
import parseScoringSummary
import parseMatchup
import parseBoxScore
import parseTeam
import parseScores
import parseSFref

import TeamConv as tc
import teamNum as tn

reload(sys)
sys.setdefaultencoding('utf8')


def f(): raise Exception("Found exit()")
    
def Fix(name, size):
    newname=name
    while len(newname) < size:
        newname += " "
    return newname



def TestTime(time1, time2):
    #print time1 - time2
    oneday=datetime.timedelta(days=1)
    if time1 == time2 or time1 == time2 + oneday or time1 == time2 - oneday:
        return True
    return False

def getdTimeYear(date, year):
    m,d = date.split('/')
    if int(m) < 10:
        dateyear="0"+m
    else:
        dateyear=m
    if int(d) < 10:
        dateyear+="/0"+d
    else:
        dateyear="/"+d
    dateyear = date + "/"+str(year)
    try:
        tformat = "%m/%d/%Y"
        gametime   = datetime.datetime.strptime(dateyear, tformat)
    except:
        print "Could not convert date:",dateyear
        f()
    return gametime

def getdTime(date):
    try:
        tformat = "%B %d, %Y"
        gametime   = datetime.datetime.strptime(date, tformat)
    except:
        print "Could not convert date:",date
        f()
    return gametime


    




##############################################################################
#
#
# parseTitle()
#
#
##############################################################################
def parseTitle(game, debug):
    print game
    vals=game.split(" - ")
    if len(vals) != 4:
        print "Can not parse title:",game
        f()

    try:
        team1,team2=vals[0].split(" vs. ")
        date=vals[2]
    except:
        print "Problem with parsing title:",vals
        f()

    return team1,team2,date






##############################################################################
#
#
# parseLogo()
#
#
##############################################################################
def parseLogo(logo, debug):
    team1=None
    team2=None
    teamnum=-1
    if debug: print "=============== logo ==============="
    for div in logo.split("<div"):
        if debug: print "\t->  ",div
        
        if teamnum == -1:
            teamnum,logoaddr=tn.getTeamNum(div)
        if teamnum != -1:
            if debug: print '--->',logoaddr,'<---'
        
        teamname="class=\"team-name\""
        if div.find(teamname) != -1:
            pos1=div.find("<span class=\"long-name\">")
            pos2=div.find("</span>", pos1+1)
            team=div[pos1+24:pos2]
            if debug: print '---> Team Long:  ',team,'<---'
            
            abrvtxt="<span class=\"abbrev\" title=\""+team+"\">"
            pos1=div.find(abrvtxt)
            pos2=div.find("</span>", pos1+1)
            abrv=div[pos1+len(abrvtxt):pos2]
            if debug: print '---> Team Short: ',abrv,'<---'
            

            if team1 == None:
                team1=[team, teamnum, logoaddr, abrv]
            else:
                team2=[team, teamnum, logoaddr, abrv]
            teamnum=-1

    if debug: print team1
    if debug: print team2

    if team1 == None or team2 == None:
        print "Could not find teams:",team1,team2
        f()

    return team1, team2
    f()






##############################################################################
#
#
# compareGames()
#
#
##############################################################################
def compareGames(fbsgames, fbsscores, teamnums):
    ks=fbsscores.keys()
    for k in ks:
        v = fbsscores[k]
        team1=k
        print "=====",Fix(k,25),"====="


        test=False
        if test:
            vals=["Buffalo"]
            for val in vals:
                for k2,v2 in fbsgames.iteritems():                
                    teams=v2.keys()
                    for team in teams:
                        if team.find(val) != -1:
                            print k2," vs ".join(teams)
            f()
                        #exit()

        testgames={}
        for k2,v2 in fbsgames.iteritems():                
            teams=v2.keys()
            for team in teams:
                if team1 == tc.TeamConv(team):
                    testgames[k2]=v2
                    break


        ngames = len(testgames)
        games=v['games']
        if ngames < 1:
            print ""
            print ""
            print "=====",k,"=====",
            print "  ---> FBS Games:",ngames
            f()
        

        for i in range(len(games)):
            game=games[i]
            fbsscore = game

            dtime = getdTimeYear(game['date'], 2015)
            team2 = game['opponent']

            gamekey = None
            fbsgame = None
            for key,v2 in testgames.iteritems():
                side = v2.keys()[0]
                dtime2 = getdTime(v2[side]['date'])
                if TestTime(dtime, dtime2):
                    gamekey = key
                    if fbsgames.get(gamekey):
                        fbsgame = fbsgames[gamekey]
                    else:
                        print "Error in key!",gamekey
                        f()
                    break
                
            if gamekey == None or fbsgame == None:
                print "  --->",team1,'vs.',team2,' \t on',game['date'],'\t',
                print "Could not find fbs game key."
                for key,v2 in testgames.iteritems():
                    sides = v2.keys()
                    dtime2 = getdTime(v2[sides[0]]['date'])
                    print key,'\t',sides[0],sides[1],dtime2
                f()

            fbsscores[k]['games'][i]['teamdata'] = fbsgame
            print '\t',Fix(game['date'], 5),'\t',Fix(team2,25),'\t',gamekey

    return fbsscores
    


def testStats(fullgames):
    for k,v in fullgames.iteritems():
        print ''        
        print "=============================================================="
        team=k
        games=v['games']
        for game in games:
            date=game['date']
            opp = game['opponent']
            score=game['score']
            oppscore=game['against']
            print '\t',date,'\t',score,'\t',oppscore,'\t --> ',team,' vs.',opp,
            details=game['play-by-play']
            try:
                teamdetails=details[team]
                oppdetails=details[opp]
            except:
                print "Error with key in fullgames{} in testStats()"
                print opp,details
                f()

            if teamdetails['summary']['score'] != score or oppdetails['summary']['score'] != oppscore:
                print "ERROR"
                print '\t\t',teamdetails['summary']['score'],'\t',oppdetails['summary']['score']
                print teamdetails
                print oppdetails
                f()
            else:
                print ""
        print ''        
        print "=============================================================="
        
    f()



def parseGame(gameid, gamehtml, fbsteams, debug, checkformissing):
    fdata = open(gamehtml).readlines()
    fdata = [x.strip('\r\n') for x in fdata]
    fdata = [x.strip('\t') for x in fdata]
    
    matchuphtml=gamehtml.replace("Plays", "Matchup")
    if matchuphtml == gamehtml:
        print "Problem parsing matchup html",gamehtml
        f()
    mdata=[]
    if os.path.exists(matchuphtml):
        mdata = open(matchuphtml).readlines()
        mdata = [x.strip('\r\n') for x in mdata]
        mdata = [x.strip('\t') for x in mdata]
    else:
        return "NoScore", None
    
    boxscorehtml=matchuphtml.replace("Matchup", "BoxScore")
    if boxscorehtml == matchuphtml:
        print "Problem parsing box score html",matchuphtml
        f()
    bdata=[]
    if os.path.exists(boxscorehtml):
        bdata = open(boxscorehtml).readlines()
        bdata = [x.strip('\r\n') for x in bdata]
        bdata = [x.strip('\t') for x in bdata]
    else:
        return "NoScore", None
    i=0
    
    gdata={}
    gdata["title"] = None
    gdata["logo"] = None
    gdata["plays"] = []
    while i < len(fdata):
        line=fdata[i]
        
        ## Game title
        gametitle="<meta name=\"title\" content=\""
        if line.find(gametitle) != -1 and gdata["title"] == None:
            gdata["title"] = line[len(gametitle):-3]

            

        ## Team logo
        logo="<img class=\"team-logo\""
        if line.find(logo) != -1 and gdata["logo"] == None:
            gdata["logo"] = line



        ## Game play-by-play
        pbp="<div id=\"gamepackage-play-by-play\" data-module=\"playbyplay\">"
        if line.find(pbp) != -1:
            while line.find("<div id=\"gamepackage-scoring-wrap\"") == -1:
                gdata["plays"].append(line)
                i += 1
                try:
                    line=fdata[i]
                except:
                    break



        ## Scoring summary
        scoresum="<div class=\"scoring-summary\">"
        if line.find(scoresum) != -1:
            gdata["scores"] = line

        i += 1

    if checkformissing:
        if gdata.get('scores') == None:
            return "NoScore",None
        else:            
            return "Good",None


    team1A,team2A,date=parseTitle(gdata["title"], debug)    
    if fbsteams.get(tc.TeamConv(team1A)) == None and fbsteams.get(tc.TeamConv(team2A)) == None:
        if debug: print "No FBS team here. Moving on."
        return "NoFBSTeam",None
    
    #print '--->',date,'<---'
    gametime = getdTime(date)
    if gametime > datetime.datetime.today():
        if debug: print "Game has not happened yet"
        return "NotPlayedYet",None


    team1Data,team2Data=parseLogo(gdata["logo"], debug)
    if team1Data[0] != team1A or team2Data[0] != team2A:
        print "Problem with teams"
        print team1Data[0],'<-->',team1A
        print team2Data[0],'<-->',team2A
        f()
        
    #print "---> Plays Info",len(gdata["plays"]),"<---"
    drives = parsePlayByPlay.parsePlayByPlay(gameid, gdata["plays"], team1Data, team2Data, debug)

    scores=[]
    if gdata.get('scores'):
        scores=parseScoringSummary.parseScoringSummary(gameid, gdata['scores'], team1Data, team2Data, debug)
    else:
        scores=None
    
    ##  Check for matchup information
    matchup=parseMatchup.parseMatchup(mdata, team1Data, team2Data, debug)
    #print matchup
    

    ##  Check for boxscore information
    boxscore=parseBoxScore.parseBoxScore(bdata, team1Data, team2Data, debug)
    #print boxscore

    gamedetails = {}
    team1Data[0] = tc.TeamConv(team1Data[0])
    team2Data[0] = tc.TeamConv(team2Data[0])
    gamedetails[team1Data[0]] = {}
    gamedetails[team2Data[0]] = {}
    print '\t'," vs. ".join(gamedetails.keys())

    gamedetails[team1Data[0]]['logo'] = team1Data[1:]
    gamedetails[team1Data[0]]["date"] = date
    gamedetails[team2Data[0]]['logo'] = team2Data[1:]
    gamedetails[team2Data[0]]["date"] = date
    
    gamedetails[team1Data[0]]['drives'] = None
    gamedetails[team1Data[0]]['scores'] = None
    gamedetails[team1Data[0]]["teamstats"] = None
    gamedetails[team1Data[0]]["indivstats"] = None
    
    gamedetails[team2Data[0]]['drives'] = None
    gamedetails[team2Data[0]]['scores'] = None
    gamedetails[team2Data[0]]["teamstats"] = None
    gamedetails[team2Data[0]]["indivstats"] = None
    
    
    if matchup != None:       
        if matchup.get(team1Data[0]) == None:
            print "Could not find",team1Data[0],"in matchup",matchup.keys()
            f()
        if matchup.get(team2Data[0]) == None:
            print "Could not find",team2Data[0],"in matchup",matchup.keys()
            f()
        gamedetails[team1Data[0]]["teamstats"] = matchup[team1Data[0]]
        gamedetails[team2Data[0]]["teamstats"] = matchup[team2Data[0]]
        
    if boxscore != None:
        if boxscore.get(team1Data[0]) == None:
            print "Could not find",team1Data[0],"in matchup",boxscore.keys()
            f()
        if boxscore.get(team2Data[0]) == None:
            print "Could not find",team2Data[0],"in matchup",boxscore.keys()
            f()
        gamedetails[team1Data[0]]["indivstats"] = boxscore[team1Data[0]]
        gamedetails[team2Data[0]]["indivstats"] = boxscore[team2Data[0]]

    if scores:
        if scores.get(team1Data[0]) == None:
            print "Could not find",team1Data[0],"in score",scores.keys()
            f()
        if scores.get(team2Data[0]) == None:
            print "Could not find",team2Data[0],"in score",scores.keys()
            f()
        gamedetails[team1Data[0]]['scores'] = scores[team1Data[0]]
        gamedetails[team2Data[0]]['scores'] = scores[team2Data[0]]
    
    if drives:
        if drives.get(team1Data[0]) == None:
            print "Could not find",team1Data[0],"in drives",drives.keys()
            f()
        if drives.get(team2Data[0]) == None:
            print "Could not find",team2Data[0],"in drives",drives.keys()
            f()
        gamedetails[team1Data[0]]['drives'] = drives[team1Data[0]]
        gamedetails[team2Data[0]]['drives'] = drives[team2Data[0]]
        


    return "Good",gamedetails



############################################################
##
##  Main()
##
############################################################
def main(args):
    yearid="2015"
    webbase="http://scores.espn.go.com"
    
    basepath     = os.path.abspath("/Users/tgadfort/Dropbox/Football")
    gamebase     = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games")
    teambase     = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games/Teams")
    schedulebase = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games/Teams/Schedule")
    spteampath   = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games/Teams/SFref")
    spyearpath   = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games/Teams/SFref/Historical")
    scorebase    = os.path.abspath("/Users/tgadfort/Dropbox/Football/Scores")
    gamesdir     = os.path.relpath("Games/Plays")
    datadir      = os.path.abspath("/Users/tgadfort/Dropbox/Football/Data")
    sprefdir     = os.path.abspath("/Users/tgadfort/Dropbox/Football/SPref")


    historicalscorebase = scorebase
    historicalteambase  = os.path.abspath("/Users/tgadfort/Dropbox/Football/Games/Teams/Historical")
    historicaljsonfile  = os.path.abspath(datadir + "/" + "HistoricalTeamScores.json")
    
    
    fbsgamesfile   = os.path.abspath(datadir + "/" + yearid+"Data.json")
    teamdbfile     = os.path.abspath(datadir + "/" + "TeamDB.json")
    

    scorehtmlfile  = os.path.abspath(scorebase + "/" + yearid + ".html")
    scorejsonfile  = os.path.abspath(datadir + "/" + yearid + "Scores.json")
    scorecsvfile   = os.path.abspath(datadir + "/" + yearid + "Scores.csv")
    

    fullgamefile   = os.path.abspath(datadir + "/" + "Merged" + yearid + ".json")
    teamdb=json.load(open(teamdbfile))
    fbsteams=teamdb['names']
    

    sprefhtml             = os.path.abspath(sprefdir + "/" + "index.html")
    sprefteamsjsonfile    = os.path.abspath(datadir + "/" + "SPrefTeams.json")
    sprefgamelogsjsonfile = os.path.abspath(datadir + "/" + "SPrefGameLogs.json")
    sprefteamyearjsonfile = os.path.abspath(datadir + "/" + "SPrefTeamYear.json")


    if args.spref:
        parseSFref.getSFref(sprefhtml, args.force)
        parseSFref.parseSFref(sprefhtml, sprefteamsjsonfile)
        parseSFref.getSFrefTeams(spteampath, sprefteamsjsonfile, args.force)
        parseSFref.parseSFrefTeams(spteampath, sprefteamsjsonfile, args.force)
        parseSFref.getSFrefTeamYears(spyearpath, sprefteamsjsonfile, args.force)
        parseSFref.parseSFrefTeamYears(spyearpath, sprefteamyearjsonfile, args.force)
        parseSFref.parseSFrefTeamGameLog(spyearpath, sprefgamelogsjsonfile, args.force)
        return

    #################################
    # If we need to get historical scores
    #################################
    if args.gethistoricalscores:
#        parseScores.getHistoricalScores(historicalscorebase, args.force)
#        parseScores.getHistoricalTeams(historicalteambase, args.force)
        parseScores.parseHistoricalScores(historicalscorebase, 
                                          historicalteambase,
                                          historicaljsonfile)
        return

    #################################
    # If we need to merge scores and data
    #################################
    if args.merge:
        fbsgames  = json.load(open(fbsgamesfile))
        fbsscores = json.load(open(scorejsonfile))
        fullgames = compareGames(fbsgames, fbsscores, teamdb)
        print "Writing",len(fullgames),"full games to",fullgamefile
        json.dump(fullgames, open(fullgamefile, "w"))
        return



    #################################
    # If we need to download scores
    #################################
    if args.getscores:
        scoreid = yearid
        parseScores.getScores(scorebase, scorehtmlfile, scoreid, args.force)
        scores = parseScores.parseScores(scorehtmlfile)
        if scores:
            parseScores.writeFile(scorecsvfile, scores)
            json.dump(scores, open(scorejsonfile, "w"))
            print "\tWrote",len(scores),"lines to",scorejsonfile
        return



    #################################
    # If we need to redownload teams
    #################################
    if args.getgame:
        gameid = args.getgame[0]
        parseTeam.getGame(gameid, gamebase, test=False, force=True)
        return



    #################################
    # If we need to redownload teams
    #################################
    if args.getteams:
        for k in teamdb['nums'].keys():
            result = parseTeam.getTeam(k, teambase, test=False, force=args.force)
            parseTeam.getHistoricalSchedule(schedulebase, k, args.force)
        return



    #################################
    # If we need to redownload games
    #################################
    if args.getgames:
        for k in teamdb['nums'].keys():
            result = parseTeam.getTeamHistoricalGames(schedulebase, k)
            for gameid, gamenum in result.iteritems():
                gameresult = parseTeam.getGame(gameid, gamebase, test=False, force=args.force)
            continue
            
            result = parseTeam.getTeamGames(gamebase, webbase, k)
            for gameid, gamehtml in result.iteritems():
                result = parseTeam.getGame(gameid, gamehtml, gamebase, test=False, force=args.force)

        return



    debug=False
    games=glob.glob(gamesdir+"/*.html")
    gamedb={}
    fbsgames={}
    missing=[]
    for g in range(len(games)):
        print "==================="
        print "Game",g+1,'/',len(games),'\t',
        game=games[g]
        key = os.path.basename(game)
        key = key.split(".")[0]
        print key,'  ',
        gamestatus,gameresults = parseGame(key, game, fbsteams, debug, args.missing)
        if args.missing:
            if gamestatus != "Good":
                missing.append([gamestatus, key])
            continue
        if gamestatus != "Good":
            print "\t-->",gamestatus
            missing.append([gamestatus, key])
            continue
        if gameresults == None:
            print "\t-->",gamestatus
            continue
    
        #print gameresults
        if gamedb.get(key):
            print "Already parsed this game [",key,"]!"
            continue
        fbsgames[key] = gameresults
        #print gameresults
        teams=gameresults.keys()
        if fbsteams.get(tc.TeamConv(teams[0])) and fbsteams.get(tc.TeamConv(teams[1])):
            gamedb[key] = gameresults
        else:   
            print "Not keeping game for later downloads by gameDB because one team is not FBS"
            
    print "Done parsing",len(games),"games."
    print "FBS Games:",len(fbsgames)
    print "Writing",len(fbsgames),"games to",fbsgamesfile
    json.dump(fbsgames, open(fbsgamesfile, "w"))



    

    #################################
    # If we need to get missing games
    #################################
    print '----- Missing -----'
    for game in missing:        
        print '\t--->',game
    print '-------------------'
    
    if args.missing:
        for game in missing:
            gamestatus = game[0]
            gameid = game[1]
            if gamestatus == "NoScore":
                result = parseTeam.getGame(gameid, gamebase, test=False, force=args.force)
        return
    
    
 

##################################################################
##
## main
##
##################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('-get-games', dest='getgames', nargs=1, help='Base directory name.')
    parser.add_argument('-spref', action="store_true", dest='spref', help='Get SFrefence data.')
    parser.add_argument('-merge', action="store_true", dest='merge', help='Merge scores and game data.')
    parser.add_argument('-get-game', nargs=1, dest='getgame', help='Get missing games.')
    parser.add_argument('-get-games', action="store_true", dest='getgames', default=False, help='Get missing games.')
    parser.add_argument('-get-teams', action="store_true", dest='getteams', default=False, help='Get missing games.')
    parser.add_argument('-missing', action="store_true", dest='missing', default=False, help='Look for missing games.')
    parser.add_argument('-force', action="store_true", dest='force', default=False, help='Force downloads.')
    parser.add_argument('-get-scores', action="store_true", dest='getscores', default=False, help='Get only scores.')
    parser.add_argument('-get-historical-scores', action="store_true", dest='gethistoricalscores', default=False, help='Get historical scores.')
    args = parser.parse_args()

    main(args)
    