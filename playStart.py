#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 19:31:36 2019

@author: tgadfort
"""

import re

from playClock import playclock

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class playstartclass:
    def __init__(self, down=None, togo=None, startY=None, side=None, extra=None):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        
        self.down   = down
        self.togo   = togo
        self.startY = startY
        self.side   = side
        self.extra  = extra
        
        self.quarter       = None
        self.gameclock     = None
        self.distToEndZone = None
        
        self.logger.debug("{0}Play Start: Down [{1}], ToGo [{2}], and Line [{3}]".format(self.ind,self.down,self.togo,self.startY))
        
    def get(self):
        keys = ["down", "togo", "startY", "side", "extra", "quarter", "gameclock", "distToEndZone"]
        retval = {k:self.__dict__[k] for k in keys}
        return retval

        
    def setStartY(self, startY):
        self.startY = startY
        
    def setDistToEndZone(self, dist):
        self.distToEndZone = dist
        
    def setQuarter(self, quarter):
        self.quarter = quarter
        
    def setGameClock(self, gameclock):
        self.gameclock = gameclock
        
    def setClock(self, pc):
        if not isinstance(pc, playclock):
            self.logger.error("{0}Clock data is not of type playclock!".format(self.ind))
            return
        
        self.setQuarter(pc.getQuarter())
        self.setGameClock(pc.getClock())
        

class playstart:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 4*" "
        self.logger.debug("Creating PlayStart Class")
    
        assert self.getStart("2nd & 10 at SMU 47").down == 2, "Should be [2]"
        assert self.getStart("1st and GOAL at CAL 1").down == 1, "Should be [1]"
        assert self.getStart("3rd & 10 at 50").down == 3, "Should be [3]"
        assert self.getStart("4th & 3 at XIY 19").down == 4, "Should be [4]"
        assert self.getStart("5th & 3 at XIY 19").down == None, "Should be [None]"
        
        
    def getStart(self, text):
        ps = None
        self.logger.debug("{0}Finding Play Start for text [{1}]".format(self.ind, text))
        
        down = "(st|nd|rd|th)"
        num  = "(\d+)"
        word = "(\w+)"
        goal = "(GOAL|goal|Goal)"
        prep = "(on|at)"
        amp  = "(&|and)"
        
        if ps is None:
            ## Look for match of type [1st and 10 at CAL 19]
            m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}\s{6}".format(num, down, amp, num, prep, word, num), text)
            if m is not None:
                groups = m.groups()
                try:
                    down   = int(groups[0])
                    togo   = int(groups[3])
                    startY = int(groups[6])
                    side   = groups[5]
                    ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
                except:
                    self.logger.error("Could not parse: {0}".format(text))
            
            
        if ps is None:
            ## Look for match of type [1st and GOAL at CAL 1]
            m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}\s{6}".format(num, down, amp, goal, prep, word, num), text)
            if m is not None:
                groups = m.groups()
                down   = int(groups[0])
                togo   = int(groups[6]) ## replace goal with distance to goal
                startY = int(groups[6])
                side   = groups[5]
                ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
            

        if ps is None:
            ## Look for very near match without side of field [1st and 10 at 50]
            m = re.search(r"{0}{1}\s{2}\s{3}\s{4}\s{5}".format(num, down, amp, num, prep, num), text)
            if m is not None:
                groups = m.groups()
                down   = int(groups[0])
                togo   = int(groups[3])
                startY = int(groups[5])
                side   = None
                ps     = playstartclass(down=down, togo=togo, startY=startY, side=side)
            
        if ps is None:
            self.logger.warn("{0}  Could not determine start of play for text [{1}]".format(self.ind, text))
            ps = playstartclass()

        
        ### Basic tests
        if isinstance(ps.down, int):
            if ps.down > 4 or ps.down < 1:
                self.logger.error("{0}Down is not correct: {1}".format(self.ind, text))
                ps.down = None


        return ps
        