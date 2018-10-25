# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 20:53:42 2015

@author: tgadfort
"""


import TeamConv as tc
import teamNum as tn
import getHTML as web
import os
import glob
import json

def getURL(basepath, name, url, force):
    #result = web.checkURL(url)
    result = True
    if result == False:
        print ' --->',url,' = ',result
        return result

    savehtml = os.path.abspath(basepath+"/" + name + ".html")
    
    if os.path.exists(savehtml) and force == False:
        #print " Did not download",url,"\tforce = FALSE"
        return False
        
    result=web.getHTML(url, savehtml)
    if result:
        print ' --->',url,'  in  ',savehtml
    else:
        print " Did not download",url
        
    return True


def stripLink(link):
    if link.find("<a") == -1 and link.find("</a") == -1:
        return link
    
    pos  = link.find("\"")
    link = link[pos+1:]
    pos  = link.find("\"")
    
    rellink = link[:pos]
    name    = link[pos+2:]
    relvals = rellink.split("/")
    webname = relvals[3].split(".")[0]
    
    pos  = name.find("<")
    name = name[:pos]    
    
    return [name, webname, rellink]


def getSFref(sprefhtml, force):
    url="http://www.sports-reference.com/cfb/schools/"
    basepath = os.path.dirname(sprefhtml)
    filename = os.path.basename(sprefhtml).split('.')[0]
    retval = getURL(basepath, "index", url, force)



def parseSFref(sprefhtml, sprefteamsjsonfile):
    fdata = open(sprefhtml).readlines()
    fdata = [x.strip('\r\n') for x in fdata]

    i = 0
    sfdata=[]
    while i < len(fdata):
        line = fdata[i]
        if line.find("<colgroup>") == -1:
            i += 1
            continue
        j = i + 1
        while line.find("<tr class=\"\">") == -1:
            print j
            j += 1
            line = fdata[j]
        j += 1
        line = fdata[j]
        headers=[]
        while line.find("</tr") == -1:
            vals=line.split("=")
            print 'x\t',len(vals),'\t',vals
            name = vals[1].replace("\"", "")
            if len(vals) > 4:
                tip  = vals[4].replace("</th>", "")
            else:
                tip  = vals[3].replace("</th>", "")
            tip  = tip.replace("\"", "")
            tip  = tip.replace("data-filter", "").strip()
            ptip = tip.find(">")
            if ptip > 0:
                tip = tip[:ptip]
            name = name.split()[0]
            headers.append([name,tip])
            j += 1
            line = fdata[j]
            
        j += 1
        line = fdata[j]
        while line.find("<tr") == -1:
            j += 1
            line = fdata[j]
            
        while line == "<tr  class=\"\">":
            j += 1
#            print fdata[j]
            values={}
            for k in range(len(headers)):
                val=fdata[j+k].replace("</td>", "")
                pos=val.find(">")
                val=val[pos+1:]
                #print k,'\t',headers[k],'\t',val
                val = stripLink(val)
                vkey = headers[k][0]
                values[vkey] = val
                #print '\t',vkey,'\t',val
            j += len(headers)+1
            sfdata.append(values)
            line = fdata[j]           
            if len(sfdata) % 20 == 0:
                while line != "<tr  class=\"\">":
                    j += 1
                    line = fdata[j]
        break
    
    print "\tWriting",len(sfdata),'to',sprefteamsjsonfile
    json.dump(sfdata, open(sprefteamsjsonfile, "w"))
    
    
def getSFrefTeams(spteampath, sprefteamsjsonfile, force):

    base="http://www.sports-reference.com"
    teams = json.load(open(sprefteamsjsonfile))
    for team in teams:
        teamurl  = team['school_name'][2]
        teamname = team['school_name'][1]
        url = base + teamurl
        retval = getURL(spteampath, teamname, url, force)        

    return True
    
    

def parseSFrefTeams(spteampath, sprefteamsjsonfile, force):
    teamdata={}
    teamhtmls = glob.glob(spteampath + "/*.html")
    for teamhtml in teamhtmls:
        fdata = open(teamhtml).readlines()
        fdata = [x.strip('\r\n') for x in fdata]
        
        teamname = os.path.basename(teamhtml).split(".")[0]
        key = teamname

        i = 0
        sfdata=[]
        while i < len(fdata):
            line = fdata[i]
            if line.find("<colgroup>") == -1:
                i += 1
                continue
            j = i + 1
            while line.find("<tr class=\"\">") == -1:
#                print j
                j += 1
                line = fdata[j]
            j += 1
            line = fdata[j]
            headers=[]
            while line.find("</tr") == -1:
                vals=line.split("=")
                #print ' ',len(vals),'\t',vals
                name = vals[1].replace("\"", "")
                name = name.replace("align", "").strip()
                if len(vals) > 4:
                    tip  = vals[4].replace("</th>", "")
                else:
                    tip  = vals[3].replace("</th>", "")
                tip  = tip.replace("\"", "")
                tip  = tip.replace("data-filter", "").strip()
                ptip = tip.find(">")
                if ptip > 0:
                    tip = tip[ptip+1:]
                headers.append([name,tip])
                j += 1
                line = fdata[j]


            j += 1
            line = fdata[j]
            while line.find("<tr") == -1:
                j += 1
                line = fdata[j]
                
            while line == "<tr  class=\"valign_top\">":
                j += 1
    #            print fdata[j]
                values={}
                for k in range(len(headers)):
                    val=fdata[j+k].replace("</td>", "")
                    pos=val.find(">")
                    val=val[pos+1:]
#                    print k,'\t',headers[k],'\t',val
                    val = stripLink(val)
                    vkey = headers[k][0]
                    values[vkey] = val
                    #print '\t',vkey,'\t',val
                j += len(headers)+1
                sfdata.append(values)
                line = fdata[j]
                #print len(sfdata),'\t',values['Year'],'  ',line
                if len(sfdata) % 20 == 0:
                    while line != "<tr  class=\"valign_top\">":                        
                        j += 1
                        try:
                            line = fdata[j]
                        except:
                            break
            break
        
        teamdata[key] = sfdata
        print '\t',key
        
    print "\tWriting",len(teamdata),'to',sprefteamsjsonfile
    json.dump(teamdata, open(sprefteamsjsonfile, "w"))



def getSFrefTeamYears(spyearpath, sprefteamfile, force):
    if not force:
        print "Not downloading or checking SPref team-years."
        return
    webbase="http://www.sports-reference.com"
    sprefteamdata = json.load(open(sprefteamfile))
    for k,v in sprefteamdata.iteritems():
        teamname = k
        teamdata = v
        for yeardata in teamdata:
            yearhtml = yeardata['year_id'][2]
            year     = yeardata['year_id'][0]
            url = webbase + yearhtml
            retval = getURL(spyearpath, teamname + "-" + year, url, force)


    
def parseSFrefTeamYears(spyearpath, sprefteamyearjsonfile, force):
    teamhtmls = glob.glob(spyearpath + "/*.html")
    webbase="http://www.sports-reference.com"


    gamelogs=None
    pteamname=None
    yeardata={}
    for teamhtml in teamhtmls:
        fdata = open(teamhtml).readlines()
        fdata = [x.strip('\r\n') for x in fdata]

        teamyearname = os.path.basename(teamhtml).split(".")[0]
        key = teamyearname
        vals = teamyearname.split("-")
        year = vals[-1]
        teamname = "-".join(vals[:-1])
        
        if teamname != pteamname and pteamname != None:
            print '\t',pteamname
            if gamelogs:
                for i in range(len(gamelogs)):
                    gamelog = gamelogs[i]
                    pos = gamelog.find("<a href=\"")
                    gameloghtml = gamelog[pos + 9:]
                    pos = gameloghtml.find("\">")
                    gameloghtml = gameloghtml[:pos]
                    url = webbase + gameloghtml
                    gamelogs[i] = url
                    vals = url.split("/")[5:8]
                    savepath = os.path.abspath(spyearpath + "/GameLogs/")
                    retval = getURL(savepath, "-".join(vals), url, force)

            gamelogs = None
            
        pteamname = teamname


        i = 0
        sfdata=[]
        if gamelogs == None:
            while i < len(fdata):
                line = fdata[i]
                if line.find("/gamelog/") != -1:
                    gamelogs = []
                    i += 1
                    line = fdata[i]
                    while line.find("</ul>") == -1:
                        if line.find("/gamelog/") != -1:                        
                            gamelogs.append(line)
                        i += 1
                        line = fdata[i]
                i += 1

          
        i = 0
        statval = None
        yearstats = {}
        while i < len(fdata):
            line = fdata[i]

            tval = "<h2 data-mobile-header=\"\" style=\"\">"      
            if line.find(tval) != -1:
                statval = line.replace(tval, "")
                statval = statval.replace("</h2>", "")
                statval = statval.replace("&amp;", "and")
                i += 1
                continue

            if line.find("<colgroup>") == -1:
                i += 1
                continue
            
            j = i + 1
            while line.find("<tr class=\"\">") == -1:
#                print j
                j += 1
                line = fdata[j]
            j += 1
            line = fdata[j]
            headers=[]
            while line.find("</tr") == -1:
                vals=line.split("=")
                #print ' ',len(vals),'\t',vals
                name = vals[1].replace("\"", "")
                name = name.replace("align", "").strip()
                if len(vals) > 4:
                    tip  = vals[4].replace("</th>", "")
                else:
                    tip  = vals[3].replace("</th>", "")
                tip  = tip.replace("\"", "")
                tip  = tip.replace("data-filter", "").strip()
                ptip = tip.find(">")
                if ptip > 0:
                    tip = tip[ptip+1:]
                headers.append([name,tip])
                j += 1
                line = fdata[j]
#                print j,'\t',tip,'\t',line.find("</tr"),'\t',line,'\t',fdata[j+1]



            j += 1
            line = fdata[j]
            while line.find("<tr") == -1:
                j += 1
                line = fdata[j]
                
            while line == "<tr  class=\"\">":
                j += 1
    #            print fdata[j]
                values={}
                for k in range(len(headers)):
                    val=fdata[j+k].replace("</td>", "")
                    pos=val.find(">")
                    val=val[pos+1:]
#                    print k,'\t',headers[k],'\t',val
                    values[headers[k][0]] = val
                j += len(headers)+1
                sfdata.append(values)
                line = fdata[j]
            
            
            if statval:
                yearstats[statval] = sfdata
                #print statval,'\t',len(sfdata)
                statval = None
                sfdata=[]
            else:
                print "No statval key!"
                f()

            i += 1

        yeardata[key] = yearstats
        
    print " Writing",len(yeardata),'stat types to',sprefteamyearjsonfile
    json.dump(yeardata, open(sprefteamyearjsonfile, "w"))


def parseSFrefTeamGameLog(spyearpath, sprefgamelogsjsonfile, force):    
    basepath = os.path.abspath(spyearpath + "/GameLogs/")
    gameloghtmls = glob.glob(basepath + "/*.html")
    webbase="http://www.sports-reference.com"

    yeardata = {}

    for teamhtml in gameloghtmls:
        fdata = open(teamhtml).readlines()
        fdata = [x.strip('\r\n') for x in fdata]

        key = os.path.basename(teamhtml).split(".")[0]
        key = key.replace("-gamelog", "")

        i = 0
        statval = None
        sfdata=[]
        yearstats={}
        while i < len(fdata):
            line = fdata[i]

            tval = "<h2 data-mobile-header=\"\" style=\"\">"      
            if line.find(tval) != -1:
                statval = line.replace(tval, "")
                statval = statval.replace("</h2>", "")
                statval = statval.replace("&amp;", "and")
                i += 1
                continue

            if line.find("<colgroup>") == -1:
                i += 1
                continue
            
            j = i + 1
            while line.find("<tr class=\"\">") == -1:
#                print j
                j += 1
                line = fdata[j]
            j += 1
            line = fdata[j]
            headers=[]
            while line.find("</tr") == -1:
                vals=line.split("=")
                #print ' ',len(vals),'\t',vals
                name = vals[1].replace("\"", "")
                name = name.replace("align", "").strip()
                if len(vals) > 4:
                    tip  = vals[4].replace("</th>", "")
                else:
                    tip  = vals[3].replace("</th>", "")
                tip  = tip.replace("\"", "")
                tip  = tip.replace("data-filter", "").strip()
                ptip = tip.find(">")
                if ptip > 0:
                    tip = tip[ptip+1:]
                headers.append([name,tip])
                j += 1
                line = fdata[j]
#                print j,'\t',tip,'\t',line.find("</tr"),'\t',line,'\t',fdata[j+1]


            j += 1
            line = fdata[j]
            while line.find("<tr") == -1:
                j += 1
                line = fdata[j]
                
            while line == "<tr  class=\"\">":
                j += 1
    #            print fdata[j]
                values={}
                for k in range(len(headers)):
                    val=fdata[j+k].replace("</td>", "")
                    pos=val.find(">")
                    val=val[pos+1:]
#                    print k,'\t',headers[k],'\t',val
                    values[headers[k][0]] = val
                j += len(headers)+1
                sfdata.append(values)
                line = fdata[j]
            
            
            if statval:
                yearstats[statval] = sfdata
                statval = None
                sfdata=[]
            else:
                print "No statval key!"
                f()

            i += 1
        yeardata[key] = yearstats
        print '\t',key

    print " Writing",len(yeardata),'stat types to',sprefgamelogsjsonfile
    json.dump(yeardata, open(sprefgamelogsjsonfile, "w"))