import sys
from debug import debugclass
from possession import playpossessionclass, mixedpossession
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
            
        fout=None
        if fout is not None:
            f = open(fout, "w")
            
        gameData = self.splitKickoff(gameData, players, copMap, debug=debug)
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitPunt(gameData, players, copMap, debug=debug)
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitInterception(gameData, players, copMap, debug=debug)        
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitSafety(gameData, players, copMap, debug=debug)        
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitFieldGoal(gameData, players, copMap, debug=debug)        
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitFumble(gameData, players, copMap, debug=True)            
        self.dc.showGame(gameData, fout=fout, debug=debug)

        gameData = self.splitTouchdown(gameData, players, copMap, debug=debug)        
        self.dc.showGame(gameData, fout=fout, debug=debug)
        
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
                    if debug:
                        print("\tSplitting Kickoff: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
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
                    if playData.play.pa.getKey("forced") is not None and not playData.possession.isKnownStart():
                        if debug:
                            print("\tUsing previous kickoff data to set possession to {0}".format(playData.play.pa.forced))
                        newPossession.start = playData.play.pa.forced
                        try:
                            playData.possession.start = copMap[playData.possession.start]
                        except:
                            playData.possession.setPreviousStart()
                        
                        playData.play.pa.forced = False
                    else:
                        try:
                            newPossession.start = copMap[playData.possession.start]
                        except:
                            newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tKickoff Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break
                    
        return gameData
    
        
    ######################################################
    ## Split play into [punt] + [return + X]
    ######################################################
    def splitPunt(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        lastPoss = None
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
                    
                    if debug:
                        print("\tSplitting Punt: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.puntplay = False
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    
                    playData = mixposs.determinePunt(playData, drivePlays, dp, debug=False)
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    if debug:
                        print("\tPunt Return: {0} --> {1}".format(playData.possession.start, newPossession.start))
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    
                    ## Check if the first play of the next drive is unknown
                    try:
                        if not gameData[idr+1].plays[0].possession.isKnownStart():
                            if debug:
                                print("Setting 1st play of next drive to {0}".format(newPossession.start))
                            gameData[idr+1].plays[0].possession.start = newPossession.start
                    except:
                        pass
                    break
                    
        lastPoss = None
        return gameData
    
        
    ######################################################
    ## Split play into [interception] + [return + X]
    ######################################################
    def splitInterception(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, passingplay) and playData.play.pa.getKey("interception"):
                    if debug:
                        print("\tSplitting Interception: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.passingplay  = False
                    newReturnPlay.pa.touchdown    = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble       = playData.play.pa.fumble
                    newReturnPlay.pa.runback      = playData.play.pa.runback
                    newReturnPlay.pa.interception = False
                    playData.play.pa.touchdown    = False
                    playData.play.pa.fumble       = False
                    playData.play.pa.runback      = False
                    
                    playData = mixposs.determineInterception(playData, drivePlays, dp, debug=debug)
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
                    
        return gameData

        
        
    ######################################################
    ## Split play into [field goal] + [return + X]
    ######################################################
    def splitFieldGoal(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, fieldgoalplay) and playData.play.pa.getKey("blocked"):
                    if debug:
                        print("\tSplitting Field Goal: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.touchdown   = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble      = playData.play.pa.fumble
                    newReturnPlay.pa.runback     = playData.play.pa.runback
                    newReturnPlay.pa.blocked     = False
                    playData.play.pa.touchdown   = False
                    playData.play.pa.fumble      = False
                    playData.play.pa.runback     = False
                    
                    
                    playData = mixposs.determineFieldGoal(playData, drivePlays, dp, debug=debug)
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
                elif isinstance(playData.play, fieldgoalplay):
                    try:
                        if not gameData[idr+1].plays[0].possession.isKnownStart():
                            if debug:
                                print("Setting 1st play of next drive to {0}".format(newPossession.start))
                            gameData[idr+1].plays[0].possession.start = newPossession.start
                    except:
                        pass
                    
        return gameData




    ######################################################
    ## Split play into [safety] + [return + X]
    ######################################################
    def splitSafety(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if isinstance(playData.play, safetyplay) or playData.play.pa.getKey("safety"):
                    if debug:
                        print("\tSplitting Safety: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
                    playData.play.pa.safetypts = False

                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.safety    = False
                    newReturnPlay.pa.safetypts = True

                    playData = mixposs.determineSafety(playData, drivePlays, dp, debug=debug)
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)
                    try:
                        newPossession.start = copMap[playData.possession.start]
                    except:
                        newPossession.start = playData.possession.setUnknownStart()
                    newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                    drivePlays.insert(dp+1, newPlayData)
                    break
                    
        return gameData

        
    ######################################################
    ## Split play into [fumble] + [return + X]
    ######################################################
    def splitFumble(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("fumble") is True:
                    if debug:
                        print("\tSplitting Fumble: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))
                        
                    lostFumble = True
                    try:
                        if playData.possession.start == drivePlays[dp+1].possession.start and drivePlays[dp+1].valid is True:
                            lostFumble = False
                    except:
                        lostFumble = True
                    
                    newReturnPlay  = returnplay(text=playData.play.text)
                    newReturnPlay.analyze()
                    newReturnPlay.pa.touchdown    = playData.play.pa.touchdown
                    newReturnPlay.pa.fumble       = False
                    newReturnPlay.pa.runback      = playData.play.pa.runback
                    playData.play.pa.touchdown    = False
                    playData.play.pa.runback      = False
                    playData.play.pa.fumblereturn = False

                    playData = mixposs.determineFumble(playData, drivePlays, dp, debug=False)
                    newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)   
                    

                        
                    if playData.play.pa.getKey("forced") is not None:
                        if debug:
                            print("\tUsing previous fumble data to set possession to {0}".format(playData.play.pa.forced))
                        newPossession.start = playData.play.pa.forced
                        try:
                            playData.possession.start = copMap[playData.possession.start]
                        except:
                            playData.possession.setPreviousStart()
                        
                        playData.play.pa.forced = False
                    else:
                        if debug:
                            print("\tResult of a lost fumble is {0}".format(lostFumble))


                        if lostFumble:
                            try:
                                newPossession.start = copMap[playData.possession.start]
                            except:
                                newPossession.setPreviousStart()
                        else:
                            newPossession.start = playData.possession.start

                        
                    if debug:
                        print("\tOld possession is {0}".format(playData.possession.start))
                        print("\tNew possession is {0}".format(newPossession.start))


                    gameData[idr].plays[dp] = playData
                    if lostFumble:
                        newPlayData = playclass(possession=newPossession, start=playData.start, play=newReturnPlay, valid=playData.valid)
                        drivePlays.insert(dp+1, newPlayData)
                        break
                    
        return gameData




    ######################################################
    ## Split play into [TD] + [PAT + X]
    ######################################################
    def splitTouchdown(self, gameData, players, copMap, debug=False):
        if debug:
            fname = sys._getframe().f_code.co_name
            print("FUNC {0}".format(fname))
            
        mixposs = mixedpossession()
        for idr in range(len(gameData)):
            drivePlays  = gameData[idr].plays
            for dp in range(len(drivePlays)):
                playData  = drivePlays[dp]
                if playData.valid is not True:
                    continue
                if playData.play.pa.getKey("touchdown") is True:
                    if debug:
                        print("\tSplitting Touchdown: Drive {0}, Play {1}, and Text {2}".format(idr,dp,playData.play.text))

                    playData = mixposs.determineTouchdown(playData, drivePlays, dp, debug=False)
                    if sum([isinstance(x.play, patplay) for x in drivePlays]) > 0:
                        break
                    playData.play.pa.addPAT()
                    if playData.play.pa.getKey("addpat") is True:
                        playData.play.pa.addpat = False
                       
                        
                        ## Split Depends on Offense vs Defense PAT
                        if playData.play.pa.getKey("defpat"):
                            newPATPlay  = patplay(text=playData.play.text)
                            newPATPlay.analyze()
                            newPATPlay.pa.touchdown   = False
                            newPATPlay.pa.runback     = playData.play.pa.runback
                            playData.play.pa.runback  = False
                                     
                            newPossession = playpossessionclass(start=None, end=None, text=playData.play.text)         
                            try:
                                newPossession.start = copMap[playData.possession.start]
                            except:
                                newPossession.start = playData.possession.setUnknownStart()
                        
                            if debug:
                                print("\tThis is a DEF PAT with POSS =",newPossession.start)
                            newPlayData = playclass(possession=newPossession, start=playData.start, play=newPATPlay, valid=playData.valid)
                        else:
                            newPATPlay  = patplay(text=playData.play.text)
                            newPATPlay.analyze()
                            newPATPlay.pa.touchdown   = False
                            newPATPlay.pa.runback     = playData.play.pa.runback
                            
                            playData.play.pa.runback  = False
                            if debug:
                                print("\tThis is a regular PAT with POSS =",playData.possession.start)

                            newPlayData = playclass(possession=playData.possession, start=playData.start, play=newPATPlay, valid=playData.valid)
                        drivePlays.insert(dp+1, newPlayData)
                        break
                    
        return gameData