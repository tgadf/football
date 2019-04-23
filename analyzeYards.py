#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:41:19 2019

@author: tgadfort
"""


from debug import debugclass

from playTypes import returnplay, kickoffplay, puntplay, passingplay
from playTypes import beginplay,endplay,timeoutplay,noplay,tbdplay,patplay
from playYards import playyards
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
        
        self.py = playyards()
        
        
    def analyze(self, gameData):
        gameData = self.kickoff(gameData)
        gameData = self.punt(gameData)
        gameData = self.genreturn(gameData)   
        gameData = self.kickreturn(gameData)   
        gameData = self.penalty(gameData)       
        gameData = self.noplays(gameData)       
        gameData = self.pat(gameData)
        #gameData = self.drive(gameData)
        
        return gameData
        
        
    def kickoff(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Kickoff Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, kickoffplay):
                    play.yds.yards = self.py.findKickoffYards(play.text)
                    self.logger.info("{0}  Setting Kickoff Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))

        return gameData
        
        
    def punt(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Punt Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, puntplay):                    
                    play.yds.yards = self.py.findPuntYards(play.text)
                    self.logger.info("{0}  Setting Punt Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))

        return gameData
        
        
    def kickreturn(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Kick Return Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, returnplay):
                    try:
                        if not isinstance(drivePlays[ipl-1].play, (puntplay, kickoffplay)):
                            continue
                    except:
                        continue
                    
                    play.yds.yards = self.py.findKickReturnYards(play.text)
                    self.logger.info("{0}  Setting Kick Return Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))

        return gameData
        
        
    def genreturn(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Return Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, returnplay):
                    play.yds.yards = self.py.findKickReturnYards(play.text)
                    self.logger.info("{0}  Setting Return Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))
                    
                    try:
                        prevPlay   = drivePlays[ipl-1].play
                        if isinstance(prevPlay, passingplay):
                            drivePlays[ipl-1].play.yds.yards = 0
                    except:
                        pass

        return gameData
        
        
    def penalty(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Penalty Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                return gameData
                print("STOP HERE")
#                
#                if isinstance(play, penaltyplay):
#                    yards = self.py.findPenaltyYards(play.text)
#                    if yards is not None and isinstance(yards, int):
#                        play.yds.yards = yards
#                        self.logger.info("{0}  Setting Penalty Yards (based on text) to {1}: {2}".format(self.ind, play.yds.yards, play.text))
#
#        for idr,driveData in enumerate(gameData):
#            drivePlays = driveData.plays
#            for ipl,drivePlay in enumerate(drivePlays):
#                play = drivePlay.play
#                if isinstance(play, penaltyplay):
#                    if play.yds.yards is None:
#                        try:
#                            nextPlay   = drivePlays[ipl+1]
#                            nextStart  = nextPlay.start                            
#                            nextStartY = nextStart.startY
#                            nextSide   = nextStart.side
#                            
#                            currStart  = drivePlay.start                            
#                            currStartY = currStart.startY
#                            currSide   = currStart.side
#                            currPoss   = drivePlay.possession.start
#                            
#                            if currSide == nextSide:
#                                if currPoss == currSide:
#                                    ## Yard Markers are increasing
#                                    yards = nextStartY - currStartY
#                                else:
#                                    ## Yard Markers are decreasing
#                                    yards = currStartY - nextStartY
#                            else:
#                                yards = (100-nextStartY) - currStartY
#                                         
#                            play.yds.yards = yards
#                            self.logger.info("{0}  Setting Penalty Yards for {1} (based on current {2}-{3} and next {4}-{5}) to {6}: {7}".format(self.ind, currPoss, currStartY, currSide, nextStartY, nextSide, play.yds.yards, play.text))
#                        except:
#                            self.logger.info("{0}  Could not set penalty yards: {1}".format(self.ind, play.text))
#                            

        return gameData
        
        
    def noplays(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing Penalty Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, (beginplay,endplay,timeoutplay,noplay,tbdplay)):
                    play.yds.yards = 0
                    self.logger.info("{0}  Setting No Play Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))
                    
                    try:
                        nextPlayStart = drivePlays[ipl+1].start.copy()
                    except:
                        nextPlayStart = None
                        
                    if nextPlayStart is not None:
                        drivePlay.start = nextPlayStart
                    
        return gameData

        
        
    def pat(self, gameData):
        self.logger.info("\n{0}".format(2*self.sep))
        self.logger.info("{0}Analyzing PAT Yards".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                play = drivePlay.play
                if isinstance(play, patplay):
                    play.yds.yards = 0
                    drivePlay.start.startY = 0
                    self.logger.info("{0}  Setting PAT Yards to {1}: {2}".format(self.ind, play.yds.yards, play.text))

        return gameData

        
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
                side   = start.side
                poss   = possession.start

                print('\t',ipl,'\t',valid,'\t',poss,'\t',down,'\t',togo,'\t',startY,'\t',side,'\t{0: <10}\t'.format(name),'\t',yards,'\t',text)
                
                if yards is None:
                    print("\n\tNO YARDS...\n")
                    continue
                
                if startY is None:
                    continue

                try:
                    nextPlay   = drivePlays[ipl+1]
                    nextStart  = nextPlay.start                            
                    nextStartY = nextStart.startY
                    nextSide   = nextStart.side
                    
                    if isinstance(nextPlay.play, returnplay):
                        continue
                    
                    currStartY = startY
                    currSide   = side
                    currPoss   = poss
                    
                    if currPoss == currSide:
                        ## Yard Markers are increasing
                        predStartY = currStartY + yards
                        if predStartY > 50:
                            predStartY = 100 - predStartY
                    else:
                        ## Yard Markers are decreasing
                        predStartY = currStartY - yards
                        if predStartY > 50:
                            predStartY = 100 - predStartY

                    if predStartY != nextStartY:
                        print("\t===>Predicted [{0}] yard line, but observed [{1}]\n".format(predStartY, nextStartY))
                        #print("\tcurrPoss == currSide: {0} == {1}".format(currPoss,currSide))
                except:
                    pass