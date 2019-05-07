import sys
from debug import debugclass
from possession import mixedpossession, playpossession
from playTypes import playsummary
from playTypes import puntplay, kickoffplay, fieldgoalplay
from playTypes import patplay, safetyplay, passingplay, returnplay


# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class possessionchangeclass:
    def __init__(self, copMap):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 2*" "
        
        self.copMap = copMap
        
        self.dc = debugclass()
        
        
    def flipPossession(self, possession):    
        try:
            start = self.copMap[possession.start]
        except:
            start = possession.setUnknownStart()
        return start
    
    
    ################################################################################################################################################################
    ## Change of Possession Plays
    ################################################################################################################################################################
    def splitChangeOfPossession(self, gameData):
        gameData = self.splitKickoff(gameData)

        gameData = self.splitPunt(gameData)

        gameData = self.splitInterception(gameData)

        gameData = self.splitSafety(gameData)

        gameData = self.splitFieldGoal(gameData)

        gameData = self.splitFumble(gameData)

        gameData = self.splitTouchdown(gameData)
                
            
        return gameData
    
        
    ######################################################
    ## Split play into [kick] + [return + X]
    ######################################################
    def splitKickoff(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, kickoffplay):
                    self.logger.debug("{0}  Kickoff Play: {1}".format(self.ind, playData.play.text))
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.kickoffplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    
                    
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)
                    if playData.play.pa.getKey("forced") is not None and not playData.possession.isKnownStart():
                        self.logger.debug("{0}  Using previous kickoff data to set possession to {1}".format(playData.play.pa.forced))
                        newPossession.start = playData.play.pa.forced
                        playData.play.pa.forced = False
                        playData.possession.start = self.flipPossession(newPossession.start)                        
                    else:
                        newPossession.start = self.flipPossession(playData.possession)
                    newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)                    
                    drivePlays.insert(dp+1, newPlayData)
                    
                    newReturnPlay.connectedPlays.append(playData)
                    playData.play.connectedPlays.append(newReturnPlay)
                    
                    changes.append(idr)
                    break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                        
                    
        return gameData
    
        
    ######################################################
    ## Split play into [punt] + [return + X]
    ######################################################
    def splitPunt(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, puntplay):
                    ## Ignore if there is a safety
                    if playData.play.pa.getKey("safety") is True:
                        continue
                    
                    self.logger.debug("{0}  Punt Play: {1}".format(self.ind, playData.play.text))
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.puntplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    
                    playData = mixposs.determinePunt(playData, drivePlays, dp, debug=False)
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)
                    newPossession.start = self.flipPossession(playData.possession)
                    try:
                        newPossession.start = self.copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    
                    newReturnPlay.connectedPlays.append(playData)
                    playData.play.connectedPlays.append(newReturnPlay)

                    changes.append(idr)                    
                    
                    ## Check if the first play of the next drive is unknown
                    try:
                        if not gameData[idr+1].plays[0].possession.isKnownStart():
                            gameData[idr+1].plays[0].possession.start = newPossession.start
                    except:
                        pass
                    break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData
    
        
    ######################################################
    ## Split play into [interception] + [return + X]
    ######################################################
    def splitInterception(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, passingplay) and playData.play.pa.getKey("interception"):
                    self.logger.debug("{0}  Interception Play: {1}".format(self.ind, playData.play.text))
                    
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.passingplay  = False
                    newReturnPlay.pa.touchdown    = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble       = playData.play.pa.fumble
                    newReturnPlay.pa.runback      = playData.play.pa.runback
                    newReturnPlay.pa.interception = False
                    playData.play.pa.touchdown    = False
                    playData.play.pa.fumble       = False
                    playData.play.pa.runback      = False
                    
                    playData = mixposs.determineInterception(playData, drivePlays, dp)
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = self.copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    
                    newReturnPlay.connectedPlays.append(playData)
                    playData.play.connectedPlays.append(newReturnPlay)

                    changes.append(idr)
                    break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData

        
        
    ######################################################
    ## Split play into [field goal] + [return + X]
    ######################################################
    def splitFieldGoal(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, fieldgoalplay) and playData.play.pa.getKey("blocked"):
                    self.logger.debug("{0}  Field Goal Play: {1}".format(self.ind, playData.play.text))
                    
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    newReturnPlay.pa.blocked     = False
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    
                    
                    playData = mixposs.determineFieldGoal(playData, drivePlays, dp)
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = self.copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    
                    newReturnPlay.connectedPlays.append(playData)
                    playData.connectedPlays.append(newReturnPlay)
                    
                    changes.append(idr)
                    break
                elif isinstance(playData.play, fieldgoalplay):
                    changes.append(idr)
                    try:
                        if not gameData[idr+1].plays[0].possession.isKnownStart():
                            gameData[idr+1].plays[0].possession.start = newPossession.start
                    except:
                        pass

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData




    ######################################################
    ## Split play into [safety] + [return + X]
    ######################################################
    def splitSafety(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, safetyplay) or playData.play.pa.getKey("safety"):
                    self.logger.debug("{0}  Safety Play: {1}".format(self.ind, playData.play.text))
                    playData.play.pa.safetypts = False

                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.safety    = False
                    newReturnPlay.pa.safetypts = True

                    playData = mixposs.determineSafety(playData, drivePlays, dp)
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = self.copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    
                    newReturnPlay.connectedPlays.append(playData)
                    playData.play.connectedPlays.append(newReturnPlay)
                    
                    changes.append(idr)
                    break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData

        
    ######################################################
    ## Split play into [fumble] + [return + X]
    ######################################################
    def splitFumble(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
                        
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("fumble") is True:
                    self.logger.debug("{0}  Fumble Play: {1}".format(self.ind, playData.play.text))
                        
                    lostFumble = True
                    try:
                        if playData.possession.start == drivePlays[dp+1].possession.start and drivePlays[dp+1].valid is True:
                            lostFumble = False
                    except:
                        lostFumble = True
                    
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.pa.touchdown    = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble       = False
                    newReturnPlay.pa.runback      = playData.play.pa.runback
                    playData.play.pa.touchdown    = False
                    playData.play.pa.runback      = False
                    playData.play.pa.fumblereturn = False

                    playData = mixposs.determineFumble(playData, drivePlays, dp, debug=False)
                    newPossession = playpossession(start=None, end=None, text=playData.play.text)   
                    

                        
                    if playData.play.pa.getKey("forced") is not None:
                        self.logger.debug("{0}Using previous fumble data to set possession to {1}".format(self.ind, playData.play.pa.forced))
                        newPossession.start = playData.play.pa.forced
                        try:
                            playData.possession.start = self.copMap[playData.possession.start]
                        except:
                            playData.possession.setPreviousStart()
                        
                        playData.play.pa.forced = False
                    else:
                        self.logger.debug("{0}Result of a lost fumble is {1}".format(self.ind, lostFumble))


                        if lostFumble:
                            try:
                                newPossession.start = self.copMap[playData.possession.start]
                            except:
                                newPossession.setPreviousStart()
                        else:
                            newPossession.start = playData.possession.start

                        
                    self.logger.debug("{0}Fumble Old possession is {1}".format(self.ind, playData.possession.start))
                    self.logger.debug("{0}Fumble New possession is {1}".format(self.ind, newPossession.start))

                    changes.append(idr)
                    gameData[idr].plays[dp] = playData
                    if lostFumble:
                        newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newReturnPlay, valid=playData.valid)
                        
                        newReturnPlay.connectedPlays.append(playData)
                        playData.play.connectedPlays.append(newReturnPlay)
                    
                        drivePlays.insert(dp+1, newPlayData)                        
                        break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
        return gameData




    ######################################################
    ## Split play into [TD] + [PAT + X]
    ######################################################
    def splitTouchdown(self, gameData):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("\n{0}{1}()".format(self.ind, fname))
        
        changes = []
        
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("touchdown") is True:

                    playData = mixposs.determineTouchdown(playData, drivePlays, dp, debug=False)
                    if sum([isinstance(x.play, patplay) for x in drivePlays]) > 0:
                        break
                    playData.play.pa.addPAT()
                    if playData.play.pa.getKey("addpat") is True:
                        self.logger.debug("{0}  Touchdown Play: {1}".format(self.ind, playData.play.text))
                        playData.play.pa.addpat = False
                       
                        
                        ## Split Depends on Offense vs Defense PAT
                        if playData.play.pa.getKey("defpat"):
                            newPATPlay  = patplay(text=playData.play.text)
                            newPATPlay.pa.touchdown   = False
                            newPATPlay.pa.runback     = playData.play.pa.runback
                            playData.play.pa.runback  = False
                                     
                            newPossession = playpossession(start=None, end=None, text=playData.play.text)         
                            try:
                                newPossession.start = self.copMap[playData.possession.start]
                            except:
                                newPossession.start = playData.possession.setUnknownStart()
                        
                            self.logger.debug("{0}This is a DEF PAT with POSS = {1}".format(self.ind, newPossession.start))
                            newPlayData = playsummary(possession=newPossession, start=playData.start.copy(), play=newPATPlay, valid=playData.valid)
                    
                            newPATPlay.connectedPlays.append(playData)
                            playData.play.connectedPlays.append(newPATPlay)
                    
                            drivePlays.insert(dp+1, newPlayData)
                            changes.append(idr)
                        else:
                            newPATPlay  = patplay(text=playData.play.text)
                            newPATPlay.pa.touchdown   = False
                            newPATPlay.pa.runback     = playData.play.pa.runback
                            playData.play.pa.runback  = False
                                
                            newPossession = playpossession(start=None, end=None, text=playData.play.text)
                            newPossession.start = playData.possession.start
                            
                            self.logger.debug("{0}This is a REGULAR PAT with POSS = {1}".format(self.ind, newPossession.start))
                            newPlayData = playsummary(possession=playData.possession, start=playData.start.copy(), play=newPATPlay, valid=playData.valid)
                            drivePlays.insert(dp+1, newPlayData)
                    
                            newPATPlay.connectedPlays.append(playData)
                            playData.play.connectedPlays.append(newPATPlay)
                    
                            changes.append(idr)
                        break

        self.logger.debug("{0}Found {1} Drives With Splits in {2}()".format(self.ind, len(changes), fname))
        for idr in set(changes):
            self.dc.showDrive(gameData[idr], idr, "Drive {0}".format(idr))
                    
                    
        return gameData