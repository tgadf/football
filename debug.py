# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class debugclass:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 0*" "
        self.sep    = "======================================================"
        
        self.spacing = {"Drv": 5, "Ply": 5, "Poss": 5, "Dwn": 5, "Yds": 5, "Line": 10, "Play": 10, "Player": 10, "Keys": 40, "Text": 40}
        self.naming  = []
        for key,value in self.spacing.items():
            self.naming.append("{0}: <{1}".format(len(self.naming), value))  
        self.naming = "{"+"}{".join(self.naming)+"}"


    def header(self, fout=None):
        self.logger.debug("{0: <5}{1: <5}{2: <5}{3: <5}{4: <5}{5: <10}{6: <6}{7: <6}{8: <12}{9: <25}{10: <40}{11: <40}".format(
                "Drv", "Ply", "Poss", "Dwn", "ToGo", "Line", "Next", "Yards", "Play", "Player", "Keys", "Text"))

        
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
        yds        = start.togo
        if yds is None:
            yds = "-"
        startY     = start.startY
        if startY is None:
            startY = "?"
        side       = start.side
        if side is None:
            side = "?"
        line       = "-".join([str(startY), str(side)])
        text       = possession.text
        keys       = ",".join(play.pa.getKeys())
        
        resultyards = play.yds.yards
        if resultyards is None:
            resultyards = "?"
        
        nextDiffYards = drivePlay.nextDiffYards
        if nextDiffYards is None:
            nextDiffYards = "-"
        prevDiffYards = drivePlay.prevDiffYards
        if prevDiffYards is None:
            prevDiffYards = "-"
        
        
        
        data = {"Drv": str(driveNo), "Ply": str(playNo), "Poss": poss, "Dwn": str(down), "Yds": str(yds),
                "Prev": str(prevDiffYards), "Next": str(nextDiffYards), "Result": resultyards,
                "Line": line, "Play": str(name), "Player": str(player), "Keys": keys, "Text": str(text)}
        
        naming  = []
        for key,value in self.spacing.items():
            naming.append("{0}: <{1}".format(key, value))
        naming = "{"+"}{".join(naming)+"}"
        
        self.logger.debug("{0: <5}{1: <5}{2: <5}{3: <5}{4: <5}{5: <10}{6: <6}{7: <6}{8: <12}{9: <25}{10: <40}{11: <40}".format(
                data["Drv"],data["Ply"], data["Poss"], data["Dwn"], data["Yds"], data["Line"], data["Next"], data["Result"], data["Play"], data["Player"], data["Keys"], data["Text"]))




        
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
            for ipl,drivePlay in enumerate(drivePlays):
                self.showPlay(drivePlay, driveNo=idr, playNo=ipl)
            self.logger.debug("")
        self.logger.debug("\n")