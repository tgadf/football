#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:29:44 2019

@author: tgadfort
"""

from debug import debugclass

from playTypes import returnplay, kickoffplay, patplay, playtype, playsummary
from possession import playpossession
#from copy import deepcopy, copy

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
## Drive Class
############################################################################################################
class analyzekicking:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        self.sep    = "======================================================"
        
        self.dc = debugclass()
        self.pt = playtype()
        
        
    def getKickoffPlays(self, drivePlays):
        for ipl,drivePlay in enumerate(drivePlays):
            kickplay = drivePlay
            if isinstance(kickplay.play, kickoffplay):
                try:
                    retplay = drivePlays[ipl+1]
                    if not isinstance(retplay.play, returnplay):
                        self.logger.debug("{0}    Play after kickoff is not a return: {1}".format(self.ind, retplay.play.text))
                        return None
                except:
                    self.logger.debug("{0}  Could not get return play after kickoff play".format(self.ind))
                    return None
                
                try:
                    genplay = drivePlays[ipl+2]
                except:
                    self.logger.debug("{0}  Could not get 1st offensive play after kickoff play".format(self.ind))
                    return None
                
                return [kickplay, retplay, genplay]
        
        return None
    
    
    
    def isKickoffReturnForTD(self, kickplay, retplay, genplay):
        if isinstance(genplay.play, patplay):
            self.logger.debug("{0}  Kickoff return was a touchdown".format(self.ind))
            if retplay.play.pa.getKey("touchdown") is None:
                self.logger.debug("{0}  Setting kickoff return touchdown".format(self.ind))
                retplay.play.pa.touchdown = True
            genplay.start.startY = 0
            genplay.start.side = kickplay.possession.start
            genplay.start.setYards(genplay.possession.start)
            self.logger.debug("{0}  Setting final PAT play yard lines".format(self.ind))
                
        return kickplay, retplay, genplay
        
    
    def isKickoffOoB(self, kickplay, retplay, genplay):
        if not isinstance(genplay.play, patplay):
            distFromEndZone = genplay.start.distFromOwnEndZone
            if distFromEndZone == 35:
                returnYards = retplay.play.yds.yards
                kickYards = kickplay.play.yds.yards
                if returnYards == 0 and kickYards < 65:
                    self.logger.debug("{0}  Kickoff was out of bounds".format(self.ind))
                    kickplay.play.pa.outofbounds = True      
                    retplay.play.yds.yards = 35
        
        return kickplay, retplay, genplay
        
    
    def isKickoffRegular(self, kickplay, retplay, genplay):
        if not isinstance(genplay.play, patplay):
            returnYards = retplay.play.yds.yards
            kickYards = kickplay.play.yds.yards
            distFromEndZone = genplay.start.distFromOwnEndZone
            
            ## Assume kickoff from 35 yard line
            ## ex
            ##   start at 35 (65)
            ##   kick at 63 to endzone
            ##   return of 17 yards
            ##   start at 19
            
            if kickplay.play.pa.getKey("outofbounds") is True:
                self.logger.debug("{0}  Kickoff was out of bounds. Assuming regular kickoff from 35 yard line".format(self.ind))
                kickplay.start.startY = 35
                kickplay.start.setYards(kickplay.possession.start)
                return kickplay
                
            
            startLine = 100 - (kickYards + (distFromEndZone - returnYards))
            if abs(startLine - 35) <= 1:
                kickplay.start.startY = 35
                self.logger.debug("{0}  Kickoff was regular and setting start to 35 yard line".format(self.ind))
            else:
                kickplay.start.startY = startLine
                self.logger.debug("{0}  Kickoff was irregular and setting start to {1} yard line".format(self.ind, startLine))
            kickplay.start.setYards(kickplay.possession.start)
        else:
            returnYards = retplay.play.yds.yards
            startLine   = 100 - returnYards
            kickplay.start.startY = startLine
            kickplay.start.side = kickplay.possession.start
            kickplay.start.setYards(kickplay.possession.start)
            self.logger.debug("{0}  Kickoff resulted in a touchdown.".format(self.ind, startLine))
            
            
        return kickplay
        
        
    def kickoffs(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Kickoff".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            
            retval = self.getKickoffPlays(drivePlays)
            if retval is None:
                continue
            try:
                kickplay, retplay, genplay = retval
            except:
                raise ValueError("Could not parse return value: {0}".format(retval))
                
            
            kickplay.start.side = kickplay.possession.start
            
            self.logger.debug("{0}Kickoff Analysis: KickYards=={1}\tReturnYards=={2}\tStart=={3}\tText=={4}".format(self.ind, kickplay.play.yds.yards, retplay.play.yds.yards, genplay.start.distFromOwnEndZone, genplay.play.text))
            
            ### Check for TD and set yards
            kickplay, retplay, genplay = self.isKickoffReturnForTD(kickplay, retplay, genplay)
            
            genplay.start.setYards(genplay.possession.start)
            
            ### Check for kickoff out of bounds
            kickplay, retplay, genplay = self.isKickoffOoB(kickplay, retplay, genplay)
            
            ### Check for a regular kickoff (@ the 35 yard line)
            kickplay = self.isKickoffRegular(kickplay, retplay, genplay)
            
            kickplay.start.setYards(kickplay.possession.start)
            
            self.logger.debug("{0}Kickoff Analysis: KickYards=={1}\tReturnYards=={2}\tStart=={3}\tText=={4}".format(self.ind, kickplay.play.yds.yards, retplay.play.yds.yards, genplay.start.distFromOwnEndZone, genplay.play.text))

                    
        self.logger.debug("{0}Analyzing Kickoff -> Done".format(self.ind))
        return gameData
    
    
    
        
        
    def returns(self, gameData):
        self.logger.debug("\n{0}".format(2*self.sep))
        self.logger.debug("{0}Analyzing Kickoff Returns".format(self.ind))
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            
            retval = self.getKickoffPlays(drivePlays)
            if retval is None:
                continue
            try:
                kickplay, retplay, genplay = retval
            except:
                raise ValueError("Could not parse return value: {0}".format(retval))
                
            self.dc.showDrive(driveData, idr)
                
            ### Get starting place
            startingLine = kickplay.start.distToEndZone
            kickingYards = kickplay.play.yds.yards
            
            self.logger.debug("{0}  Starting/Kicking -> {1} {2}".format(self.ind, startingLine, kickingYards))
            
            ### Set starting line
            returnStart = startingLine - kickingYards
            if returnStart < 65:
                retplay.start.side   = retplay.possession.start
                retplay.start.startY = returnStart
            else:
                raise ValueError("Not sure what to do about this kickoff!!!")
            
            if kickplay.play.pa.getKey("outofbounds") is True:
                retplay.play.yds.yards = None
                oobplay = self.pt.getPlay("Penalty: Kickoff Out of Bounds")                
                oobposs = playpossession(start=kickplay.possession.start, end=None, text=oobplay.text)
                oobstart = kickplay.start.copy()
                oobstart.startY = 35
                playResult = playsummary(possession=oobposs, start=oobstart, play=oobplay, valid=True)       
                playResult.start.setYards(playResult.possession.start)                
                drivePlays.insert(1, playResult)
                
                noretplay = self.pt.getPlay("Post Penalty: Starting at 35 yard line")
                noretplay.yds.yards = 0
                noretposs = playpossession(start=retplay.possession.start, end=None, text=noretplay.text)
                noretstart = retplay.start.copy()
                noretstart.startY = 35
                playResult = playsummary(possession=noretposs, start=noretstart, play=noretplay, valid=True)
                playResult.start.setYards(playResult.possession.start)

                drivePlays.pop(2) ## get rid of old return play
                drivePlays.insert(2, playResult) ## insert new return play of zero yards

                        
            self.dc.showDrive(driveData, idr)
            
        self.logger.debug("{0}Analyzing Kickoff Returns -> Done".format(self.ind))
        return gameData