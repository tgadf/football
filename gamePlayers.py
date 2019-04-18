from searchUtils import findNearest
import re
import sys
from teamPlayers import teamstatisticsclass

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class teamplayers:
    def __init__(self, statsData):
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        
        if statsData is None:
            raise ValueError("Stats data is empty!")
            
        self.statsData  = statsData
        self.kickers    = {}
        self.fgkickers  = {}
        self.punters    = {}
        self.passers    = {}
        self.runners    = {}
        self.receivers  = {}
        self.defense    = {}

        self.addPlayers()

    def getShortName(self, name):
        vals  = name.split()
        start = ["{0}.".format(y[0]) for y in vals[:-1]]
        end   = vals[-1]
        sname = " ".join([" ".join(start), end])
        return sname
                
        
    def setPositionPlayers(self, key, value):
        playerData = self.statsData.get(key)
        if playerData is None:
            print("Team {0} Data is None".format(key))
            return
        else:
            try:
                for player in playerData.keys():
                    name,pos = player.split("$")
                    name = name.strip()
                    if len(name) == 0 or len(pos) == 0:
                        continue
                    if name == "TOTAL" or pos == "ALL":
                        continue
                    value[name]                      = pos
                    value[self.getShortName(name)]   = pos
            except:
                print("ERROR getting setting player {0} data!: {0}".format(key, playerData.keys()))



    def addPlayers(self):
        ## Get Kickers
        self.setPositionPlayers(key="Kicking", value=self.kickers)
        self.setPositionPlayers(key="Kicking", value=self.fgkickers)
        self.setPositionPlayers(key="Kicking", value=self.punters)        
        
        ## Get Passers
        self.setPositionPlayers(key="Passing", value=self.passers)        
        
        ## Get Runners
        self.setPositionPlayers(key="Rushing", value=self.runners)       
        
        ## Get Receivers
        self.setPositionPlayers(key="Receiving", value=self.receivers)      
        
        ## Get Defense
        self.setPositionPlayers(key="Defense", value=self.defense)

    
    
class gameplayers:
    def __init__(self, statsData, teamsMap):
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        
        self.fieldMap = teamsMap
        
        homeTeam   = teamsMap['Home']
        homeTeamID = teamsMap[homeTeam]
        awayTeam   = teamsMap['Away']
        awayTeamID = teamsMap[awayTeam]

        homeTeamStatsData = statsData.get(homeTeamID)
        if homeTeamStatsData is None:
            print("WARNING: Home Team {0} stats data is NONE".format(homeTeam))
        awayTeamStatsData = statsData.get(awayTeamID)
        if awayTeamStatsData is None:
            print("WARNING: Away Team {0} stats data is NONE".format(homeTeam))
            
        self.homeTeamPlayers = teamplayers(homeTeamStatsData)
        self.homeTeamName    = homeTeam
        self.homeTeamID      = homeTeamID

        self.awayTeamPlayers = teamplayers(awayTeamStatsData)
        self.awayTeamName    = awayTeam
        self.awayTeamID      = awayTeamID
        
        self.logger.debug("{0}Home Team ({1}, {2}): {3}".format(self.ind, self.homeTeamName, self.homeTeamID, self.homeTeamPlayers))
        self.logger.debug("{0}Away Team ({1}, {2}): {3}".format(self.ind, self.awayTeamName, self.awayTeamID, self.awayTeamPlayers))
        
        
        self.tsc = teamstatisticsclass()

        
        
        self.punters   = {}
        self.runners   = {}
        self.kickers   = {}
        
        
    def augmentData(self, augmentedData, debug=False):
        homeTeamData = augmentedData.get(self.homeTeamID)
        if homeTeamData is not None:
            punters = homeTeamData.get("Punters")
            if punters is not None:
                for name,pos in punters.items():
                    self.homeTeamPlayers.punters[name] = "P"
            kickers = homeTeamData.get("Kickers")
            if kickers is not None:
                for name,pos in kickers.items():
                    self.homeTeamPlayers.kickers[name] = "K"
            fgkickers = homeTeamData.get("FGKickers")
            if fgkickers is not None:
                for name,pos in fgkickers.items():
                    self.homeTeamPlayers.fgkickers[name] = "PK"
            runners = homeTeamData.get("Runners")
            if runners is not None:
                for name,pos in runners.items():
                    self.homeTeamPlayers.runners[name] = "RB"
            passers = homeTeamData.get("Passers")
            if passers is not None:
                for name,pos in passers.items():
                    self.homeTeamPlayers.passers[name] = "QB"

        
        awayTeamData = augmentedData.get(self.awayTeamID)
        if awayTeamData is not None:
            punters = awayTeamData.get("Punters")
            if punters is not None:
                for name,pos in punters.items():
                    self.awayTeamPlayers.punters[name] = "P"
            kickers = awayTeamData.get("Kickers")
            if kickers is not None:
                for name,pos in kickers.items():
                    self.awayTeamPlayers.kickers[name] = "K"
            fgkickers = awayTeamData.get("FGKickers")
            if fgkickers is not None:
                for name,pos in fgkickers.items():
                    self.awayTeamPlayers.fgkickers[name] = "PK"
            runners = awayTeamData.get("Runners")
            if runners is not None:
                for name,pos in runners.items():
                    self.awayTeamPlayers.runners[name] = "RB"
            passers = awayTeamData.get("Passers")
            if passers is not None:
                for name,pos in passers.items():
                    self.awayTeamPlayers.passers[name] = "QB"


        self.logger.debug("{0}Augmented Home Team ({1}, {2}): {3}".format(self.ind, self.homeTeamName, self.homeTeamID, self.homeTeamPlayers))
        self.logger.debug("{0}Augmented Away Team ({1}, {2}): {3}".format(self.ind, self.awayTeamName, self.awayTeamID, self.awayTeamPlayers))
        

    def findPlayerTeam(self, playText, playersDict, useNearest=None, debug=False):
        if playText is None:
            return None
            
        for name,pos in playersDict.items():
            if name in playText:
                if debug:
                    print("\t\tEXACT MATCH: {0} <-- {1}".format(pos, name))
                return [name,pos]
        
        if useNearest is not None:
            pos = findNearest(item=playText, ilist=playersDict.keys(), cutoff=useNearest, num=1)
            if len(pos) == 0:
                return None
            else:
                name = pos[0]
                pos  = playersDict[name]
                if debug:
                    print("\t\tNEAR MATCH: {0} <-- {1}".format(name, playText))
                return [name,pos]
        
        return None
    
    
    def findReturnValue(self, posnames, posH, posA):
        if posH is not None and posA is None:
            name = posH[0]
            pos  = posH[1]
            return [self.homeTeamName,name,pos]
        elif posA is not None and posH is None:
            name = posA[0]
            pos  = posA[1]
            return [self.awayTeamName,name,pos]
        elif posH is None and posA is None:
            return [None,None,None]
        else:
            if posH in posnames:
                name = posH[0]
                pos  = posH[1]
                return [self.homeTeamName,name,pos]
            elif posA in posnames:
                name = posA[0]
                pos  = posA[1]
                return [self.awayTeamName,name,pos]

        return [None,None,None]

    
    
    ################################################################################################
    # Common Functions
    ################################################################################################
    def getName(self, playText, fname, keys):
        text = None
        if playText is not None and keys is not None:
            pos      = self.tsc.getPos(playText, keys)
            text     = self.tsc.getName(playText, pos)
        self.logger.debug("{0}  {1} --> {2}".format(self.ind, playText, text))
        return text
        

    def getTeam(self, name, fname, posnames, homePlayers, awayPlayers):
        posH   = self.findPlayerTeam(name, homePlayers)
        posA   = self.findPlayerTeam(name, awayPlayers)
        retval = self.findReturnValue(posnames, posH, posA)
        self.logger.debug("{0}  {1} --> {2}".format(self.ind, name, retval))
        return retval


        
    ################################################################################################
    # Kicking Players
    ################################################################################################
    def getKickingTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))        
        text = self.getName(playText, fname, self.tsc.kickerkeys)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.kickers, self.awayTeamPlayers.kickers)
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
        
        
    
    ################################################################################################
    # PAT Players
    ################################################################################################
    def getPATText(self, playText, debug=False):
        start = playText.rfind("(")
        end   = playText.rfind(")")
        if start > 0 and end > 0 and start < end:
            playText = playText[start+1:end+1]
            return playText
        return None
    
    def getPATKickingTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))      
        playText = self.getPATText(playText)
        text = self.getName(playText, fname, self.tsc.fgkickerkeys)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.fgkickers, self.awayTeamPlayers.fgkickers)
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
        
    
    
    ################################################################################################
    # Field Goal Players
    ################################################################################################
    def getFGText(self, playText, debug=False):
        ### Field Goal
        kick = ("(fg|FG)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
        m = re.split("{0}\s{1}\s{2}".format(num, dist, kick), playText)
        if len(m) > 1:
            name = m[0].strip()
            return name
            
        ### Field Goal
        wrd1 = ("(field|Field|FIELD)")
        wrd2 = ("(goal|Goal|GOAL)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
        
        m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
        if len(m) > 1:
            name = m[0].strip()
            return name
        
        return None

    
    def getFGKickingTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))      
        text = self.getFGText(playText)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.fgkickers, self.awayTeamPlayers.fgkickers)
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
        
        
    ################################################################################################
    # Punting Players
    ################################################################################################
    def getPuntingTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))      
        text = self.getName(playText, fname, self.tsc.punterkeys)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.punters, self.awayTeamPlayers.punters)
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
    
        
    ################################################################################################
    # Passing Players
    ################################################################################################
    def getPassingText(self, fname, playText, posnames):
        retval = None
        wrd1 = ("(pass|Pass|PASS)")
        wrd2 = ("(from|From|FROM)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
        m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
        if len(m) > 1:
            try:                    
                text   = " ".join([x.strip() for x in m[-1].split()[:2]])
                retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.passers, self.awayTeamPlayers.passers)
            except:
                retval = None
        return retval
                
    
    def getPassingTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))      
        text = self.getName(playText, fname, self.tsc.passerkeys)
        posnames = ["QB", "RB", "WR"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.passers, self.awayTeamPlayers.passers)
        
        if retval[0] is None:
            retval = self.getPassingText(fname, text, posnames)
                
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
    
        
    ################################################################################################
    # Sacked Players
    ################################################################################################
    def getSackedTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))
        text = self.getName(playText, fname, self.tsc.sackedkeys)
        posnames = ["QB"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.passers, self.awayTeamPlayers.passers)
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
    
        
        
    ################################################################################################
    # Running Players
    ################################################################################################
    def getRunningText(self, fname, playText, posnames):
        retval = None
        run  = ("(run|Run|RUN)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
    
        m = re.split("{0}\s{1}\s{2}".format(num, dist, run), playText)
        if len(m) > 1:
            text = m[0].strip()
            retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.runners, self.awayTeamPlayers.runners)
        return retval
    
        
    def getRunningTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))
        text = self.getName(playText, fname, self.tsc.runnerkeys)
        posnames = ["QB", "WR", "RB"]
        retval = self.getTeam(text, fname, posnames, self.homeTeamPlayers.runners, self.awayTeamPlayers.runners)
        
        if retval[0] is None:
            self.getRunningText(fname, playText, posnames)
            
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
        

    
        
        
    ################################################################################################
    # Receiving Players
    ################################################################################################
    def getReceivingTeam(self, playText):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))
        posnames = ["WR", "RB", "TE", "QB"]
        retval = [None,None,None]
        
        ## Fix Text
        keys = ["pass complete", "Pass Complete", "PASS COMPLETE", "pass incomplete", "Pass Incomplete", "PASS INCOMPLETE"]
        pos = max([playText.find(x) for x in keys])
        if pos > 0:
            txt = playText[pos:].strip()
            txt = " ".join(txt.split()[2:])[3:].strip()
            keys = [" for ", " For ", " FOR "]
            pos = [x for x in [txt.find(x) for x in keys] if x != -1]
            if len(pos) > 0 and min(pos) > 0:
                text = txt[:min(pos)].strip()

                posH   = self.findPlayerTeam(text, self.homeTeamPlayers.receivers)
                posA   = self.findPlayerTeam(text, self.awayTeamPlayers.receivers)        
                retval = self.findReturnValue(posnames, posH, posA)          
        
        
        if retval[0] is None:
            wrd1 = ("(pass|Pass|PASS)")
            wrd2 = ("(from|From|FROM)")
            num  = "([+-?]\d+|\d+)"  
            dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
            m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
            if len(m) > 1:
                text = m[0].strip()
                posH   = self.findPlayerTeam(text, self.homeTeamPlayers.receivers)
                posA   = self.findPlayerTeam(text, self.awayTeamPlayers.receivers)
                retval = self.findReturnValue(posnames, posH, posA)    
                
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return retval
                
        
        
    ################################################################################################
    # Defense Players
    ################################################################################################
    def getDefenseTeam(self, playText, debug=False):
        fname = sys._getframe().f_code.co_name
        self.logger.debug("{0}{1}({2})".format(self.ind, fname, playText))
        return None
        pos = self.findPlayerTeam(playText, self.homeTeamPlayers.defense)
        if pos is not None:
            return self.homeTeamName

        pos = self.findPlayerTeam(playText, self.awayTeamPlayers.defense)
        if pos is not None:
            return self.awayTeamName
        
        self.logger.debug("{0}{1}({2}) --> {3}".format(self.ind, fname, playText, retval))
        return None