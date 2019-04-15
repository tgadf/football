class debugclass:
    def __init__(self):
        self.name = "debugclass"
        
    def showPlay(self, drivePlay, driveNo=None, playNo=None, fout=None, debug=False):
        if debug is False:
            return        
        play       = drivePlay.play
        valid      = drivePlay.valid
        if valid is False:
            return
        possession = drivePlay.possession
        text       = possession.text
        keys = ",".join([k for k,v in play.pa.__dict__.items() if v is True])
        if fout is not None:
            print("{0}\t{1}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format(str(driveNo),str(playNo),
                                                                             str(possession.start),
                                                                             str(play.name),
                                                                             str(possession.player),
                                                                             str(possession.position),
                                                                             str(keys),str(text)), file=open(fout, "a"))
        else:
            print("{0}\t{1}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format(str(driveNo),str(playNo),
                                                                             str(possession.start),
                                                                             str(play.name),
                                                                             str(possession.player),
                                                                             str(possession.position),
                                                                             str(keys),str(text)))



    def header(self, fout=None):
        if fout is not None:
            print("{0}\t{1}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format("Drive","Play",
                                                                             "Poss",
                                                                             "Type",
                                                                             "Player",
                                                                             "Position",
                                                                             "Keys","Text"), file=open(fout, "a"))
        else:
            print("{0}\t{1}\t{2}\t{3: <15}{4: <20}{5: <5}{6: <40}{7}".format("Drive","Play",
                                                                             "Poss",
                                                                             "Type",
                                                                             "Player",
                                                                             "Position",
                                                                             "Keys","Text"))


        
    def showDrive(self, driveData, driveNo=None, fout=None, debug=False):
        if debug is False:
            return

        self.header()        
        drivePlays = driveData.plays
        for ipl,drivePlay in enumerate(drivePlays):
            self.showPlay(drivePlay, driveNo=driveNo, playNo=ipl, fout=fout, debug=debug)                
        if fout is None:
            print("")
        else:
            print("", file=open(fout, "a"))
        
        
    def showGame(self, gameData, fout=None, debug=False):
        if debug is False:
            return

        self.header(fout)
        
        for idr,driveData in enumerate(gameData):
            drivePlays = driveData.plays
            for ipl,drivePlay in enumerate(drivePlays):
                self.showPlay(drivePlay, driveNo=idr, playNo=ipl, fout=fout, debug=debug)
                
            if fout is None:
                print("")
            else:
                print("", file=open(fout, "a"))