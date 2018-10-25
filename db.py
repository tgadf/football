#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:57:51 2017

@author: tgadfort
"""
import sys
if '/Users/tgadfort/Python' not in sys.path:
    sys.path.insert(0, '/Users/tgadfort/Python')

from fsio import setFile
from fileio import get,save
from search import findExt
from path import getTeamsDBDir
from htmlParser import getHTML
from strops import makeStrFromUnicode


def createTeamDB(debug = False):
    teamsDBDir = getTeamsDBDir()
    files = findExt(teamsDBDir, ext=".html")
    teamDB = {}
    for ifile in files:
        bsdata = getHTML(ifile)
        link = bsdata.find("link", {"rel": "canonical"})
        if link:
            href = link.attrs['href']
            vals = href.split('/')
            teamID   = vals[-2]
            teamName = makeStrFromUnicode(vals[-1])
            teamDB[teamName] = teamID

    saveTeamsDB(teamDB)
    
    
def getTeamsDB(debug = False):
    teamsDBDir  = getTeamsDBDir()
    teamsDBfile = setFile(teamsDBDir,"teamsDB.yaml")
    data = get(teamsDBfile, debug)
    return data


def saveTeamsDB(teamDB, debug = True):
    teamsDBDir  = getTeamsDBDir()
    savename = setFile(teamsDBDir,"teamsDB.yaml")
    save(savename, teamDB, debug)


def addTeam(teamID, teamName, debug = False):
    teamDB = getTeamsDB(debug)
    teamDB[teamName] = teamID
    saveTeamsDB(teamDB, debug)
