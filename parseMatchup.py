# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 14:02:40 2015

@author: tgadfort
"""

import TeamConv as tc
import teamNum as tn


##############################################################################
#
#
# parseMatchup()
#
#
##############################################################################

def getAttr(mdata, key, i):
    j=i
    attrs=[]
    while j < len(mdata):
        #print j,'\t',mdata[j]
        if j > i + 20:
            f()
        value=None
        if mdata[j].find("</tr>") != -1:
            break
        if mdata[j].find("td>") == -1:
            value=mdata[j].strip()
            #print '--->',j,value
            attrs.append(value)            
        j += 1

    if len(attrs) == 4:
        attrs.pop(0)
    name=attrs[0]
    val1=attrs[1]
    val2=attrs[2]
    itype=int    
    if val1.find("-") != -1 and val2.find("-") != -1: itype = str
    if val1.find(".") != -1 and val2.find(".") != -1: itype = float
    if val1.find(":") != -1 and val2.find(":") != -1: itype = complex
    
    if itype == int:
        val1=int(val1)
        val2=int(val2)
    if itype == float:
        val1=float(val1)
        val2=float(val2)
    if itype == str:
        vals=val1.split('-')
        if len(vals[0]) == 0:
            val1 = int(val1)
        else:
            vals=[int(x) for x in val1.split("-")]
            val1 = [vals[0], vals[1]]
            
        vals=val2.split('-')
        if len(vals[0]) == 0:
            val2 = int(val2)
        else:
            vals=[int(x) for x in val2.split("-")]
            val2 = [vals[0], vals[1]]
    if itype == complex:
        vals=[int(x) for x in val1.split(":")]
        val1 = [vals[0], vals[1]]
        vals=[int(x) for x in val2.split(":")]
        val2 = [vals[0], vals[1]]
        
    #print 'attrs->',attrs
    #print val1,val2    
    retval=[name, val1, val2]    
    
    return retval


def parseMatchup(mdata, team1data, team2data, debug):
    teams={}
    teams[int(team1data[1])] = tc.TeamConv(team1data[0])
    teams[int(team2data[1])] = tc.TeamConv(team2data[0])
    teams[team1data[3]] = tc.TeamConv(team1data[0])
    teams[team2data[3]] = tc.TeamConv(team2data[0])
    summary=[]
    #print len(mdata)

    teamorder=[None,None]
    keys=["firstDowns", "thirdDownEff", "fourthDownEff", 
          "totalYards", "netPassingYards",
          "yardsPerPass", "completionAttempts", "interceptions",
          "rushingYards", "rushingAttempts", "yardsPerRushAttempt",
          "totalPenaltiesYards", "turnovers", "fumblesLost",
          "interceptions", "possessionTime"]
    values={}
    for key in keys:
        values[key] = None



    for i in range(len(mdata)):
        line=mdata[i]
        if line == "<th>Matchup</th>":
            j=i+1
            while j < len(mdata):
                if mdata[j].find("<img src=") != -1:
                    teamnum,addr=tn.stripTeamNum(mdata[j])
                    if teamorder[0] == None:
                        teamorder[0] = teams[teamnum]
                        j+=1
                        continue
                    if teamorder[1] == None:
                        teamorder[1] = teams[teamnum]
                        break
                j +=1 

        for key in keys:
            if line.find("data-stat-attr=\""+key+"\"") != -1:
                attr=getAttr(mdata, key, i)
                values[key] = attr
                #print key,'\t',attr
                break

    if teamorder[0] == None or teamorder[1] == None:
        return None

    retvals={}
    retvals[teamorder[0]] = {}
    retvals[teamorder[1]] = {}
    for k,v in values.iteritems():
        if v == None:
            retvals[teamorder[0]][k] = None
            retvals[teamorder[1]][k] = None
        else:
            retvals[teamorder[0]][v[0]] = v[1]
            retvals[teamorder[1]][v[0]] = v[2]
    return retvals