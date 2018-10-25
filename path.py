#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 13:03:40 2017

@author: tgadfort
"""

import sys
if '/Users/tgadfort/Python' not in sys.path:
    sys.path.insert(0, '/Users/tgadfort/Python')

from fsio import isDir, setSubDir

def getBase():
    dval = "/Users/tgadfort/Documents/football"
    if isDir(dval):
        return dval
    raise ValueError(dval,"does not exist!")
    

def getSchedulesDBDir():
    teamDBDir = setSubDir(getBase(), ["data", "schedules"])
    if not isDir(teamDBDir):
        raise ValueError(teamDBDir,"does not exist")
    return teamDBDir
    

def getTeamsDBDir():
    teamDBDir = setSubDir(getBase(), ["data", "teams"])
    if not isDir(teamDBDir):
        raise ValueError(teamDBDir,"does not exist")
    return teamDBDir
    

def getNetworkDBDir():
    networkDBDir = setSubDir(getBase(), ["data", "network"])
    if not isDir(networkDBDir):
        raise ValueError(networkDBDir,"does not exist")
    return networkDBDir