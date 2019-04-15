from searchUtils import findNearest
import re
import sys
from teamPlayers import teamstatisticsclass

class teamplayers:
    def __init__(self, statsData):
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
    def getName(self, playText, fname, keys, debug=False, verydebug=False):
        if debug:
            print("\t{0}({1})".format(fname, playText))
        if playText is None or keys is None:
            return None
        pos      = self.tsc.getPos(playText, keys, verydebug)
        text     = self.tsc.getName(playText, pos, verydebug)
        if verydebug:
            print("\t{0}({1}) -> {2}".format(fname, playText, text))
        return text
        

    def getTeam(self, name, fname, posnames, homePlayers, awayPlayers, debug=False, verydebug=False):
        posH   = self.findPlayerTeam(name, homePlayers, debug=verydebug)
        posA   = self.findPlayerTeam(name, awayPlayers, debug=verydebug)
        if verydebug:
            print("\t{0}:  Home == {1} \tAway == {2}".format(fname, posH, posA))
        retval = self.findReturnValue(posnames, posH, posA)
        if debug:
            print("\t{0}({1}) -> {2}".format(fname, name, retval))
        return retval


        
    ################################################################################################
    # Kicking Players
    ################################################################################################
    def getKickingTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        text = self.getName(playText, fname, self.tsc.kickerkeys, debug, verydebug)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.kickers, self.awayTeamPlayers.kickers, debug, verydebug)
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
        playText = self.getPATText(playText)
        text = self.getName(playText, fname, self.tsc.fgkickerkeys, debug, verydebug)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.fgkickers, self.awayTeamPlayers.fgkickers, debug, verydebug)
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
        text = self.getFGText(playText)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.fgkickers, self.awayTeamPlayers.fgkickers, debug=debug, verydebug=verydebug)
        return retval
    
        
        
    ################################################################################################
    # Punting Players
    ################################################################################################
    def getPuntingTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        text = self.getName(playText, fname, self.tsc.punterkeys, debug, verydebug)
        posnames = ["K", "PK", "P"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.punters, self.awayTeamPlayers.punters, debug, verydebug)
        return retval
    
    
        
    ################################################################################################
    # Passing Players
    ################################################################################################
    def getPassingTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        text = self.getName(playText, fname, self.tsc.passerkeys, debug, verydebug)
        posnames = ["QB", "RB", "WR"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.passers, self.awayTeamPlayers.passers, debug, verydebug)
        
        if retval[0] is None:
            wrd1 = ("(pass|Pass|PASS)")
            wrd2 = ("(from|From|FROM)")
            num  = "([+-?]\d+|\d+)"  
            dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
            m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
            if len(m) > 1:
                try:                    
                    text   = " ".join([x.strip() for x in m[-1].split()[:2]])
                    retval = self.getTeam(text, text, posnames, 
                                          self.homeTeamPlayers.passers, self.awayTeamPlayers.passers, debug, verydebug)
                except:
                    pass
                
        return retval
    
    
        
    ################################################################################################
    # Sacked Players
    ################################################################################################
    def getSackedTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        text = self.getName(playText, fname, self.tsc.sackedkeys, debug, verydebug)
        posnames = ["QB"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.passers, self.awayTeamPlayers.passers, debug, verydebug)
        return retval
    
        
        
    ################################################################################################
    # Running Players
    ################################################################################################
    def getRunningTeam(self, playText, debug=False, verydebug=False):
        fname = sys._getframe().f_code.co_name
        text = self.getName(playText, fname, self.tsc.runnerkeys, debug, verydebug)
        posnames = ["QB", "WR", "RB"]
        retval = self.getTeam(text, fname, posnames, 
                              self.homeTeamPlayers.runners, self.awayTeamPlayers.runners, debug, verydebug)
        
        if retval[0] is None:
            run  = ("(run|Run|RUN)")
            num  = "([+-?]\d+|\d+)"  
            dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
            m = re.split("{0}\s{1}\s{2}".format(num, dist, run), playText)
            if len(m) > 1:
                text = m[0].strip()
                retval = self.getTeam(text, fname, posnames, 
                                      self.homeTeamPlayers.runners, self.awayTeamPlayers.runners, debug, verydebug)
                
        return retval
        

    
        
        
    ################################################################################################
    # Receiving Players
    ################################################################################################
    def getReceivingTeam(self, playText, debug=False, verydebug=False):
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

                posH   = self.findPlayerTeam(text, self.homeTeamPlayers.receivers, debug=debug)
                posA   = self.findPlayerTeam(text, self.awayTeamPlayers.receivers, debug=debug)        
                retval = self.findReturnValue(posnames, posH, posA)          
        
        
        if retval[0] is None:
            wrd1 = ("(pass|Pass|PASS)")
            wrd2 = ("(from|From|FROM)")
            num  = "([+-?]\d+|\d+)"  
            dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
            m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
            if len(m) > 1:
                text = m[0].strip()
                posH   = self.findPlayerTeam(text, self.homeTeamPlayers.receivers, debug=debug)
                posA   = self.findPlayerTeam(text, self.awayTeamPlayers.receivers, debug=debug)        
                retval = self.findReturnValue(posnames, posH, posA)    
                
                
        if debug:
            print("  Receiving Team: {0}".format(retval))
        return retval
                
        
        
    ################################################################################################
    # Defense Players
    ################################################################################################
    def getDefenseTeam(self, playText, debug=False):
        return None
        pos = self.findPlayerTeam(playText, self.homeTeamPlayers.defense)
        if pos is not None:
            return self.homeTeamName

        pos = self.findPlayerTeam(playText, self.awayTeamPlayers.defense)
        if pos is not None:
            return self.awayTeamName
        
        return None