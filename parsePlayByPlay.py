# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 10:53:01 2015

@author: tgadfort
"""

from collections import Counter
import TeamConv as tc
import teamNum as tn


def Fix(name, size):
    newname=name
    while len(newname) < size:
        newname += " "
    return newname
    
def driveScore(result):
    res = result.title()
    if len(result) == 0:
        return 0
    if res == "Safety":
        return -2
    if res == "End Of Game Touchdown":
        return 6
    if res == "Touchdown" or res == "Touchdown Touchdown":
        return 7
    if res == "Fumble Touchdown" or res == "Fumble Return Touchdown" or res == "Punt Touchdown" or res == "Punt Return Touchdown" or res == "End Of Half Touchdown" or res == "Downs Touchdown":
        return -7
    if res == "Interception Touchdown":
        return -7
    if res == "Missed Fg Touchdown":
        return -7
    if res == "Field Goal":
        return 3
    noPoints=["Kickoff", "Interception", "Punt", "Missed Fg", "Missed Fg Touchdown", "Downs", "End Of Game", "Fumble", "End Of Half", "Possession (For Ot Drives)"]
    for nop in noPoints:
        #print res,nop
        if res == nop:
            return 0
    print '-> ['+result.title()+']'
    if any(word in noPoints for word in res):
        print "Something is here"
    f()
    return 0

def augmentScore(drives, d, team, augscore):
    drives[d]['runningscore'][team][1] += augscore
    return drives


def driveFixes(gameid, drives, teams):
    if gameid == "400756912": # Miami vs FAU
        print "Fixing drives for this game"
        drives[6]['team'] = teams['MIA']
        drives[6]['result'] = "Punt"
        print "\tDrive6 -> Punt"
        drives[7]['team'] = teams['FAU']
        drives[7]['result'] = "Fumble"        
        print "\tDrive7 -> Fumble"
        drives[8]['team'] = teams['MIA']
    if gameid == "400603869": # Texas A&M vs Ball St
        drives[20]['team'] = teams['BALL']
    if gameid == "400603936": # Texas A&M vs Ball St
        drives[9]['team'] = teams['TA&M']
    if gameid == "400756952":
        augmentScore(drives, 8, 1, 3)
    if gameid == "400787442":
#        augmentScore(drives, 2, 0, 3)
        augmentScore(drives, 2, 1, 7)
    if gameid == "400763533": # Iowa vs Wis
        drives[9]['team'] = teams['IOWA']
        drives[15]['team'] = teams['WIS']
    if gameid == "400763552": # Iowa vs MD
        drives[19]['team'] = teams['MD']
        drives[20]['team'] = teams['MD']
    if gameid == "400787296": # Iowa vs MD
        drives[9]['team'] = teams['SDSU']
    if gameid == "400763589":
        augmentScore(drives, 26, 0, 2)
    if gameid == "400763590":
        drives.pop(15)
    if gameid == "400763645":
        drives[30]['team'] = teams['MTSU']
        drives[30]['score'] = 7
        drives[32]['runningscore'] = drives[31]['runningscore']
        drives[32]['team'] = teams['MTSU']
        drives[32]['result'] = "Field Goal"
        drives[32]['score'] = 3
        drives[31] = drives[34]
        drives[31]['result'] = "Touchdown"
        drives[31]['team'] = teams['MRSH']
        drives[31]['score'] = 7
        drives[33]['runningscore'] = drives[32]['runningscore']
        drives[33]['result'] = "Missed Field Goal"
        drives[33]['team'] = teams['MRSH']
        drives[33]['score'] = 0
        drives.pop(34)
    return drives


    if gameid == "400757042":
        drives[30]['runningscore'][0][1] += 2
    if gameid == "400757061":
        drives[10]['runningscore'][0][1] += 7
        
    if gameid == "400756952":
        drives[8]['runningscore'][1][1] += 3
        drives[14]['runningscore'][0][1] += 7
        
    if gameid == "400756951":
        print "Fixing drives for this game"
        drives[19]['runningscore'][1][1] += 2
        print "\tDrive8 -> MIA ball"
    if gameid == "400756961":
        drives[21]['runningscore'][1][1] += 8
        
    if gameid == "400757064": augmentScore(drives, 7, 1, 7)
#    if gameid == "400763457": augmentScore(drives, 25, 0, 6)
#    if gameid == "400763470": augmentScore(drives, 15, 0, 7)
#    if gameid == "400763470": augmentScore(drives, 16, 1, 7)
#    if gameid == "400763472": augmentScore(drives, 19, 0, 6)
    return drives

def analyzeDriveSummary(gameid, drives, awayteam, hometeam):
    teams={}
    #print awayteam
    #print hometeam
    teams[int(awayteam[0])] = awayteam[1]
    teams[awayteam[1]] = int(awayteam[0])
    teams[int(hometeam[0])] = hometeam[1]
    teams[hometeam[1]] = int(hometeam[0])

    ## Some are just totally messed up and require hand coding:
    #print "Game ID -->",gameid
    drives=driveFixes(gameid, drives, teams)
    
    realDebug=False
    if realDebug:
        print '\t',Fix("Driving",10),'\t','# Running Score','\t\t\tResult'
        for i in range(len(drives)-1):
            drive=drives[i]
            drivingteam=teams[drive['team']]
        
            print i,'\t',Fix(drivingteam,10),'\t',drive['score'], drive['runningscore'],'\t',drive['summary'],'\t',drive['result']

    ## Check for an extra entry due to Punt Return
    extras=[]


    ## In case we need to remove a drive    
    for i in range(len(drives)-1):
        result=drives[i]['result']
        ryards=drives[i]['summary'][1]
        rscore=drives[i]['score']        
        rtime =60*drives[i]['summary'][2]+drives[i]['summary'][3]
        nextresult=drives[i+1]['result']
        nextryards=drives[i+1]['summary'][1]
        nextrscore=drives[i+1]['score']
        nextrtime =60*drives[i+1]['summary'][2]+drives[i+1]['summary'][3]
        
        if result.find("Touchdown") -1 and nextresult.find("Touchdown") != -1:
            if nextryards == 0 and rscore < 0 and nextrscore > 0 and nextrtime == 0:
                extras.append(i+1)
                print "====================================================="
                print "====================================================="
                print drives[i]
                print drives[i+1]," <--- Removing this guy."
                print "====================================================="
                print "====================================================="
    for extra in extras:
        drives.pop(extra)
        

    debugScore=False
    if debugScore: print '#\tPrev\tCurr\tDiff\tDrive\tNext\tDiffNext'
    for i in range(len(drives)-1):
        ## Offense score
        drivingteam=teams[drives[i]['team']]
        dscore=0
        teamid=-1
        
        if i == 0:
            prevscores=[ 0,0 ]
        else:
            prevscores=[ drives[i-1]['runningscore'][0][1], drives[i-1]['runningscore'][1][1] ]
        currscores=[ drives[i]['runningscore'][0][1], drives[i]['runningscore'][1][1] ]
        nextscores=[ drives[i+1]['runningscore'][0][1], drives[i+1]['runningscore'][1][1] ]
        diffscores=[0,0]
        diffscores[0]=currscores[0] - prevscores[0]
        diffscores[1]=currscores[1] - prevscores[1]
        diffnextscores=[0,0]
        diffnextscores[0]=nextscores[0] - currscores[0]
        diffnextscores[1]=nextscores[1] - currscores[1]
        
        if drivingteam == awayteam[1]:
            drivescore=[ drives[i]['score'],0 ]
        if drivingteam == hometeam[1]:
            drivescore=[ 0, drives[i]['score'] ]
        if debugScore: print i,'\t',prevscores,'\t',currscores,'\t',diffscores,'\t',drivescore,'\t',nextscores,'\t',diffnextscores,'\t',

        
        ## Away team scored
        if drivescore[0] > 0:
            teamid=0
            if diffscores[teamid] == 0:
                if debugScore: print "Away Score, but no update. Setting to",drives[i+1]['runningscore'][teamid][1],'from',drives[i]['runningscore'][teamid][1],
                drives[i]['runningscore'][teamid][1] = drives[i+1]['runningscore'][teamid][1]

        ## Home team gave up defensive points to away team
        if drivescore[1] < 0:
            teamid=0
            if diffscores[teamid] == 0:
                if debugScore: print "Away Score on defense, but no update. Setting to",drives[i+1]['runningscore'][teamid][1],"from",drives[i]['runningscore'][teamid][1]
                drives[i]['runningscore'][teamid][1] = drives[i+1]['runningscore'][teamid][1]

                
        ## Home team scored
        if drivescore[1] > 0:
            teamid=1
            if diffscores[teamid] == 0:
                if debugScore: print "Home Score, but no update. Setting to",drives[i+1]['runningscore'][teamid][1],'from',drives[i]['runningscore'][teamid][1],
                drives[i]['runningscore'][teamid][1] = drives[i+1]['runningscore'][teamid][1]

        ## Away team gave up defensive points to home team
        if drivescore[0] < 0:
            teamid=1
            if diffscores[teamid] == 0:
                if debugScore: print "Home Score on defense, but no update. Setting to",drives[i+1]['runningscore'][teamid][1],'from',drives[i]['runningscore'][teamid][1],
                drives[i]['runningscore'][teamid][1] = drives[i+1]['runningscore'][teamid][1]

        ## Strange thing that happens in OT
        if diffnextscores[0] != 0 and diffnextscores[1] != 0:
            if i == len(drives) - 2:
                if debugScore: print "Two scoring changes. Setting to",drives[i]['runningscore'],'from',drives[i+1]['runningscore']
                drives[i+1]['runningscore'] = drives[i]['runningscore']
        if debugScore: print ''


    #for i in range(len(drives)):
    #    print i,'\t',drives[i]['runningscore']

    ## Check for higher scores incorrectly given
    for t in range(2):
        i=0
        for i in range(len(drives)-1):
            currscore = drives[i]['runningscore'][t][1]
            #print i,"\tCurrent Score:",currscore
            j = i+1
            fix=False
            while j < len(drives) - 1:
                nextscore = drives[j]['runningscore'][t][1]
                if nextscore < currscore:
                    #print '\t',j,'\tNext Score:',nextscore
                    k=j-1
                    #print "\tFixing [",i,k,"] entries."
                    fix=True
                    break
                j += 1
            if fix:
                j=i
                while j <= k:
                    print '  Fixing Score on drive',j,'\t',
                    print '  ',drives[j]['runningscore'][t][1],' -> ',nextscore
                    drives[j]['runningscore'][t][1] = nextscore
                    j += 1
                
                
            #print i,'\t',drives[i]['runningscore'][t]

    nerr=0
    scores={}
    scores[awayteam[1]]=0
    scores[hometeam[1]]=0
    showResult=False
    
    if showResult: print i,'\t',Fix("Driving",10),'\t','# Running Score','\t\t','Team Score','\tResult'
    for i in range(len(drives)):
        drive=drives[i]
        drivingteam=teams[drive['team']]
        scoreval=drive['score']
        if drivingteam == awayteam[1]:
            newscore = drive['runningscore'][0][1]
            oteamscore = drive['runningscore'][1][1]
            oteam = hometeam[1]
        else:
            newscore = drive['runningscore'][1][1]
            oteamscore = drive['runningscore'][0][1]
            oteam = awayteam[1]
           

        ## Special for negative plays
        if scoreval < 0:
            if showResult: print "Turnover ->",drivingteam,' -> '
            if drivingteam == awayteam[1]:
                if showResult: print "\t home team scores",drive['runningscore'][1][1],'  ',scores[hometeam[1]]
                if drive['runningscore'][1][1] != scores[hometeam[1]]:
                    drivingteam = hometeam[1]
                newscore = drive['runningscore'][1][1]
                #oteamscore = drive['runningscore'][0][1]
                #oteam = awayteam[1]
            else:
                if showResult: print "\t home team scores",drive['runningscore'][0][1],'  ',scores[awayteam[1]]
                if drive['runningscore'][0][1] != scores[awayteam[1]]:
                    drivingteam = awayteam[1]
                newscore = drive['runningscore'][0][1]
                #oteamscore = drive['runningscore'][1][1]
                #oteam = hometeam[1]
            if showResult: print drivingteam,"Should be the one that got points."
            scoreval *= -1
            

        err=False
        diff=0
        if newscore != scores[drivingteam] + scoreval:
            err=True
            diff = scores[drivingteam] + scoreval - newscore
            result=drive['result']
            comment = ""
            ## Missed extra point or two-point conversion
            if diff < -10 and result == "Downs":
                scoreval = 0
                comment = "End of Game"
            if scoreval == 7 and diff == 1:
                scoreval = 6
                comment = "Missed Extra Point"
            if scoreval == 7 and diff == -1:
                scoreval = 8
                comment = "Two Point Conversion"
            if scoreval == 0 and diff == -3 and result == "End of Half":
                scoreval = 3
                comment = "Field Goal"
            if scoreval == 0 and diff == -3 and result == "Fumble":
                scoreval = 3
                comment = "Field Goal"
            if scoreval == 0 and diff == -3 and result == "Downs":
                scoreval = 3
                comment = "Field Goal"
            if scoreval == 0 and diff == -7 and result == "End of Half":
                scoreval = 7
                comment = "Touchdown"
            if scoreval == 0 and diff == -7 and result == "End of Game":
                scoreval = 7
                comment = "Touchdown"

            ## Check if we need to also fix the other teams score
            if scores[oteam] != oteamscore:
                oteamdiff = oteamscore - scores[oteam]
                if oteamdiff == 2:
                    comment += " Defensive PAT"
                    scores[oteam] = oteamscore
                else:
                    print "Something happened to",oteam,"so that they got",oteamdiff,"points."
                    
        
            ## Check if this fixes things
            if newscore == scores[drivingteam] + scoreval:
                err=False
                drives[i]['score'] = 6
                drives[i]['edit'] = 1
                drives[i]['result'] += " "+comment
            else:
                nerr += 1                
            
            scores[drivingteam] = scores[drivingteam] + scoreval
        else:
            err=False
            scores[drivingteam] = scores[drivingteam] + scoreval
        
        if showResult:
            print i,'\t',Fix(drivingteam,10),'\t',drive['score'], drive['runningscore'],'\t',scores[drivingteam],'\t',drive['summary'],'\t',drive['result'],
            if err:
                print '\t\t',err,'\t(',diff,')'
            else:
                print ''

    if nerr > 3:
        print "There were",nerr,"remaining errors in the drive summary"
        f()
    return drives
    

def parseDriveSummary(drive, debug):
    vals=drive.split("<span")
    res={}
    res['summary'] = None
    res['team'] = None
    res['result'] = None
    res['score'] = None
    res['runningscore']=[]
    
    for val in vals:        
        ## Headline
        hline="class=\"headline\">"
        if val.find(hline) != -1:
            #print val
            pos=val.find(hline)
            dresult=val[pos+17:-7]
            res['result'] = dresult
            res['score'] = driveScore(dresult)

            
        ## Get Score Info
        tname="class=\"team-name\">"
        if val.find(tname) != -1:
            pos1=val.find(tname)
            if pos1 == -1:
                print "Could not find current team name when parsing..."
            pos2=val.find("</span>", pos1+1)
            teamname=val[pos1+len(tname):pos2]
            
        ## Get Score Info
        tscore="class=\"team-score\">"
        if val.find(tscore) != -1:
            pos1=val.find(tscore)
            if pos1 == -1:
                print "Could not find current team score when parsing..."
            pos2=val.find("</span>", pos1+1)
            teamscore=int(val[pos1+len(tscore):pos2])
            res['runningscore'].append([teamname, teamscore])


        ## Details
        details="class=\"drive-details\">"
        if val.find(details) != -1:
            pos1=val.find(details)
            pos2=val.find("</span>")
            detail=val[pos1+len(details):pos2]
            dvals=detail.split(",")
            try:
                plays=dvals[0].replace("plays","")
                plays=plays.replace("play","")
                yards=dvals[1].replace("yards","")
                yards=yards.replace("yard","")
            except:
                print "Problem with drive (plays,yards) details"
                print dvals
                f()
                
            if len(dvals) == 3:
                try:
                    ptime=dvals[2].strip()
                    m,s=ptime.split(":")            
                except:
                    print "Problem with drive (time) details"
                    print dvals
                    f()
            else:
                m=0
                s=0                
                
            try:
                details=[int(plays), int(yards), int(m), int(s)]
            except:
                print "Problem with drive details: Making ints"
                print dvals
                f()
            res['summary'] = details

            
        ## Game title
        logo="class=\"home-logo\">"
        if val.find(logo) != -1:
            pos2=val.find(".png")
            pos1=val.find("/", pos2-5)
            if pos1 == -1 or pos2 == -1:
                continue
                print "Problem parsing logo in drive summary:",val
                f()
            teamnum = val[pos1+1:pos2]
            try:
                teamnum=int(teamnum)
            except:
                print "Problem parsing team number:",teamnum
                print "Original value:",val[pos1+1:pos2]
                print pos1
                print pos2
                f()
            res['team'] = teamnum

    for k,v in res.iteritems():
        if v == None:
            continue
            print "Could not parse drive"
            print 'drive -->',drive
            print '==============================='
            print res
            f()

    #analyzeDriveSummary(res)

    if res['team'] == None:
        return None
        
    
    return res


def updateTime(ptime, newval):
    minval=ptime[0]
    secval=ptime[1]

    minval += newval[0]
    secval += newval[1]
    if secval > 60:
        minval += 1
        secval -= 60
    return [minval,secval]

def getDown(down):
    if down == "1st":
        down=1
    elif down == "2nd":
        down=2
    elif down == "3rd":
        down=3
    elif down == "4th":
        down=4
    else:
        print "Unknown down",down
        f()
    return down

def parsePlays(gameid, teams, allplays, dsum):
    plays=[]
    currstate=None
    quarter=1

    showPlay=False
    try:
        teamnum,addr=tn.stripTeamNum(allplays[0])
    except:
        print "Problem with getting driving team!",allplays[0]
        return None,plays
        print dsum
        f()
    drivingteam = teams[teams[teamnum]]
    teamname = teams[teamnum]
    for p in range(len(allplays)-2):
        play = allplays[p]
        if allplays[p] == "<span class=\"post-play\">" and allplays[p+2] == "</span>":
            playresult = allplays[p+1]
            if playresult.find("NO PLAY") != -1:
                continue
            if showPlay: print '--->',playresult
            if currstate:
                currplay = [currstate, playresult]
                plays.append(currplay)
                currstate = None
            else:
                print "No information about the drive state!"
                f()

        if (allplays[p] == "<li class=\"end-quarter\">" or allplays[p] == "<li class=\"half-time\">") and allplays[p+2] == "<p>":
            driveinfo=[0,0,0]
            if showPlay: print '--->',driveinfo
            currstate=driveinfo


        if (allplays[p] == "<li class=\"\">" or allplays[p] == "<li class=\"video\">") and allplays[p+2] == "<p>":
            drivestate = allplays[p+1]
            drivestate = drivestate.replace("<h3>", "")
            drivestate = drivestate.replace("</h3>", "")
            if drivestate == "":
                drivestate = "Kickoff"
            vals=drivestate.split()
            driveinfo=[]
            if len(vals) == 1:
                driveinfo=[0,0,0]
            elif len(vals) == 6:
                down=getDown(vals[0])
                if vals[2] == "Goal":
                    togo="Goal"
                else:
                    togo=int(vals[2])
                if vals[4] == drivingteam:
                    dist=100 - int(vals[5])
                else:
                    dist=int(vals[5])
                driveinfo=[down,togo,dist]
            elif len(vals) == 5:
                if vals[0] == "and":
                    driveinfo=[0,"2 PT",int(vals[4])]
                elif vals[4] == "50":
                    down=getDown(vals[0])
                    if vals[2] == "Goal":
                        togo="Goal"
                    else:
                        togo=int(vals[2])
                    dist=50
                    driveinfo=[down,togo,dist]
                else:
                    print "Can not parse drive state!",drivestate
                    f()                        
            else:
                print "Can not parse drive state!",drivestate
                f()
            if showPlay: print '--->',drivestate,'\t\t',driveinfo
            currstate=driveinfo
                
    return teamname,plays

def parsePlayByPlay(gameid, pbp, team1data, team2data, debug):
    j=0
    ndrives=0
    drives=[]
    driveplays=[]
    awayteam=[team1data[1], team1data[3]]
    hometeam=[team2data[1], team2data[3]]
        
    teams={}
    teams[int(team1data[1])] = tc.TeamConv(team1data[0])
    teams[int(team2data[1])] = tc.TeamConv(team2data[0])
    teams[team1data[3]] = tc.TeamConv(team1data[0])
    teams[team2data[3]] = tc.TeamConv(team2data[0])
    teams[tc.TeamConv(team1data[0])] = team1data[3]
    teams[tc.TeamConv(team2data[0])] = team2data[3]
    while j < len(pbp):
        line = pbp[j]
        
               
        ## Game title
        drive="<span class=\"drive-details\">"
        dsum = None
        if line.find(drive) != -1 and False:
            continue
        
            dsum = parseDriveSummary(line, debug)
            if debug:
                print "Drive[",ndrives,'] -->',dsum
            if dsum == None:
                j += 1
                continue
            drives.append(dsum)
            ndrives += 1
            
        flag="<ul class=\"drive-list\">"
        if line.find(flag) != -1:
            k=j+1
            try:
                while pbp[k].find("</ul>") == -1:
                    k += 1
            except:
                k=len(pbp)
            teamname,plays=parsePlays(gameid, teams, pbp[j:k], dsum)
            if teamname == None or len(plays) == 0:
                j += 1
                continue
            plays.insert(0, teamname)
            driveplays.append(plays)
            if debug: print len(plays),'\t',plays                

        j += 1

#    if len(drives) != len(driveplays):
#        print "Found",len(drives),"drive summaries and",len(driveplays),"drive plays."
#        f()
        
    #drives = analyzeDriveSummary(gameid, drives, awayteam, hometeam)

    if len(driveplays) == 0:
        print "No drives found for this game."
        return None
        

    summary={}
    summary[tc.TeamConv(team1data[0])] = []
    summary[tc.TeamConv(team2data[0])] = []
    
    for i in range(len(driveplays)):
        team=driveplays[i][0]
        if summary.get(team) == None:
            print "Error paring drive plays for",team
            print summary.keys()
            f()
        plays = driveplays[i][1:]
        plays.insert(0, i)
        
        summary[team].append(plays)
        
    return summary