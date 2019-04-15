#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:52:31 2019

@author: tgadfort
"""

import sys
import re
from datetime import timedelta
from playTypes import playtype


############################################################################################################
## Drive Class
############################################################################################################
class driveclass:
    def __init__(self, headline, detail, possession, postdrivehomescore, postdriveawayscore, plays=None):
        self.headline = headline
        self.detail   = detail
        self.possession = possession
        self.postdrivehomescore = postdrivehomescore
        self.postdriveawayscore = postdriveawayscore
        self.plays = plays
        
    def setPlays(self, plays):
        self.plays = plays


############################################################################################################
## Drive Detail Class
############################################################################################################
class drivedetailclass:
    def __init__(self, plays, yards, gametime):
        self.plays = plays
        self.yards = yards
        self.gametime = gametime


############################################################################################################
## Drive Summary Class
############################################################################################################
class drivesummary:
    def __init__(self, drive, fieldMap):
        self.name = "drivesummary"
        
        self.headline = None
        self.score    = None
        self.details  = None
        
        self.fullDrive = None
    

        driveNo = drive.get('Drive')
        if driveNo is None:
            raise ValueError("No Drive in drive dict")

        headline = drive.get('Headline')
        if headline is None:
            raise ValueError("No Headline in drive dict")

        detail = drive.get('Detail')
        if detail is None:
            raise ValueError("No Detail in drive dict")

        possession = drive.get('Posession')
        if possession is None:
            raise ValueError("No Posession in drive dict")

        data = drive.get('Data')
        if data is None:
            raise ValueError("No Data in drive dict")


        ###
        ### For whatever reason home/away scores are reversed on the webpage...
        ###
        homescore = drive.get('AwayScore')
        if homescore is None:
            raise ValueError("No AwayScore in drive dict")
            
        awayscore = drive.get('HomeScore')
        if awayscore is None:
            raise ValueError("No HomeScore in drive dict")
                    


        self.possession = self.parsePossession(possession, fieldMap)
        self.headline   = self.parseHeadline(headline)
        self.detail     = self.parseDetail(detail)
        self.homescore  = self.parseScore(homescore)
        self.awayscore  = self.parseScore(awayscore)
        
        self.driveplays = data
                    
        self.fullDrive = driveclass(headline=headline, detail=detail, possession=possession,
                                    postdrivehomescore=homescore, postdriveawayscore=awayscore)    
    
    
    def getPostDriveScore(self):
        return [self.awayscore, self.homescore]
    
    def getDrivePlays(self):
        return self.driveplays
    
    def getFullDrive(self):
        return self.fullDrive

        
    def parsePossession(self, possession, fieldMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(possession, list):
            raise ValueError("Possession is not a list: {0}".format(possession))
            
        if len(possession) != 1:
            raise ValueError("Not one element in possession list: {0}".format(possession))
            
        teamID = possession[0]
        
        teamAbbrev = None
        try:
            teamAbbrev = fieldMap[teamID]
        except:
            raise ValueError("Could not find {0} in field map: {1}".format(teamID, fieldMap))
            
        return teamAbbrev
    
    

    def parseHeadline(self, headline, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        pltype = None
        
        if isinstance(headline, list):
            if len(headline) >= 1:
                ptype  = playtype(headline[0])
                pltype = ptype.getPlay()
                
                if pltype is None:
                    raise ValueError("Could not determine headline play type: {0}".format(headline[0]))
            else:
                print("Not one headline entry: {0}".format(headline))
        else:
            raise ValueError("Headline is not a list: {0}".format(headline))
                   
        return pltype
    
    
    def parseScore(self, score, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(score, list):
            raise ValueError("Could not determine score type: {0}".format(score))
            
        if len(score) != 1:
            raise ValueError("Not one detail entry: {0}".format(score))
            
        scoredata = score[0]
        
        try:
            scoredata = int(scoredata)
        except:
            raise ValueError("Could not find an integer score for {0}".format(scoredata))
            
        return scoredata
    
    
    def parseDetail(self, detail, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        if not isinstance(detail, list):
            raise ValueError("Could not determine detail play type: {0}".format(detail))
            
        if len(detail) != 1:
            raise ValueError("Not one detail entry: {0}".format(detail))
            
        detaildata = detail[0]
        
        
        yards = "(yards|yard|Yds|yds|Yd|yd)"
        plays = "(play|plays)"        
        num  = "([+-?]\d+|\d+)"
        
        totalplays = None
        totalyards = None
        totalclock = None

        m = re.search(r"{0}\s{1},\s{2}\s{3},\s{4}:{5}".format(num, plays, num, yards, num, num), detaildata)
        if m is not None:
            groups = m.groups()
            totalplays = int(groups[0])
            totalyards = int(groups[2])
            totalclock = timedelta(minutes=int(groups[4]), seconds=int(groups[5]))

            
        if totalplays is None and totalyards is None and totalclock is None:
            m = re.search(r"{0}\s{1},\s{2}\s{3}".format(num, plays, num, yards), detaildata)
            if m is not None:
                groups = m.groups()
                totalplays = int(groups[0])
                totalyards = int(groups[2])
                totalclock = timedelta(minutes=0, seconds=0)
                
            
        if totalplays is None and totalyards is None and totalclock is None:
            raise ValueError("Could not parse drive detail: {0}".format(detaildata))

        drivedetail = drivedetailclass(plays=totalplays, yards=totalyards, gametime=totalclock)
            
        return drivedetail
    
    
    