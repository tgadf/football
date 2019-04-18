# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))

class debugclass:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 0*" "
        self.sep    = "======================================================"
        
        
    def showPlay(self, drivePlay, driveNo=None, playNo=None):
        play       = drivePlay.play
        possession = drivePlay.possession
        valid      = play.valid
        text       = possession.text
        keys       = play.pa.getKeys()
        if valid is False:
            self.logger.debug("{0: <5}{1: <5}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format(str(driveNo),str(playNo),
                                                                                         "",
                                                                                         str(play.name),
                                                                                         "",
                                                                                         "",
                                                                                         str(keys),str(text)))
            return
            
        self.logger.debug("{0: <5}{1: <5}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format(str(driveNo),str(playNo),
                                                                                     str(possession.start),
                                                                                     str(play.name),
                                                                                     str(possession.player),
                                                                                     str(possession.position),
                                                                                     str(keys),str(text)))



    def header(self, fout=None):
        self.logger.debug("{0: <5}{1: <5}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format("Drv","Ply",
                                                                                     "Poss",
                                                                                     "Type",
                                                                                     "Player",
                                                                                     "Position",
                                                                                     "Keys","Text"))

        
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