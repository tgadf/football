class debugclass:
    def __init__(self):
        self.name = "debugclass"
        
    def showPlay(self, drivePlay, driveNo=None, playNo=None, debug=False):
        if debug is False:
            return        
        play       = drivePlay.play
        valid      = drivePlay.valid
        if valid is False:
            return
        possession = drivePlay.possession
        text       = possession.text
        keys = ",".join([k for k,v in play.pa.__dict__.items() if v is True])
        print("{0}\t{1}\t{2}\t{3: <15}{4: <15}{5: <5}{6: <40}{7}".format(str(driveNo),str(playNo),
                                                                         str(possession.start),
                                                                         str(play.name),
                                                                         str(possession.player),
                                                                         str(possession.position),
                                                                         str(keys),str(text)))


    def header(self):
        print("{0}\t{1}\t{2}\t{3: <15}{4: <15}{5: <5}{6: <40}{7}".format("Drive","Play",
                                                                         "Poss",
                                                                         "Type",
                                                                         "Player",
                                                                         "Position",
                                                                         "Keys","Text"))


        
    def showGame(self, gameData, debug=False):
        if debug is False:
            return

        self.header()
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                self.showPlay(drivePlay, driveNo=idr, playNo=ipl, debug=debug)
            print("")