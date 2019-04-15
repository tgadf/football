import sys
from footballPlays import playtype, footballplay, penaltyplay, puntplay, kickoffplay, fieldgoalplay
from footballPlays import patplay, returnplay, downsplay, tbdplay, noplay, safetyplay
from footballPlays import timeoutplay, endplay, beginplay, sackplay, rushingplay, passingplay, fumbleplay, touchdownplay


class playpossessionclass:
    def __init__(self, start, end, text=None):
        self.start = start
        self.end   = end
        
        self.text  = text
        
        self.valid = True
        
        self.prev    = "PREV"
        self.unknown = "UNK"
        
        self.player     = None
        self.position   = None
        
        self.turnover = False
        self.forced   = None
        
    def setPlayer(self, name):
        self.player = name
        
    def setPosition(self, position):
        self.position
        
    def isPreviousStart(self):
        return self.start == self.prev
        
    def setPreviousStart(self):
        self.start  = self.prev
        
    def isUnknownStart(self):
        return self.start == self.unknown
        
    def setUnknownStart(self):
        self.start  = self.unknown
        
    def isKnownStart(self):
        if self.isPreviousStart() or self.isUnknownStart() or self.start is None:
            return False
        return True
        
    def isForced(self):
        return self.forced
    
        
class mixedpossession:
    def __init__(self):
        self.name = "mixposs"
        
    def determineFumble(self, playData, drivePlays, playNo, debug=False):        
        if debug:
            print("  Determine Fumbling Team Possession. Currently:",playData.possession.start)
            
        if not playData.possession.isKnownStart():
            if debug:
                print("    Trying previous play")
            try:
                prevPlay = drivePlays[playNo-1]
                if prevPlay.possession.isKnownStart():
                    playData.possession.start = prevPlay.possession.start
                    if debug:
                        print("  Setting current possession to {0} because previous play was a {1}".format(playData.possession.start, prevPlay.play.name))
                else:
                    if debug:
                        print("  Not using previous play because possession is not set.")
            except:
                if debug:
                    print("Could not access previous play")
                pass
            
            
        if not playData.possession.isKnownStart():
            if debug:
                print("    Trying next previous play")
            try:
                prevPlay = drivePlays[playNo-2]
                if prevPlay.possession.isKnownStart():
                    playData.possession.start = prevPlay.possession.start
                    if debug:
                        print("  Setting current possession to {0} because two plays ago play was a {1}".format(playData.possession.start, prevPlay.play.name))
                else:
                    if debug:
                        print("  Not using next previous play possession is not set.")
            except:
                if debug:
                    print("Could not access next previous play")
                pass
            
            
        if not playData.possession.isKnownStart():
            if debug:
                print("    Trying next-next previous play")
            try:
                prevPlay = drivePlays[playNo-3]
                if prevPlay.possession.isKnownStart():
                    playData.possession.start = prevPlay.possession.start
                    if debug:
                        print("  Setting current possession to {0} because three plays ago play was a {1}".format(playData.possession.start, prevPlay.play.name))
                else:
                    if debug:
                        print("  Not using next-next previous play possession is not set.")
            except:
                if debug:
                    print("Could not access next-next previous play")
                pass
            
        return playData
    

        
    def determinePunt(self, playData, drivePlays, playNo, debug=False):
        return self.determineFumble(playData, drivePlays, playNo, debug)
    
    def determineSafety(self, playData, drivePlays, playNo, debug=False):
        return self.determineFumble(playData, drivePlays, playNo, debug)
        
    def determineInterception(self, playData, drivePlays, playNo, debug=False):   
        return self.determineFumble(playData, drivePlays, playNo, debug)
        
    def determineTouchdown(self, playData, drivePlays, playNo, debug=False):   
        return self.determineFumble(playData, drivePlays, playNo, debug)
        
    def determineFieldGoal(self, playData, drivePlays, playNo, debug=False):   
        return self.determineFumble(playData, drivePlays, playNo, debug)
        
                        
        

class possessionclass:
    def __init__(self, players):
        self.name = "possession"
        self.players = players
        
    
    ########################################################################################################
    ##
    ## Determine Play Possession
    ##
    ########################################################################################################
    def determinePossession(self, play, debug=False, verydebug=False):
        txt   = play.text

        debug=False
        if verydebug:
            fname = sys._getframe().f_code.co_name
            print("    FUNC {0}({1}): {2}".format(fname, txt, play.name))
        
        
        ## Check for TD
        isTD = False
        if play.pa.getKey("touchdown"):
            isTD = True
        
        ## Check for fumble
        isFumble = False
        if play.pa.getKey("fumble"):
            isFumble = True
        
        ## Create empty object
        poss     = playpossessionclass(start=None, end=None, text=txt)
        name     = None
        position = None
        

        ## Kickoff
        if isinstance(play, kickoffplay):
            poss.start,name,position = self.players.getKickingTeam(txt, debug, verydebug)
            if isTD:
                start,name,position = self.players.getPATKickingTeam(txt, debug, verydebug)
                if start is not None:
                    print("  Found recovering team: {0}".format(poss.start))
                    poss.forced = start                
            if poss.start is None:
                poss.setPreviousStart()

        ## Field Goal
        if isinstance(play, fieldgoalplay):
            poss.start,name,position = self.players.getFGKickingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Punt
        if isinstance(play, puntplay):
            poss.start,name,position = self.players.getPuntingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Passing
        if isinstance(play, passingplay):
            poss.start,name,position = self.players.getPassingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getReceivingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Sack
        if isinstance(play, sackplay):
            poss.start,name,position = self.players.getSackedTeam(txt, debug, verydebug)
            if isFumble:
                start,name,position = self.players.getPATKickingTeam(txt, debug, verydebug)
                if start is not None:
                    print("  Found recovering team: {0}".format(start))
                    poss.forced = start
            if poss.start is None:
                poss.setPreviousStart()

        ## Running
        if isinstance(play, rushingplay):
            poss.start,name,position = self.players.getRunningTeam(txt, debug, verydebug)
            if isFumble:
                poss.start,name,position = self.players.getPATKickingTeam(txt, debug, verydebug)
                if poss.start is not None:
                    print("  Found recovering team: {0}".format(poss.start))
                    poss.forced = poss.start                
            if poss.start is None:
                poss.setPreviousStart()
            
        ## Safety
        if isinstance(play, safetyplay):
            if poss.start is None:
                poss.start,name,position = self.players.getPassingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getRunningTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getPuntingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Penalty/Timeout/End
        if isinstance(play, penaltyplay):
            poss.setPreviousStart()
            
        ## Empty play
        if isinstance(play, (endplay, timeoutplay)):
            poss.setPreviousStart()
            poss.valid=False
                     
        ## PAT
        if isinstance(play, patplay):
            poss.setPreviousStart()
                
        ############################################
        # Unclear...
        ############################################

        ## Touchdown
        if isinstance(play, touchdownplay):
            if poss.start is None:
                poss.start,name,position = self.players.getPassingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getRunningTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getPuntingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getFGKickingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.start,name,position = self.players.getKickingTeam(txt, debug, verydebug)
            if poss.start is None:
                poss.setUnknownStart()

        ## Fumble (?)
        if isinstance(play, fumbleplay):
            if poss.start is None:
                poss.start,name,position = self.players.getPATKickingTeam(txt, debug, verydebug)
                if poss.start is not None:
                    print("  Found recovering team: {0}".format(poss.start))
                    poss.forced = poss.start
            if poss.start is None:
                poss.setUnknownStart()

        ## TBD (?)
        if isinstance(play, tbdplay):
            poss.setUnknownStart()
            
        poss.setPlayer(name)
        poss.setPosition(position)
        
        if verydebug:
            print("\tResult: {0: <15}  Team: {1: <10}  Name: {2: <25}  Position: {3: <8}  Txt: {4}".format(play.name, str(poss.start), str(name),str(position), txt))
        
        return poss
        