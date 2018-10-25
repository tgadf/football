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
# parseTeamData()
#
#
##############################################################################    
def parseTeamData(line, teams, showData):
    pos=line.find("<thead><tr>")
    if pos == -1:
        print "Problem parseing team data",line
        f()
        
    ## Get name
    info=line[:pos]
    info=info.replace("</caption>", "")
    ipos=info.rfind(">")
    info=info[ipos+1:]
    dataname=info
    teamname=None
    for team,tconv in teams.iteritems():
        if dataname.find(team) != -1:
            teamname = tconv
            break
    
    if teamname == None:
        print "Could not find team in",dataname
        print "Expected:",teams
        f()
    #print 'Data ->',dataname
    
    ## Get info
    line=line[pos:]
    line=line.replace("<thead>", "")
    #print 'Full line --->',line
    #print ''
    
    lines=line.split("<tr")
    if len(lines[0]) == 0:
        lines.pop(0)
        
    for l in range(len(lines)):
        if lines[l][0] == '>':
            lines[l] = lines[l][1:]
        lines[l] = lines[l].strip()
        #print '\t',l,'\t',lines[l]
    #print ''
        
    keys=[]
    headers=lines[0].split("<th")
    headers=[x.replace("class=\"", "") for x in headers]
    headers=[x.replace("</th>", "") for x in headers]
    headers=[x.strip() for x in headers]
    headers=[x for x in headers if x != ""]
    for h in range(len(headers)):
        pos=headers[h].find("\">")
        if pos != -1:
            headers[h] = headers[h][:pos]
        keys.append(headers[h])
        #print '\t',h,'\t',headers[h]
    #print ''

    values={}
    if showData: print 'keys --->',keys
    lines.pop(0)
    if showData: print lines
    if showData: print ''
    teamvals={}
    noInfo=False
    
    for lne in lines:
        lvals=lne.split("</td")

        vals=[]        
        for k in range(len(keys)):
            if lvals[k].find("class=\""+keys[k]+"\"") == -1:
                if lvals[k].find("No") == -1:
                    print "Problem parsing box score"
                    print keys[k]
                    print keys
                    print lvals
                    f()
                else:
                    noInfo=True
                    break
            
            lvals[k] = lvals[k].replace("</a>", "")
            lvals[k] = lvals[k].strip()
            pos = lvals[k].rfind(">")
            val = lvals[k][pos+1:]
            vals.append(val)
            #print keys[k],'\t',val

        if not noInfo:         
            teamvals[vals[0]] = vals[1:]
            if showData: print '\t',vals[0], teamvals[vals[0]]


    if noInfo:
        teamvals["None"] = []
        for i in range(len(keys)-1): teamvals["None"].append('0')
            

    keys=keys[1:]        
    for name in teamvals.keys():
        val = teamvals[name]
        data={}
        for i in range(len(keys)):
            if val[i].find(".") != -1: data[keys[i]] = float(val[i])
            elif val[i].find("/") != -1: data[keys[i]] = [int(x) for x in val[i].split("/")]
            else: 
                try:
                    data[keys[i]] = int(val[i])
                except:
                    data[keys[i]] = str(val[i])
        teamvals[name] = data
        
    try:
        field = dataname.replace(teamname, "").strip()
    except:
        print "Problem parsing data field name",dataname
        f()
        

    if showData: print teamname,'\t',field,'\t',teamvals
    return teamname,field,teamvals


    
    
##############################################################################
#
#
# parseBoxScore()
#
#
##############################################################################
def parseBoxScore(bdata, team1data, team2data, debug):
    teams={}
    teams[int(team1data[1])] = tc.TeamConv(team1data[0])
    teams[int(team2data[1])] = tc.TeamConv(team2data[0])
    teams[team1data[3]] = tc.TeamConv(team1data[0])
    teams[team2data[3]] = tc.TeamConv(team2data[0])

    values={}
    values[tc.TeamConv(team1data[0])] = {}
    values[tc.TeamConv(team2data[0])] = {}
    
    tconvs={}
    for team in values.keys():
        tconvs[team] = team
        invconv = tc.InvTeamConv(team)
        if invconv == team:
            continue
        tconvs[invconv] = team
        
    for team in values.keys():
        if team.find("State") != -1:
            tstate = team.replace("State", "").strip()
            if tconvs.get(tstate) == None:
                tconvs[tstate]= team
    
    showData=debug
    
    for i in range(len(bdata)):
        line=bdata[i]
        if line.find("class=\"boxscore-tabs game-package-box-score ") != -1:
            vals=line.split("<div class=\"col column-")
            for val in vals:
                if val.find(".png") != -1:
                    teamnum,addr = tn.stripTeamNum(val)
                else:
                    continue
#                try:
#                    print val
#                    teamnum,addr = tn.stripTeamNum(val)
#                except:
#                    print val
#                    continue
                if showData: print ''
                if showData: print teamnum
                teamname,field,teamdata=parseTeamData(val, tconvs, showData)
                if values.get(teamname) == None:
                    print "Did not recognize team",teamname
                    print "Should be",values.keys()
                    f()
                values[teamname][field] = teamdata
                if showData: print teamname,'\t',field,'\t',teamdata
                if showData: print ''

    if showData: print values
        
    return values