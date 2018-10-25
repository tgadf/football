# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 10:59:51 2015

@author: tgadfort
"""

import TeamConv as tc
import teamNum as tn


##############################################################################
#
#
# parseScoringSummary()
#
#
##############################################################################
def parseScoringSummary(gameid, scoredata, team1data, team2data, debug):
    scores=scoredata.split("<span class=\"headline\">")
    scores=scoredata.split("<div class=\"table-row\">")
    scores=scoredata.split("<img class=\"team-logo\" ")
    scores=scoredata.split("<tr><td class=\"logo\"><img class=\"team-logo\" ")

    teams={}
    teams[int(team1data[1])] = tc.TeamConv(team1data[0])
    teams[int(team2data[1])] = tc.TeamConv(team2data[0])
    teams[team1data[3]] = tc.TeamConv(team1data[0])
    teams[team2data[3]] = tc.TeamConv(team2data[0])
    summary=[]
    
    awayteam=None
    hometeam=None
    quarter=None
    for s in range(len(scores)):
        score=scores[s]
        teamnum,logoaddr=tn.stripTeamNum(score)
        
        

        ## Quarter
        flag="<th id=\"quarter-1\" class=\"quarter\" colspan=\"2\">"
        pos1=score.find(flag)
        pos2=score.find("</th>", pos1+1)
        if pos1 != -1:
            tmpquarter=score[pos1+len(flag):pos2]
        if quarter == None:
            quarter = tmpquarter            
            

        ## Score type        
        flag="<div class=\"score-type\">"
        pos1=score.find(flag)
        pos2=score.find("</div>", pos1+1)
        scoretype=score[pos1+len(flag):pos2]

        ## Drive time
        flag="<div class=\"time-stamp\">"
        pos1=score.find(flag)
        pos2=score.find("</div>", pos1+1)
        timestamp=score[pos1+len(flag):pos2]

        ## Result
        flag="<div class=\"headline\">"
        pos1=score.find(flag)
        pos2=score.find("</div>", pos1+1)
        headline=score[pos1+len(flag):pos2]
        
        ## Require timestamp and result to continue
        if len(timestamp) == 0 and len(headline) == 0:
            continue
        #print '[',timestamp,'][',headline,']'

        ## Score
        flag="<td class=\"home-score\">"
        pos1=score.find(flag)
        pos2=score.find("</td>", pos1+1)
        homescore=int(score[pos1+len(flag):pos2])

        ## Score
        flag="<td class=\"away-score\">"
        pos1=score.find(flag)
        pos2=score.find("</td>", pos1+1)
        awayscore=int(score[pos1+len(flag):pos2])

        ## Details
        flag="class=\"drive-details\">"
        details=[-1, -1, -1, -1]
        if score.find(flag) != -1 and True:
            pos1=score.find(flag)
            pos2=score.find("</div>", pos1+1)
            detail=score[pos1+len(flag):pos2]            
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
                    minutes,seconds=ptime.split(":")            
                except:
                    print "Problem with drive (time) details"
                    print dvals
                    f()
            else:
                minutes=-1
                seconds=-1
                
            try:
                details=[int(plays), int(yards), int(minutes), int(seconds)]
            except:
                print "Problem with drive details: Making ints"
                print dvals
                f()
        
        if hometeam == None:
            flag="<th class=\"home-team\">"
            pos1=score.find(flag)
            pos2=score.find("</th>", pos1+1)
            hometeam=score[pos1+len(flag):pos2]
        if awayteam == None:
            flag="<th class=\"away-team\">"
            pos1=score.find(flag)
            pos2=score.find("</th>", pos1+1)
            awayteam=score[pos1+len(flag):pos2]
        
        

        qnum=quarter.title()
        if qnum.find("First") != -1:
            qnum=1
        elif qnum.find("Second") != -1:
            qnum=2
        elif qnum.find("Third") != -1:
            qnum=3
        elif qnum.find("Fourth") != -1:
            qnum=4
        elif qnum.find("Overtime") != -1:
            qnum=5
        else:
            print "Could not extract quarter from",qnum
            f()
        summary.append([teams[teamnum], scoretype, qnum, timestamp, awayscore, homescore, headline, details])
        show=False
        if show:
            print s,'\t',teams[teamnum],'\t',scoretype,'\t',qnum,'\t',timestamp, '\t',
            print headline,'\t',awayteam,awayscore,'-',homescore,hometeam,'\t',
            print details,'\t',
            print scores[s]
        #,'\t\t',scores[s]
            
        quarter = tmpquarter
        
    scores={}
    scores[tc.TeamConv(team1data[0])] = []
    scores[tc.TeamConv(team2data[0])] = []
    summary=[]
    for i in range(len(summary)):
        teamname = tc.TeamConv(summary[i][0])
        if scores.get(teamname) == None:
            print "Key error in scores:",teamname
            print scores.keys()
            f()
        ssum = summary[i][1:]
        ssum.insert(0, i)
        scores[teamname].append(ssum)

    #print scores
    return scores