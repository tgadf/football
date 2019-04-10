from espngames import historical

class teamstatisticsclass:
    def __init__(self):
        self.passerkeys = []
        keys  = ["deep left pass", "deep right pass", "deep middle pass", "left side pass", "right side pass", "deep pass", "sideline pass", "middle pass", "post pass"]
        keys += ["across the middle pass", "right sideline pass", "right screen pass", "left screen pass", "deep sideline pass", "left sideline pass", "right endzone pass", "flag pass"]
        keys += ["right deep sideline pass", "deep out pass", "medium pass", "short left pass", "shovel pass", " pass left ", " pass right ", "medium middle pass", "crossing pass"]
        keys += ["slant pass", "curl pass", "screen pass", "left deep sideline pass", "short middle pass", "deep in pass"]
        names   = [" pass complete", " Pass Complete", "PASS COMPLETE"] + [" pass incomplete", " Pass Incomplete", "PASS INCOMPLETE"]
        names  += ["pass intercepted", "Pass Intercepted", "PASS INTERCEPTED"]

        for key in keys:
            self.passerkeys.append("{0}".format(key))
        for name in names:
            self.passerkeys.append("{0}".format(name))
        
        self.sackedkeys = [" sack by", " Sack By", "SACK BY", " sacked by", " Sacked By", "SACKED BY"]
                                
        self.runnerkeys = ["run for ", "run for ".title(), "run for".upper(), "runs for ", "runs for ".title(), "runs for".upper()]

        self.punterkeys = [" punt for ", " Punt For ", " PUNT FOR ", " punts for ", " Punts For ", " PUNTS FOR "]
        
        self.kickerkeys = ["kickoff", "Kickoff", "KICKOFF", "on-side kickoff"]
        
        self.fgkickerkeys = ["Kick)", "kick)", "KICK)"]

            
    ##############################################################################
    #
    # Main Loop
    #
    ##############################################################################
    def collect(self, hist, test=False, debug=False):
        files    = findExt(hist.getGamesResultsDir(), ext=".p", debug=debug)
        for ifile in files:
            print(ifile)
            try:
                year = int(getBaseFilename(ifile).split("-")[0])
            except:
                raise ValueError("Could not get year from {0}".format(ifile))
            
            if year != 2014:
                continue
                
            yearData = getFile(ifile)
            
            
            seasonFilename = setFile(hist.getSeasonResultsDir(), "{0}.p".format(year))
            seasonData     = getFile(seasonFilename)
            
            statsData      = {}                    
            self.runners   = {}
            self.passers   = {}
            self.punters   = {}
            self.kickers   = {}
            self.fgkickers = {}
                
            
            for teamID,teamData in seasonData.teams.items():
                games = [x["Game"] for x in teamData.games]
                for game in games:
                    gameID = game.gameID

                    
                    try:
                        gameData = yearData[gameID]
                    except:
                        continue
                        
                
                    teamsMetaData    = gameData["Teams"]
                    homeTeamMetaData = teamsMetaData["Home"]
                    awayTeamMetaData = teamsMetaData["Away"]
                    driveData        = gameData["Plays"]

                    fieldMap = {}
                    fieldMap[homeTeamMetaData["ID"]]     = homeTeamMetaData["Abbrev"]
                    fieldMap[homeTeamMetaData["Abbrev"]] = homeTeamMetaData["ID"]
                    fieldMap[awayTeamMetaData["ID"]]     = awayTeamMetaData["Abbrev"]
                    fieldMap[awayTeamMetaData["Abbrev"]] = awayTeamMetaData["ID"]

                    fieldMap["Home"] = homeTeamMetaData["Abbrev"]
                    fieldMap["Away"] = awayTeamMetaData["Abbrev"]
                    
                    copMap = {}
                    copMap[homeTeamMetaData["ID"]] = awayTeamMetaData["ID"]
                    copMap[awayTeamMetaData["ID"]] = homeTeamMetaData["ID"]
                

                    self.getRunners(driveData, fieldMap, debug=False)
                    self.getPassers(driveData, fieldMap, debug=False)
                    self.getPunters(driveData, fieldMap, debug=False)
                    self.getKickers(driveData, copMap, debug=False)
                    self.getFieldGoalKickers(driveData, fieldMap, debug=False)
                    
            
            ###
            ### Now Assign Player To A Team
            ###
            
            ### Passers
            from math import sqrt
            mapping = {"Passers": self.passers, "Runners": self.runners, "Punters": self.punters, "Kickers": self.kickers, "FGKickers": self.fgkickers}
            for position,players in mapping.items():
                for name,passerTeams in players.items():
                    mc     = passerTeams.most_common(1)[0]
                    frac   = mc[1] / sum(dict(passerTeams).values())
                    if frac < 0.75:
                        continue
                    sig    = sqrt(sum(dict(passerTeams).values()))
                    if sig < 2:
                        continue
                    teamID = mc[0]
                    if statsData.get(teamID) is None:
                        statsData[teamID] = {}
                    if statsData[teamID].get(position) is None:
                        statsData[teamID][position] = {}
                    statsData[teamID][position][name] = [round(frac,1),round(sig,1)]

                            
            ## Show team stats
            if debug:
                for teamID,teamStats in statsData.items():
                    print(teamID)
                    for pos,names in teamStats.items():
                        statsData[teamID]
                        print('\t',pos,names)
                    
                    
            if test is False:
                augmentedStatsFilename = setFile(hist.getStatisticsResultsDir(), "{0}-stats-extra.json".format(year))
                saveFile(idata=statsData, ifile=augmentedStatsFilename, debug=True)

                    
                    
    ###############################################################################################################
    # Clean Text
    ###############################################################################################################
    def clean(self, playText):
        ## Remove clock/quarter information
        pos = playText.find(")")
        if pos > 0 and pos < len(playText) - 2:
            playText = playText[pos+1:].strip()     
        return playText
    

    
    ###############################################################################################################
    # Add Player
    ###############################################################################################################
    def getPos(self, playText, keys, debug=False):
        vals = [playText.find(x) for x in keys]
        vals = [x for x in vals if x > 0]
        if len(vals) == 0:
            return None
        pos = min(vals)
        return pos
    
    
    def getName(self, playText, pos, debug=False):
        if pos is None:
            return None
        if pos > 0:
            text = playText[:pos].strip()
            if text in ["TEAM", "Team", "- Team", "team"]:
                return
            
            if text.find(",") != -1:
                if sum([x.upper() == "TEAM" for x in text.split()]) == 0:
                    vals = [x.strip() for x in text.split(",")]
                    if len(vals) == 2:
                        text = " ".join([vals[1], vals[0]])
                    
            if sum([x == x.upper() for x in text.split()]) > 0:
                text = " ".join([x.title() for x in text.split()])

            if len(text.split()) >= 4:
                return None
            
            if text.startswith("-") is True:
                return None
            
            if sum([x.upper() == "CLOCK" for x in text.split()]) > 0:
                return None
            
            if sum([x == x.lower() for x in text.split()]) > 0:
                print("[{0}]".format(text),' \t',pos,'\t ',playText)
            
            return text
                
        return None

    
    def addPlayer(self, name, possession, players, position, debug=False):
        if name is None:
            return
        if players.get(name) is None:
            players[name] = Counter()
            if debug:
                print("Adding {0} player: {1}".format(position, name))
        players[name][possession] += 1


    
        
    ###############################################################################################################
    # Runners
    ###############################################################################################################
    def getRunners(self, driveData, fieldMap, debug=False):
        for idr,drive in enumerate(driveData):
            possession = drive['Posession'][0]
            if fieldMap is not None:
                if fieldMap.get(possession) is None:
                    continue
            for ipl,play in enumerate(drive["Data"]):
                self.getRunnerText(play["Data"], possession, debug)


    def getRunnerText(self, playText, possession, debug=False):
        playText = self.clean(playText)
        if self.getPos(playText, self.passerkeys, debug) is not None:
            return
        pos  = self.getPos(playText, self.runnerkeys, debug)
        name = self.getName(playText, pos, debug)
        self.addPlayer(name, possession, self.runners, "RB", debug)

                    
    ###############################################################################################################
    # Passers
    ###############################################################################################################
    def getPassers(self, driveData, fieldMap, debug=False):
        for idr,drive in enumerate(driveData):
            possession = drive['Posession'][0]
            ptype    = playtype(drive['Headline'][0])
            headline = ptype.getPlay()
            if debug:
                print('\n',idr,'\t',headline,'\t',end="")
            if not isinstance(headline, (puntplay, fieldgoalplay)):
                if debug:
                    print("Not a punt/FG")
                #continue
            if fieldMap is not None:
                if fieldMap.get(possession) is None:
                    if debug:
                        print("Not in field map")
                    continue
            if debug:
                print("Good")
            for ipl,play in enumerate(drive["Data"]):
                self.getPasserText(play["Data"], possession, idr, ipl, debug)


    def getPasserText(self, playText, possession, idr, ipl, debug=False):
        playText = self.clean(playText)
        pos  = self.getPos(playText, self.passerkeys, debug)
        name = self.getName(playText, pos, debug)
        self.addPlayer(name, possession, self.passers, "QB", debug)                
        if debug and name is not None:
            print("\t{0: <8}{1: <4}{2: <4}{3}\t{4: <20}{5}\t{6}".format(possession, idr, ipl, "QB", name, self.passers[name], playText))


                   
            
    ###############################################################################################################
    # Punters
    ###############################################################################################################
    def getPunters(self, driveData, fieldMap, debug=False):
        for idr,drive in enumerate(driveData):
            possession = drive['Posession'][0]
            if fieldMap is not None:
                if fieldMap.get(possession) is None:
                    continue
            for ipl,play in enumerate(drive["Data"]):
                self.getPunterText(play["Data"], possession, debug)


    def getPunterText(self, playText, possession, debug=False):
        playText = self.clean(playText)
        pos  = self.getPos(playText, self.punterkeys, debug)
        name = self.getName(playText, pos, debug)
        self.addPlayer(name, possession, self.punters, "P", debug)                              

                   
            
    ###############################################################################################################
    # Kickers
    ###############################################################################################################
    def getKickers(self, driveData, fieldMap, debug=False):
        for idr,drive in enumerate(driveData):
            possession = drive['Posession'][0]
            if fieldMap is not None:
                if fieldMap.get(possession) is None:
                    continue
                possession = fieldMap[possession]
            for ipl,play in enumerate(drive["Data"]):
                self.getKickerText(play["Data"], possession, debug)


    def getKickerText(self, playText, possession, debug=False):
        playText = self.clean(playText)
        pos  = self.getPos(playText, self.kickerkeys, debug)
        name = self.getName(playText, pos, debug)
        self.addPlayer(name, possession, self.kickers, "K", debug)                                           

                   
            
    ###############################################################################################################
    # Field Goal Kickers
    ###############################################################################################################
    def getFieldGoalKickers(self, driveData, fieldMap, debug=False):
        for idr,drive in enumerate(driveData):
            possession = drive['Posession'][0]
            if fieldMap is not None:
                if fieldMap.get(possession) is None:
                    continue
            for ipl,play in enumerate(drive["Data"]):
                self.getFieldGoalText(play["Data"], possession, debug)


    def getPATText(self, playText, possession, retname=False, debug=False):
        start = playText.rfind("(")
        end   = playText.rfind(")")
        if start > 0 and end > 0 and start < end:
            playText = playText[start+1:end+1]
            pos  = self.getPos(playText, self.fgkickerkeys, debug)
            name = self.getName(playText, pos, debug)
            if retname:
                return name
            self.addPlayer(name, possession, self.fgkickers, "PK", debug)
        return None
            
                
    def getFGText(self, playText, possession, retname=False, debug=False):
        ### Field Goal
        kick = ("(fg|FG)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
        m = re.split("{0}\s{1}\s{2}".format(num, dist, kick), playText)
        if len(m) > 1:
            name = m[0].strip()
            if retname:
                return name
            self.addPlayer(name, possession, self.fgkickers, "PK", debug)
            
            
        ### Field Goal
        wrd1 = ("(field|Field|FIELD)")
        wrd2 = ("(goal|Goal|GOAL)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yard|Yds|yds|Yd|yd)")
        
        m = re.split("{0}\s{1}\s{2}\s{3}".format(num, dist, wrd1, wrd2), playText)
        if len(m) > 1:
            name = m[0].strip()
            if retname:
                return name
            self.addPlayer(name, possession, self.fgkickers, "PK", debug)
            
        return None
    
                
    def getFieldGoalText(self, playText, possession, debug=False):
        playText = self.clean(playText)
        self.getPATText(self, playText, possession, retname=False, debug=debug)
        self.getFGText(self, playText, possession, retname=False, debug=debug)