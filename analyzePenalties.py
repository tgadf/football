#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:29:44 2019

@author: tgadfort
"""

from debug import debugclass

from playTypes import noplay
from playYards import playyards
#from copy import deepcopy, copy

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
## Drive Class
############################################################################################################
class analyzepenalties:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        self.sep    = "======================================================"
        
        self.dc = debugclass()
        
        self.py = playyards()
        
    
    def isPenaltyAdditive(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Penalty Additiveness".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if play.penalty.isPenalty is False:
                    continue
            
                penaltyyards  = play.penalty.yards
                playyards     = play.yds.yards
                nextYards     = drivePlay.nextDiffYards
                
                if all([penaltyyards, playyards, nextYards]):
                    if penaltyyards + playyards == nextYards:
                        continue
                    elif penaltyyards == playyards and penaltyyards == nextYards:
                        play.yds.yards = 0                        
                        continue
                    else:
                        self.logger.debug("{0}Penalty Analysis: Penalty Yards=={1}\tPlay Yards=={2}\tNext Yards=={3}\tText=={4}".format(self.ind, penaltyyards, playyards, nextYards, play.text))
                else:
                    self.logger.debug("{0}Penalty Analysis: Penalty Yards=={1}\tPlay Yards=={2}\tNext Yards=={3}\tText=={4}".format(self.ind, penaltyyards, playyards, nextYards, play.text))
                
                
        
        self.logger.debug("{0}Analyzing Penalty Additiveness -> Done".format(self.ind))
        
        
        
    def penalties(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Penalties".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if play.penalty.isPenalty is False:
                    continue
            
                penaltyyards  = self.py.findPenaltyYards(play.text)
                nextYards     = drivePlay.nextDiffYards
                if isinstance(play, noplay):
                    if play.yds.yards == 0 and penaltyyards is not None:
                        play.yds.yards = penaltyyards
                    elif play.yds.yards == 0 and penaltyyards is None:
                        play.yds.yards = nextYards
                else:
                    if play.yds.yards is None:
                        play.yds.yards = nextYards
                    else:
                        print("Not sure...")
                        
                if nextYards == 0 and play.yds.yards == 0:
                    penaltyyards = 0
                
                if sum([x in play.text for x in ["Personal Foul", "Unsportsmanlike Conduct", "Face Mask"]]) > 0:
                    if nextYards == 15:
                        penaltyyards = 15
                        play.yds.yards = 0
                    elif nextYards == 15:
                        penaltyyards = -15
                        play.yds.yards = 0
                        
                if nextYards == penaltyyards:
                    if play.yds.yards == 0:
                        play.yds.yards = nextYards
                    
                play.penalty.yards = penaltyyards
                
                
                if nextYards == play.yds.yards and nextYards == penaltyyards:
                    continue
                
                self.logger.debug("{0}Penalty Analysis: Penalty=={1}\tPlay=={2}\tNext=={3}\tYards=={4}\tPYards=={5}\tText=={6}".format(self.ind, play.penalty.isPenalty, play.name, nextYards, play.yds.yards, penaltyyards, play.text))
                
                        
            
        self.logger.debug("{0}Analyzing Penalties -> Done".format(self.ind))
        return gameData