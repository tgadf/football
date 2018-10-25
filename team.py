#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:00:12 2017

@author: tgadfort
"""

import sys
if '/Users/tgadfort/Python' not in sys.path:
    sys.path.insert(0, '/Users/tgadfort/Python')

from fsio import setFile, isFile
from fileio import save
from path import getTeamsDBDir
from htmlParser import getHTML
from download import getURL

def getConferenceBaseURL():
    return "http://www.espn.com/college-football/standings/"

def getFBSURL():
    return getConferenceBaseURL()+"_/season/"
    
def getFCSURL():
    return getConferenceBaseURL()+"_/view/fcs/season/"
    
def getDIIURL():
    return getConferenceBaseURL()+"_/view/d2/season/"
    
def getDIIIURL():
    return getConferenceBaseURL()+"_/view/d3/season/"


def downloadConferenceData(yearID, debug = True):
    url = getFBSURL()+str(yearID)
    savename = setFile(getTeamsDBDir(), "FBS-"+str(yearID)+".p")
    if not isFile(savename):
        getURL(url, savename, debug)

    url = getFCSURL()+str(yearID)
    savename = setFile(getTeamsDBDir(), "FCS-"+str(yearID)+".p")
    if not isFile(savename):
        getURL(url, savename, debug)

    url = getDIIURL()+str(yearID)
    savename = setFile(getTeamsDBDir(), "DII-"+str(yearID)+".p")
    if not isFile(savename):
        getURL(url, savename, debug)

    url = getDIIIURL()+str(yearID)
    savename = setFile(getTeamsDBDir(), "DIII-"+str(yearID)+".p")
    if not isFile(savename):
        getURL(url, savename, debug)


def getConferenceData(yearID, confName, debug = True):
    savename = setFile(getTeamsDBDir(), confName+"-"+str(yearID)+".p")
    bsdata   = getHTML(savename)

    conferences = []
    h2s = bsdata.findAll("h2", {"class": "table-caption"})
    for h2 in h2s:
        span = h2.find("span", {"class": "long-caption"})
        if span:
            conferences.append(span.text)

    teamData = {}
    teamMap  = {}
                    
    tables = bsdata.findAll("table")
    for i,table in enumerate(tables):
        conferenceName = conferences[i]
        headers = []
        headers.append("Team")
        ths = table.findAll("th")
        for th in ths:
            span = th.find("span", {"class": "tooltip"})
            if span:
                headers.append(span.text)

        trs = table.findAll("tr", {"class": "standings-row"})
        for j,tr in enumerate(trs):
            tds = tr.findAll("td")
            
            ## Name
            try:
                ref      = tds[0].find("a").attrs['href']
                teamID   = ref.split("/")[-2]
                #teamName = ref.split("/")[-1]
                niceName = tds[0].find("span", {"class": "team-names"}).text
            except:
                #if debug:
                #print "Unknown team",tds[0]
                #print "Skipping..."
                continue

            teamMap[teamID] = {"CONF": conferenceName, "DIV": confName}
            if teamMap.get(conferenceName) == None:
                teamMap[conferenceName] = []
            teamMap[conferenceName].append(teamID)

            if teamMap.get(confName) == None:
                teamMap[confName] = []
            teamMap[confName].append(teamID)
            
            teamData[teamID] = {}

            localData = []
            localData.append(niceName)
            #print niceName,'\t',teamID
            for k in range(1,len(tds)):
                #print j,'\t',k,'\t',tds[k].text
                localData.append(tds[k].text)
            teamData[teamID] = dict(zip(headers, localData))
            teamData[teamID]["Conference"] = conferenceName
            teamData[teamID]["Division"]   = confName
                    
            

    return teamMap, teamData


def createConferenceData(yearID, debug = False):
    teamMapFBS,teamDataFBS   = getConferenceData(yearID, 'FBS', debug)
    teamMapFCS,teamDataFCS   = getConferenceData(yearID, 'FCS', debug)
    teamMapDII,teamDataDII   = getConferenceData(yearID, 'DII', debug)
    teamMapDIII,teamDataDIII = getConferenceData(yearID, 'DIII', debug)
    
    teamMap  = teamMapFBS.copy()
    teamMap.update(teamMapFCS)
    teamMap.update(teamMapDII)
    teamMap.update(teamMapDIII)

    teamData = teamDataFBS.copy()
    teamData.update(teamDataFCS)
    teamData.update(teamDataDII)
    teamData.update(teamDataDIII)
    
    savename = setFile(getTeamsDBDir(), str(yearID)+"-Map.p")
    save(savename, teamMap, debug = True)
    
    savename = setFile(getTeamsDBDir(), str(yearID)+"-Data.p")
    save(savename, teamData, debug = True)