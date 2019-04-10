class playstartclass:
    def __init__(self, down=None, togo=None, startY=None, side=None, extra=None):
        self.down   = down
        self.togo   = togo
        self.startY = startY
        self.side   = side
        self.extra  = extra
        self.quarter   = None
        self.gameclock = None
        self.distToEndZone = None
        
    def setStartY(self, startY):
        self.startY = startY
        
    def setDistToEndZone(self, dist):
        self.distToEndZone = dist
        
    def setQuarter(self, quarter):
        self.quarter = quarter
        
    def setGameClock(self, gameclock):
        self.gameclock = gameclock
        
        
class drivedetailclass:
    def __init__(self, plays, yards, gametime):
        self.plays = plays
        self.yards = yards
        self.gametime = gametime
        
        
class playclass:
    def __init__(self, possession, start, play, valid):
        self.possession = possession
        self.start      = start
        self.play       = play
        self.valid      = valid

class driveclass:
    def __init__(self, headline, detail, possession, postdrivehomescore, postdriveawayscore, plays=None):
        self.headline = headline
        self.detail   = detail
        self.possession = possession
        self.postdrivehomescore = postdrivehomescore
        self.postdriveawayscore = postdriveawayscore
        self.plays = plays
        
    def setPlays(self, plays):
        self.plays = plays