# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class debugclass:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 0*" "
        self.sep    = "======================================================"
        
        self.spacing = {"Drv": 5, "Ply": 5, "Poss": 5, "Dwn": 5, "Yds": 5, "Penal": 5, "Pred": 10, "Line": 10, "Play": 10, "Player": 10, "Keys": 40, "Text": 40}
        self.naming  = []
        for key,value in self.spacing.items():
            self.naming.append("{0}: <{1}".format(len(self.naming), value))  
        self.naming = "{"+"}{".join(self.naming)+"}"


    def header(self, fout=None):
        
        self.dvals = {
        "Drv": "Drv"       , "DrvN":    5,
        "Ply": "Ply"       , "PlyN":    5,
        "Poss": "Poss"     , "PossN":   5,
        "Dwn": "Dwn"       , "DwnN":    5,
        "ToGo": "ToGo"     , "ToGoN":   5,
        "Line": "Line"     , "LineN":   10,
        "Next": "Next"     , "NextN":   6,
        "Yards": "Yards"   , "YardsN":  6,
        "Conn": "Conn"     , "ConnN":   6,
        "Penal": "Penal"   , "PenalN":  6,
        "Pred": "Pred"     , "PredN":   6,
        "Play": "Play"     , "PlayN":   12,
        "Player": "Player" , "PlayerN": 25,
        "Keys": "Keys"     , "KeysN":   40,
        "Text": "Text"     , "TextN":   40
        } 
        
        vals = []
        for k,v in self.dvals.items():
            if isinstance(v, str):
                vals.append("{0}: <{1}".format(k, "{0}N".format(k)))        
        vals = ["{0}{1}{2}".format('{', x, '}}').replace("<", "<{") for x in vals]
        self.logger.debug("".join(vals).format_map(self.dvals))
        
        
    def showPlay(self, drivePlay, driveNo=None, playNo=None):
        play       = drivePlay.play
        name       = play.name
        possession = drivePlay.possession
        poss       = possession.start
        position   = possession.position
        if position is None:
            position = "?"
        player     = possession.player
        if player is None:
            player = "?"
        player     = "-".join([position, player])
        start      = drivePlay.start
        down       = start.down
        if down is None:
            down = "-"
        togo        = start.togo
        if togo is None:
            togo = "-"
        startY     = start.startY
        if startY is None:
            startY = "?"
        side       = start.side
        if side is None:
            side = "?"
        line       = "-".join([str(startY), str(side)])
        text       = possession.text
        keys       = ",".join(play.pa.getKeys())
        
        conn = len(play.connectedPlays)
        if conn == 0:
            conn = ""
        
        yards = play.yds.yards
        if yards is None:
            yards = "?"
        
        nextDiffYards = drivePlay.nextDiffYards
        if nextDiffYards is None:
            nextDiffYards = "-"
        prevDiffYards = drivePlay.prevDiffYards
        if prevDiffYards is None:
            prevDiffYards = "-"
            
        if play.penalty.isPenalty == True:
            penal = 'x'
        else:
            penal = ''
        
        if isinstance(nextDiffYards, int):
            pred = nextDiffYards == yards
            if pred is False:
                pred = 'x'
            else:
                pred = ''
        else:
            pred = ''
        
        
        data = {"Drv": str(driveNo), "Ply": str(playNo), 
                "Poss": poss, "Dwn": str(down), "ToGo": str(togo),
                "Prev": str(prevDiffYards), "Next": str(nextDiffYards), "Yards": yards,
                "Penal": str(penal), "Pred": str(pred), "Conn": conn,
                "Line": line, "Play": str(name), "Player": str(player), 
                "Keys": keys, "Text": str(text)}
        for key in self.dvals.keys():
            if data.get(key) is not None:
                self.dvals[key] = data[key]
        
        vals = []
        for k,v in self.dvals.items():
            if k.endswith("N") is False:
                vals.append("{0}: <{1}".format(k, "{0}N".format(k)))        
        vals = ["{0}{1}{2}".format('{', x, '}}').replace("<", "<{") for x in vals]
        self.logger.debug("".join(vals).format_map(self.dvals))


        
    def compDrive(self, driveData, prevDriveData, driveNo=None, expl=None):
        self.logger.debug("\n{0} CompDrive({1}) {2}".format(self.sep, expl, self.sep))
        self.header()
        self.logger.debug("{0}New Drive".format(self.ind))
        drivePlays = driveData.plays
        for ipl,drivePlay in enumerate(drivePlays):
            self.showPlay(drivePlay, driveNo=driveNo, playNo=ipl)
        self.logger.debug("\n{0}Old Drive".format(self.ind))
        drivePlays = prevDriveData.plays
        for ipl,drivePlay in enumerate(drivePlays):
            self.showPlay(drivePlay, driveNo=driveNo, playNo=ipl)
        self.logger.debug("\n")


        
    def showDrive(self, driveData, driveNo=None, expl=None):
        self.logger.debug("\n{0} ShowDrive({1}) {2}".format(self.sep, expl, self.sep))
        self.header()        
        drivePlays = driveData.plays
        for ipl,drivePlay in enumerate(drivePlays):
            self.showPlay(drivePlay, driveNo=driveNo, playNo=ipl)
        
        
    def showGame(self, gameData, expl=None):
        self.logger.debug("\n{0} ShowGame({1}) {2}".format(self.sep, expl, self.sep))
        self.header()
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            self.logger.debug("SUMMARY ===> {0}".format(driveData.getSummaryText()))
            for ipl,drivePlay in enumerate(drivePlays):
                self.showPlay(drivePlay, driveNo=idr, playNo=ipl)
            self.logger.debug("\n")
        self.logger.debug("\n\n")