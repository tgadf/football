import sys
from footballPlays import *

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
        

class possessionclass:
    def __init__(self, players):
        self.name = "possession"
        self.players = players
        
    
    ########################################################################################################
    ##
    ## Determine Play Possession
    ##
    ########################################################################################################
    def determinePossession(self, play, debug=False):
        txt   = play.text

        if debug:
            fname = sys._getframe().f_code.co_name
            print("\tFUNC {0}({1}): {2}".format(fname, txt, play.name))
        
        
        ## Create empty object
        poss     = playpossessionclass(start=None, end=None, text=txt)
        name     = None
        position = None
        

        ## Kickoff
        if isinstance(play, kickoffplay):
            poss.start,name,position = self.players.getKickingTeam(txt, debug)
            if poss.start is None:
                poss.setUnknownStart()

        ## Field Goal
        if isinstance(play, fieldgoalplay):
            poss.start,name,position = self.players.getFGKickingTeam(txt, debug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Punt
        if isinstance(play, puntplay):
            poss.start,name,position = self.players.getPuntingTeam(txt, debug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Passing
        if isinstance(play, passingplay):
            poss.start,name,position = self.players.getPassingTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getReceivingTeam(txt, debug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Sack
        if isinstance(play, sackplay):
            poss.start,name,position = self.players.getSackedTeam(txt, debug)
            if poss.start is None:
                poss.setPreviousStart()

        ## Running
        if isinstance(play, rushingplay):
            poss.start,name,position = self.players.getRunningTeam(txt, debug)
            if poss.start is None:
                poss.setPreviousStart()
            
        ## Safety
        if isinstance(play, safetyplay):
            if poss.start is None:
                poss.start,name,position = self.players.getPassingTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getRunningTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getPuntingTeam(txt, debug)
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
                poss.start,name,position = self.players.getPassingTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getRunningTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getPuntingTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getFGKickingTeam(txt, debug)
            if poss.start is None:
                poss.start,name,position = self.players.getKickingTeam(txt, debug)
            if poss.start is None:
                poss.setUnknownStart()

        ## Fumble (?)
        if isinstance(play, fumbleplay):
            poss.setUnknownStart()

        ## TBD (?)
        if isinstance(play, tbdplay):
            poss.setUnknownStart()
            
        poss.setPlayer(name)
        poss.setPosition(position)
        
        if debug:
            print("\tResult: {0: <15}  Team: {1: <10}  Name: {2: <25}  Position: {3: <8}  Txt: {4}".format(play.name, str(poss.start), str(name),str(position), txt))
        
        return poss
        