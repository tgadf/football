#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:19:00 2019

@author: tgadfort
"""


import re
from datetime import timedelta

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


class playclock:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        
        self.gamequarter = None
        self.gameclock   = None
        self.playtext    = None
        self.fulltext    = None
        
    def getQuarter(self):
        return self.gamequarter
    
    def getClock(self):
        return self.gameclock
    
    def getPlayText(self):
        return self.playtext
        
    
    def parsePlay(self, playData):
        self.logger.debug("{0}Finding Game Clock and Quarter from text {1}".format(self.ind, playData))
        
        self.fulltext = playData
        gameclock = None
        quarterNo = None
        
        ## Check for end of quarter/half/game
        if sum([x in playData for x in ["End of the ", "End Of The ", "end of the ", "end of ", "End of "]]) > 0:
            gameclock = timedelta(minutes=0, seconds=0) 
            if sum([x in playData for x in ["1st Quarter", "1st quarter"]]) > 0:
                quarterNo = 1
            elif sum([x in playData for x in ["2nd Quarter", "2nd quarter", "1st Half", "1st half", "half", "Half"]]) > 0:
                quarterNo = 2
            elif sum([x in playData for x in ["3rd Quarter", "3rd quarter"]]) > 0:
                quarterNo = 3
            elif sum([x in playData for x in ["4th Quarter", "4th quarter", "2nd Half", "2nd half", " Game", " game"]]) > 0:
                quarterNo = 4
            elif "OT" in playData:
                quarterNo = "OT"
            else:
                quarterNo = "UNKNOWN END QTR"
                #raise ValueError("Could not determine quarter from {0}".format(playData))

                
        if gameclock is None and quarterNo is None:
            ## Check for start of quarter/half/game
            if sum([x in playData for x in ["Start of the ", "Start Of The ", "start of the ", "start of "]]) > 0:
                gameclock = timedelta(minutes=15, seconds=0) 
                if sum([x in playData for x in ["1st Quarter", "1st quarter"]]) > 0:
                    quarterNo = 1
                elif sum([x in playData for x in ["2nd Quarter", "2nd quarter", "1st Half", "1st half"]]) > 0:
                    quarterNo = 2
                elif sum([x in playData for x in ["3rd Quarter", "3rd quarter", "2nd Half", "2nd half"]]) > 0:
                    quarterNo = 3
                elif sum([x in playData for x in ["4th Quarter", "4th quarter", "2nd Half", "2nd half", " Game", " game"]]) > 0:
                    quarterNo = 4
                elif "OT" in playData:
                    quarterNo = "OT"
                else:
                    quarterNo = "UNKNOWN START QTR"
                    #raise ValueError("Could not determine quarter from {0}".format(playData))

        
        if gameclock is None and quarterNo is None:

            ## Check for specific format (HH:MM - 1st)
            m = re.match(r"\((.*?)\)", playData)
            if m is None:
                self.logger.error("Could not determine time and quarter from {0}".format(self.ind, playData))

            try:
                text = m.group(0)
            except:
                self.logger.error("{0}Could not extract regex result from {1}".format(self.ind, playData))

               
            ## Check for overtime
            try:
                result = text[1:-1]
                if "OT" in result:
                    gameclock = timedelta(minutes=0, seconds=0) 
                    quarterNo = "OT"
            except:
                pass
            

            if gameclock is None:
                try:
                    result = text[1:-1]
                    result = result.split(" - ")
                    gameclock,quarter = result
                except:
                    self.logger.error("{0}Could not parse time data: {1}".format(self.ind, text))


                try:
                    minutes,seconds = gameclock.split(":")
                    gameclock = timedelta(minutes=int(minutes), seconds=int(seconds)) 
                except:
                    self.logger.error("{0}Could not create timedelta for {1}".format(self.ind, gameclock))


                quarterNo = {"1st":1, "2nd": 2, "3rd": 3, "4th": 4}.get(quarter)
                if quarterNo is None:
                    self.logger.warn("{0}Could not find quarter from [{1}] or [{2}]".format(self.ind, quarter, text))
                    #raise ValueError("Could not find quarter from [{0}] or [{1}]".format(quarter, text))


                try:
                    playData = playData.replace(text, "").strip()
                except:
                    self.logger.error("{0}Could not remove [{1}] from [{2}]".format(self.ind, text, playData))
                
        
        self.gameclock = gameclock
        self.gamequarter = quarterNo
        self.playtext = playData
        
        self.logger.debug("{0}  Found Game Clock [{1}], Game Quarter [{2}], and Remaining Text [{3}]".format(self.ind, self.gameclock, self.gamequarter, self.playtext))
        