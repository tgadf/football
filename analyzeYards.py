#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:41:19 2019

@author: tgadfort
"""


from debug import debugclass

from playTypes import returnplay, patplay
#from copy import deepcopy, copy

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
## Drive Class
############################################################################################################
class analyzeyards:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        self.sep    = "======================================================"
        
        
    def analyze(self, gameData):
        gameData = self.drive(gameData)
        
        
    def drive(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            detail     = driveData.detail
            headline   = driveData.headline
            print(idr,'\t',headline,'\t',detail)
            for ipl,drivePlay in enumerate(drivePlays):
                possession = drivePlay.possession
                start      = drivePlay.start
                valid      = drivePlay.valid
                play       = drivePlay.play
                
                name       = play.name
                text       = play.text
                
                pa         = play.pa
                keys       = pa.getKeys()
                
                yds        = play.yds
                yards      = yds.yards
                #print('\t',ipl,'\t',valid,'\t',possession.get(),'\t',start.get(),'\t',text)
                
                down   = start.down
                togo   = start.togo
                startY = start.startY
                poss   = possession.start
                print('\t',ipl,'\t',valid,'\t',poss,'\t',down,'\t',togo,'\t',startY,'\t',name,'\t',yards,'\t',keys,'\t',text)