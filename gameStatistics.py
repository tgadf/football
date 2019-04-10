from searchUtils import findNearest
from collections import Counter
import re
from teamStatistics import teamstatisticsclass

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
                    print("  EXACT MATCH: {0} <-- {1}".format(pos, name))
                return [name,pos]
        
        if useNearest is not None:
            pos = findNearest(item=playText, ilist=playersDict.keys(), cutoff=useNearest, num=1)
            if len(pos) == 0:
                return None
            else:
                name = pos[0]
                pos  = playersDict[name]
                if debug:
                    print("  NEAR MATCH: {0} <-- {1}".format(name, playText))
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
    # Kicking Players
    ################################################################################################
    def getKickingTeam(self, playText, debug=False):
        #playText = self.tsc.clean(playText)
        pos      = self.tsc.getPos(playText, self.tsc.kickerkeys, debug)
        text     = self.tsc.getName(playText, pos, debug)
                        
        posnames = ["K", "PK", "P"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.kickers, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.kickers, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)
        if debug:
            print("  Kicking Team: {0}".format(retval))
        return retval
    
        
        
    ################################################################################################
    # Field Goal Players
    ################################################################################################



    def getPATText(self, playText, debug=False):
        start = playText.rfind("(")
        end   = playText.rfind(")")
        if start > 0 and end > 0 and start < end:
            playText = playText[start+1:end+1]
            pos  = self.getPos(playText, self.fgkickerkeys, debug)
            name = self.getName(playText, pos, debug)
            return name
        return None
            
                
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

    
    def getFGKickingTeam(self, playText, debug=False):
        if debug:
            print("\tgetFGKickingTeam(",playText,")")
            
        text = self.getFGText(playText, debug)
        if text is None:
            #playText = self.tsc.clean(playText)
            pos      = self.tsc.getPos(playText, self.tsc.fgkickerkeys, debug)
            if debug:
                print("\tgetFGKickingTeam:",pos)
            text     = self.tsc.getName(playText, pos, debug)
            if debug:
                print("\tgetFGKickingTeam:",text)
                        
        posnames = ["K", "PK", "P"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.fgkickers, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.fgkickers, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)
        
        if debug:
            print("  Field Goal Kicking Team: {0}".format(retval))
        return retval
    
        
        
    ################################################################################################
    # Punting Players
    ################################################################################################
    def getPuntingTeam(self, playText, debug=False):
        if debug:
            print("\tgetPuntingTeam(",playText,")")
        #playText = self.tsc.clean(playText)
        if debug:
            print("\tgetPuntingTeam(",playText,")")
        pos      = self.tsc.getPos(playText, self.tsc.punterkeys, debug)
        if debug:
            print("\tgetPuntingTeam:",pos)
        text     = self.tsc.getName(playText, pos, debug)
        if debug:
            print("\tgetPuntingTeam:",text)


        posnames = ["K", "PK", "P"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.punters, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.punters, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)
        
        if debug:
            print("  Punting Team: {0}".format(retval))        
        return retval
    
    
        
    ################################################################################################
    # Passing Players
    ################################################################################################
    def getPassingTeam(self, playText, debug=False):
        #playText = self.tsc.clean(playText)
        pos      = self.tsc.getPos(playText, self.tsc.passerkeys, debug)
        text     = self.tsc.getName(playText, pos, debug)
                        
        posnames = ["QB"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.passers, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.passers, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)
        
        if debug:
            print("  Passing Team: {0}".format(retval))
        return retval
    
    
        
    ################################################################################################
    # Sacked Players
    ################################################################################################
    def getSackedTeam(self, playText, debug=False):
        #playText = self.tsc.clean(playText)
        pos      = self.tsc.getPos(playText, self.tsc.sackedkeys, debug)
        text     = self.tsc.getName(playText, pos, debug)
                        
        posnames = ["QB"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.passers, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.passers, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)
        
        if debug:
            print("  Passing Team: {0}".format(retval))
        return retval
    
        
        
    ################################################################################################
    # Running Players
    ################################################################################################
    def getRunningTeam(self, playText, debug=False):
        #playText = self.tsc.clean(playText)
        pos      = self.tsc.getPos(playText, self.tsc.runnerkeys, debug)
        text     = self.tsc.getName(playText, pos, debug)
                         
        posnames = ["RB", "QB", "WR"]
        posH   = self.findPlayerTeam(text, self.homeTeamPlayers.runners, debug=debug)
        posA   = self.findPlayerTeam(text, self.awayTeamPlayers.runners, debug=debug)        
        retval = self.findReturnValue(posnames, posH, posA)      
        
        if retval[0] is None:
            run  = ("(run|Run|RUN)")
            num  = "([+-?]\d+|\d+)"  
            dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
            m = re.split("{0}\s{1}\s{2}".format(num, dist, run), playText)
            if len(m) > 1:
                text = m[0].strip()          

                posH   = self.findPlayerTeam(text, self.homeTeamPlayers.runners, debug=debug)
                posA   = self.findPlayerTeam(text, self.awayTeamPlayers.runners, debug=debug)        
                retval = self.findReturnValue(posnames, posH, posA)    
                
        if debug:
            print("  Running Team: {0}".format(retval))
        return retval
        

    
        
        
    ################################################################################################
    # Receiving Players
    ################################################################################################
    def getReceivingTeam(self, playText, debug=False):
        posnames = ["WR", "RB"]
        retval = None
        
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