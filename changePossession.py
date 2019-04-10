import sys
from debug import debugclass
from possession import playpossessionclass
from summary import playclass
from footballPlays import *

class possessionchangeclass:
    def __init__(self):
        self.name = "pcc"
        
        self.dc = debugclass()
    
    
    ################################################################################################################################################################
    ## Change of Possession Plays
    ################################################################################################################################################################
    def splitChangeOfPossession(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        self.splitKickoff(gameData, players, copMap, debug=debug)
        self.splitPunt(gameData, players, copMap, debug=debug)
        self.splitInterception(gameData, players, copMap, debug=debug)        
        self.splitSafety(gameData, players, copMap, debug=debug)        
        self.splitFieldGoal(gameData, players, copMap, debug=debug)        
        self.splitFumble(gameData, players, copMap, debug=debug)            
        self.splitTouchdown(gameData, players, copMap, debug=debug)        
        
        self.dc.showGame(gameData)
        #gameData = self.analyzePossession(gameData, players, debug)
        
            
        return gameData
    
        
    ######################################################
    ## Split play into [kick] + [return + X]
    ######################################################
    def splitKickoff(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, kickoffplay):
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.kickoffplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tKickoff Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break
    
        
    ######################################################
    ## Split play into [punt] + [return + X]
    ######################################################
    def splitPunt(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, puntplay):
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.puntplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tPunt Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break
    
        
    ######################################################
    ## Split play into [interception] + [return + X]
    ######################################################
    def splitInterception(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, passingplay) and playData.play.pa.getKey("interception"):
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.passingplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tInterception Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break

        
        
    ######################################################
    ## Split play into [field goal] + [return + X]
    ######################################################
    def splitFieldGoal(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, fieldgoalplay) and playData.play.pa.getKey("blocked"):
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    newReturnPlay.pa.blocked     = False
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tField Goal Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break




    ######################################################
    ## Split play into [safety] + [return + X]
    ######################################################
    def splitSafety(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, safetyplay):
                    playData.pa.safetypts = False

                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.safety    = False
                    newReturnPlay.pa.safetypts = True

                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break

        
    ######################################################
    ## Split play into [fumble] + [return + X]
    ######################################################
    def splitFumble(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("fumble") is True:
                    lostFumble = True
                    try:
                        if playData.possession.start == drivePlays[dp+1].possession.start and drivePlays[dp+1].valid is True:
                            lostFumble = False
                    except:
                        lostFumble = True
                    
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    if lostFumble:
                        newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                        newReturnPlay.pa.fumble      = False
                        newReturnPlay.pa.runback     = playData.play.pa.runback
                        playData.play.pa.touchdown   = False
                        playData.play.pa.runback     = False
                    else:
                        newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                        newReturnPlay.pa.fumble      = False
                        newReturnPlay.pa.runback     = playData.play.pa.runback
                        playData.play.pa.touchdown   = False
                        playData.play.pa.runback     = False

                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)                    
                    if lostFumble:
                        if playData.possession.isPreviousStart():
                            try:
                                playData.possession.start = drivePlays[dp-1].possession.start
                                newPossession.start = copMap[playData.possession.start]
                            except:
                                newPossession.setPreviousStart()
                        elif playData.possession.isUnknownStart():
                            newPossession.setUnknownStart()
                        else:
                            newPossession.start = copMap[playData.possession.start]
                    else:
                        newPossession.start = playData.possession.start
                        
                    gameData[idr].plays[dp] = playData
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break




    ######################################################
    ## Split play into [TD] + [PAT + X]
    ######################################################
    def splitTouchdown(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("touchdown") is True:
                    if sum([isinstance(x.play, patplay) for x in drivePlays]) > 0:
                        break
                    playData.play.pa.addPAT()
                    if playData.play.pa.getKey("addpat") is True:
                        playData.play.pa.addpat = False
                        newPATPlay  = patplay(text=playData.play.text)
                        newPATPlay.analyze()
                        newPATPlay.pa.touchdown   = False
                        newPATPlay.pa.runback     = playData.play.pa.runback
                        playData.play.pa.runback  = False
                        newPlayData = playclass(possession=playData.possession, start=playData.start, play=newPATPlay, valid=playData.valid)
                        drivePlays.insert(dp+1, newPlayData)
                        break