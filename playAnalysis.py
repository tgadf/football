import sys
from playYards import playyards

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class playtextclass:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 8*" "
        
        
    ## Passing
    def getInterception(self):
        return ["interception", "Interception", "intercepted", "Intercepted"]

    def getCompletePass(self):
        return ["complete", "Complete"]
    
    
    ## PAT
    def getPAT(self):
        return self.getOnePtPAT() + self.getTwoPtPAT() + self.getUNKPtPAT() + self.getDefensivePAT()
    
    def getDefensivePAT(self):
        return ["defensive PAT", "Defensive PAT"]
    
    def getOnePtPAT(self):
        retval = []
        vals = ["kick)"]
        for val in vals:
            retval += [val, val.title(), val.upper()]
        retval += [" PAT MISSED)", " PAT blocked)", "(PAT blocked)", "(PAT)", " BLOCKED)"]
        return retval
    
    def getUNKPtPAT(self):
        return ["PAT failed", "Team Extra Point Attempt Failed"]
    
    def getTwoPtPAT(self):
        return ["2 point", " 2 Point", "Two-point", "two-point", "Two-Point", "two pt", "Two pt"]

    
    ## Touchdown
    def getTouchdown(self):
        return ["touchdown", "Touchdown", "TOUCHDOWN", " TD", "TD,", "TD "]
    
    
    ## Fumble
    def getFumble(self):
        return [" fumble", " Fumble", " fumbled", " Fumbled"]
    
    
    ## Penalty
    def getPenalty(self):
        retval = []
        vals = ["ILLEGAL BLOCK", "illegal block"]
        for val in vals:
            retval += [val, val.title(), val.upper()]
        return retval
    
    
    ## Runback (Return)
    def getRunback(self):
        return ["return", "Return", "recovered", "Recovered"]
    
    def getNoRunback(self):
        return ["no return", "No Return"]
    
    
    ## No Play
    def getNoPlay(self):
        return ["NO PLAY", "No Play"]
    
    
    ## Safety
    def getSafety(self):
        return ["SAFETY", "Safety"]
    
    
    ## Touchback
    def getTouchback(self):
        val = "touchback"
        retval = [val, val.title(), val.upper()]
        return retval    
    
    ## Blocked
    def getBlocked(self):
        return [" block", " blocked", "Blocked", "Block", "BLOCKED"]
    
    ## Field Goal
    def getFieldGoal(self):
        return ["Field Goal", "FIELD GOAL", "FG"]
    
    def getFieldGoalMiss(self):
        return [" miss ", " missed", " Missed", "MISSED", "no good", "no good", "No Good", "No good", "NO GOOD", "Failed", "FAILED", "failed"]
    
    def getFieldGoalReturn(self):
        return [" FG RETURNED "]
    
    
    ## Kickoff
    def getKickoff(self):
         return ["kickoff", "Kickoff", "kick off", "Kick Off", "Onside Kick", "Onside kick", "onside kick", "on-side kick", " kick for "]
    
    ## Punt
    def getPunt(self):
        return ["punt", " PUNT", "Punt"]
    
    
class playanalysis:
    def __init__(self, text, playtype):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 8*" "
        
        self.text  = text
        self.yards = None
        
        self.ptc = playtextclass()
        
        self.__dict__[playtype] = True
        self.playtype = playtype
        
        
        py = playyards(text=text, playtype=playtype)
        self.findYards = py.findYards
        
        self.called = {}
    
    
    def setPlayText(self, text):
        self.text = text
    
    
    def getKey(self, key):
        if self.__dict__.get(key) is not None:
            return self.__dict__[key]
        return None
    
    
    def getKeys(self):
        keys = [k for k,v in self.__dict__.items() if v is True]
        return keys
    
    
    def setNoPlay(self):
        if self.getKey("noplay") is True:
            for k in self.__dict__.keys():
                if self.__dict__[k] is True:
                    self.__dict__[k] = False
            self.noplay = True
        
    
    def isScore(self, points=True):
        if self.getKey("noplay") is True:
            if points:
                return 0
            return False
        
        if self.getKey("touchdown") is True:
            if points:
                return 6
            return True
        elif self.getKey("fieldgoal") is True:
            if points:
                return 3
            return True
        elif self.getKey("safetypts") is True:
            if points:
                return 2
            return True
        elif self.getKey("pat") is True:
            if self.getKey("oneptpat") is True:
                if points:
                    return 1
                return True
            elif self.getKey("twoptpat") is True:
                if points:
                    return 2
                return True
            elif self.getKey("defpat") is True:
                if points:
                    return 2
                return True
            else:
                if points:
                    return 0
                return False
        else:
            if points:
                return 0
            return False
                                

    ##################################################
    ## Basic Play
    ##################################################
    def findBasicPlay(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True


        self.fumble    = False
        self.touchdown = False
        self.safety    = False
        self.penalty   = False
        self.runback   = False
        self.noplay    = False


        if sum([x in self.text for x in self.ptc.getTouchdown()]) > 0:
            ## Noted Exceptions
            if self.text.find("TD Moton") != -1:
                self.touchdown = False
            else:
                self.touchdown = True

        if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
            self.touchdown = True
            
        if sum([x in self.text for x in self.ptc.getFumble()]) > 0:
            self.fumble = True
            
        if sum([x in self.text for x in self.ptc.getPenalty()]) > 0:
            self.penalty = True
        
        if sum([x in self.text for x in self.ptc.getRunback()]) > 0:
            self.runback = True
            
        if sum([x in self.text for x in self.ptc.getNoPlay()]) > 0:
            self.noplay = True
        
        if sum([x in self.text for x in self.ptc.getSafety()]) > 0:
            self.safety = True
            
        
    ##################################################
    ## InterceptedPassing Play
    ##################################################
    def findInterceptedPass(self, debug): 
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.interception = False
        if sum([x in self.text for x in self.ptc.getInterception()]) > 0:
            self.interception = True

            if self.touchdown is False:
                if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
                    self.touchdown = True

        
    ##################################################
    ## Intercepted PAT Play
    ##################################################
    def findInterceptedPAT(self, debug):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        try:
            patsubplay = self.play[self.text.rfind("("):self.text.rfind(")")]
            self.interception = False
            if sum([x in patsubplay for x in self.ptc.getInterception()]) > 0:
                self.interception = True
        except:
            if self.getKey("interception") is None:
                self.interception = False
            return
        

    ##################################################
    ## Passing Play
    ##################################################
    def findPassing(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay(debug)
        
        self.complete     = False
        self.interception = False
        
        if sum([x in self.text for x in self.ptc.getCompletePass()]) > 0:
            self.complete = True
                        
        if self.complete is False:
            self.findInterceptedPass(debug)
                    
        
    ##################################################
    ## Rushing Play
    ##################################################
    def findRushing(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay(debug)
                    
        
    ##################################################
    ## Interception Play
    ##################################################
    def findInterception(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay(debug)
        self.findPassing(debug)
        
        ## Check for implied touchdown
        if self.interceptionreturn is True:
            if self.touchdown is False:
                if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
                    self.touchdown = True
                    
        
    ##################################################
    ## Fumble Play
    ##################################################
    def findFumble(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay(debug)
        
        ## Check for implied touchdown
        if self.fumble is True:
            if self.touchdown is False:
                if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
                    self.touchdown = True
        
            
    ##################################################
    ## Basic Kicking
    ##################################################
    def findBasicKicking(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay()
        self.blocked   = False
        self.missed    = False
        self.runback   = False
        self.touchback = False
        self.outofbounds = False
        
        
        if sum([x in self.text for x in self.ptc.getRunback()]) > 0:
            self.runback = True
        
        if sum([x in self.text for x in self.ptc.getNoRunback()]) > 0:
            self.runback = False

        if sum([x in self.text for x in self.ptc.getBlocked()]) > 0:
            if sum([x in self.text for x in self.ptc.getPenalty()]) == 0:
                self.blocked = True

        if sum([x in self.text for x in self.ptc.getTouchback()]) > 0:
            self.touchback = True
            self.runback   = True
            
    
        if sum([x in self.text for x in self.ptc.getFieldGoalMiss()]) > 0:
            self.missed = True
                   
                    
        
    ##################################################
    ## Punt Play
    ##################################################
    def findPunt(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay(debug)
        
        ## Check for implied touchdown
        if self.punt is True:
            if self.touchdown is False:
                if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
                    self.touchdown = True
            
        
    ##################################################
    ## Field Goal Play
    ##################################################
    def findFieldGoal(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicKicking(debug)
        if sum([x in self.text for x in self.ptc.getFieldGoalReturn()]) > 0:
            self.blocked = True

        if self.blocked is True or self.missed is True:
            self.fieldgoaltry = True
            self.fieldgoal    = False
        else:
            self.fieldgoaltry = False
            self.fieldgoal    = True
            
        
        
    ##################################################
    ## PAT Play
    ##################################################
    def addPAT(self, debug=False):
        self.addpat = False
        if self.touchdown is True:
            if sum([x in self.text for x in self.ptc.getPAT()]) > 0:
                self.addpat = True
                self.findPAT(debug)
                
                
    def findPAT(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicKicking(debug)
        self.findInterceptedPAT(debug)
        
        
        ## Check for incorrect blocked assignment
        if self.blocked is True:
            if sum([x in self.text for x in self.ptc.getPunt()]) > 0:
                self.blocked = False
            if sum([x in self.text for x in self.ptc.getFieldGoal()]) > 0:
                self.blocked = False
                
            
        ## Extra Point
        if self.missed is True or self.blocked is True:
            self.oneptpattry = True
            self.oneptpat    = False
        else:
            self.oneptpattry = False
            self.oneptpat    = True

        
        ## Defensive PAT
        self.defpat = False
        if sum([x in self.text for x in self.ptc.getDefensivePAT()]) > 0:
            self.defpat      = True
            self.oneptpat    = False
            self.oneptpattry = True

        
        ## 2-Point
        self.twoptpattry = False
        self.twoptpat    = False
        if sum([x in self.text for x in self.ptc.getTwoPtPAT()]) > 0:
            self.twoptpattry = True
            self.oneptpattry = False
            self.oneptpat    = False
            
            if self.missed is True or self.interception is True:
                self.twoptpat = False
            else:
                self.twoptpat = True
                
        
        ## Interception (from two point)
        if self.interception is True:
            self.twoptpattry = True
            self.twoptpat    = False
            self.oneptpattry = False
            self.oneptpat    = False
            

        ## Sanity check
        self.pat = False
        if sum([self.oneptpat, self.oneptpattry, self.twoptpat, self.twoptpattry, self.defpat]) > 0:
            self.pat = True

            
        
    def findKickoff(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicKicking(debug)
        
        self.touchback = False
        self.onside    = False
        self.recovery  = False
        
        if sum([x in self.text for x in ["onside ", "Onside ", "on-side"]]) > 0:
            self.onside = True

        if sum([x in self.text for x in ["recovered"]]) > 0:
            self.recovery = True

        

    ############################################################################################################
    ## Return Play
    ############################################################################################################
    def findReturn(self, debug=False):
        fname = sys._getframe().f_code.co_name
        if self.called.get(fname) is not None:
            return
        self.called[fname] = True

        self.findBasicPlay()
        
        self.puntreturn         = False
        self.fieldgoalreturn    = False
        self.kickoffreturn      = False
        self.onsidereturn       = False
        self.fumblereturn       = False
        self.interceptionreturn = False

        if self.__dict__.get("punt") is not None:
            if self.punt is True:
                self.puntreturn = True
                self.findPunt()
                
        if self.__dict__.get("kickoff") is not None:
            if self.kickoff is True:
                self.kickoffreturn = True
                
        if self.__dict__.get("onside") is not None:
            if self.onside is True:
                self.onsidereturn = True
                
        if self.__dict__.get("fieldgoal") is not None:
            if self.fieldgoal is True:
                self.fieldgoalreturn = True
                
        if self.__dict__.get("fumble") is not None:
            if self.fumble is True:
                self.fumblereturn = True
                self.findFumble()
                
        if self.__dict__.get("interception") is not None:
            if self.interception is True:
                self.interceptionreturn = True
                self.findInterception()
                

                
        
            
            

    ############################################################################################################
    ## Result of Play
    ############################################################################################################
    def findResult(self, debug=False):
        return self.playtype
        
        self.result = None
        if self.__dict__.get("penalty"):
            if self.penalty is True:
                self.result = "Penalty"
        elif self.__dict__.get("timeout"):
            if self.timeout is True:
                self.result = "Timeout"
        elif self.__dict__.get("end"):
            if self.end is True:
                self.result = "End"
        elif self.__dict__.get("touchdown"):
            if self.touchdown is True:
                self.result = "Touchdown"
        elif self.__dict__.get("madefieldgoal"):
            if self.madefieldgoal is True:
                self.result = "FieldGoal"
        elif self.__dict__.get("madefieldpat"):
            if self.madefieldpat is True:
                self.result = "PAT"
        elif self.__dict__.get("interception"):
            if self.interception is True:
                self.result = "Interception"
        elif self.__dict__.get("punt"):
            if self.punt is True:
                self.result = "Punt"
        else:
            self.result = "Continue"