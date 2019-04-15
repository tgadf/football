from playYards import playyards
from playResult import playanalysis


############################################################################################################
### ## Football Play Type
############################################################################################################
class playtype:
    def __init__(self, playText, debug=False):
        play = None
        self.playtext = playText
        self.valid = True
        self.unknownPlays = []
        
        playSubText = playText
        pos = playText.rfind("(")
        if pos != -1 and pos > 5:
            playSubText = playText[:pos].strip()
            
        
        if sum([x in playSubText for x in ["field goal", "Field Goal", "Field goal", "FIELD GOAL", " fg ", " FG ", "MISSED FG", "Missed FG"]]) > 0:
            play = fieldgoalplay(playText, debug=debug)
        elif sum([x in playText for x in ["fake field goal", "Fake Field Goal"]]) > 0:
            play = fieldgoalplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["timeout", "Timeout"]]) > 0:
            play = timeoutplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["kickoff", "Kickoff", "kick off", "Kick Off", "Onside Kick", "Onside kick", "onside kick", "on-side kick", " kick for "]]) > 0:
            play = kickoffplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["punt ", "PUNT", "Punt", " punted", " Punted", " punt,", " punter ", "punts "]]) > 0:
            play = puntplay(playText, debug=debug)
        elif playSubText.endswith(" punt"):
            play = puntplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["end of the ", "End Of The ", "End of the ", "end of ", "End of ", "END OF "]]) > 0:
            play = endplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["start of the ", "Start Of The ", "Start of the ", "Begin Drive", "start of ", "Start of ", "START OF "]]) > 0:
            play = beginplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["SAFETY", "safety", "Safety"]]) > 0:
            play = safetyplay(playText, debug=debug)
        elif sum([x in playSubText for x in [" sack ", " sacked ", " Sack ", " Sacked ", "sacked,"]]) > 0:
            play = sackplay(playText, debug=debug)
        elif sum([x in playSubText for x in [" pass ", " passed ", " Pass ", " Passed ", " spikes ", " spiked ", " pass,to ",
                                          "Interception Return", "Interception", "INTERCEPTION"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText, debug=debug)
            elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
                play = penaltyplay(playText, debug=debug)
            else:
                play = passingplay(playText, debug=debug)
        elif sum([x in playSubText for x in [" rush ", " rushed ", " Rush ", " Rushed ", " scramble", " rush,", " run ", " Run"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText, debug=debug)
            elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
                play = penaltyplay(playText, debug=debug)
            else:
                play = rushingplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
            play = penaltyplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["fumble", "Fumble", " fumbled ", " Fumble ", " Fumbled ", "FUMBLE"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText, debug=debug)
            else:
                play = fumbleplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["downs", "Downs", "DOWNS"]]) > 0:
            play = downsplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
            play = touchdownplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["extra point", "Extra Point", "Extra point", "PAT", "2 point", "2 Point", "two-point", "Two-point", "Two-Point"]]) > 0:
            play = patplay(playText, debug=debug)
        elif sum([x in playSubText for x in ["NO PLAY", "No Play"]]) > 0:
            play = noplay(playText, debug=debug)
        elif len(playText) > 1:
            play = tbdplay(playText, debug=debug)
        elif len(playText) <= 1:
            self.play  = None
            self.valid = False
            if debug:
                print("PLAYTEXT is EMPTY!!! so PLAY == NONE")
        else:
            self.unknownPlays.append(playText)
            self.play = None
            self.valid = False
            if debug:
                raise ValueError("NO IDEA ABOUT THIS PLAY: {0}".format(playText))
            
        self.play = play
        
                
    def isValid(self):
        return self.valid
            
    def getPlay(self):
        return self.play
        
    def getPlayText(self):
        return self.playtext
                        

############################################################################################################
### ## Football Play Data
############################################################################################################
class footballplay:
    def __init__(self, playtype, text, debug=False):
        self.playtype = playtype.title()
        self.text     = text
        
        self.__dict__[playtype] = True
        
        self.startY  = None
        self.endY    = None
        self.startT  = None
        self.endT    = None
        
        self.down    = None
        self.togo    = None
        self.quarter = None
        
        self.result   = None
        self.gain     = None
        self.turnover = None
        self.newdowns = None
        
        self.possession = None

        self.printType(debug)
        
    def setType(self, playtype):
        self.type = playtype
        
    def printType(self, debug=False):
        if debug:
            print("===> {0} Play".format(self.playtype))

############################################################################################################
## Penalty Play
############################################################################################################
class penaltyplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "penalty"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Penalty Specific
        self.penaltytype  = None
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = self.yds.penaltyyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult of {0} play is penaltyyards=={1}".format(self.name, self.result))
            
            
        
############################################################################################################
## Punt Play
############################################################################################################
class puntplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "punt"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.kicker = None
                
    def analyze(self, debug=False):
        self.pa.findPunt()
        self.yds.findYards()
        self.result = self.yds.kickingyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True])))

        
        
############################################################################################################
## Kickoff Play
############################################################################################################
class kickoffplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "kickoff"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.kicker = None
                
    def analyze(self, debug=False):
        self.pa.findKickoff()
        self.yds.findYards()
        self.result = self.yds.kickingyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 

        
############################################################################################################
## Field Goal Play
############################################################################################################
class fieldgoalplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "fieldgoal"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.kicker = None
                
    def analyze(self, debug=False):
        self.pa.findFieldGoal()
        self.yds.findYards()
        self.result = self.yds.kickingyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## PAT Play
############################################################################################################
class patplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "pat"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.kicker = None
                
    def analyze(self, debug=False):
        self.pa.findPAT()
        self.pa.touchdown = False
        self.yds.findYards()
        self.result = self.yds.kickingyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 

            

############################################################################################################
## Return Play
############################################################################################################
class returnplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "return"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.returner = None
                
    def analyze(self, debug=False):
        self.pa.findBasicKicking()
        self.pa.findBasicPlay()
        self.pa.findPassing()
        self.pa.findRushing()
        self.pa.findReturn()
        self.yds.findYards()
        self.result = self.yds.runbackyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Downs Play
############################################################################################################
class downsplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "downs"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = 0
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True])))
        

        
############################################################################################################
## TBD Play
############################################################################################################
class tbdplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "tbd"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.pa.findBasicKicking()
        self.yds.findYards()
        self.result = None
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## No Play
############################################################################################################
class noplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "no"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = 0
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Safety Play
############################################################################################################
class safetyplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "safety"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)

        ## Safety Specific
        self.rushing = None
        self.passing = None
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = self.yds.yards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Timeout Play
############################################################################################################
class timeoutplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "timeout"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = 0
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## End Play
############################################################################################################
class endplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "end"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = 0
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Begin Play
############################################################################################################
class beginplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "begin"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = 0
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Sack Play
############################################################################################################
class sackplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "sack"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.quarterback = None
                
    def analyze(self, debug=False):
        self.pa.findBasicPlay()
        self.yds.findYards()
        self.result = self.yds.playyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        
        


############################################################################################################
## Run Play
############################################################################################################
class rushingplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "rushing"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Running Back
        self.runningback = None
                
    def analyze(self, debug=False):
        self.pa.findRushing()
        self.yds.findYards()
        self.result = self.yds.playyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True])))    

            

        
############################################################################################################
## Pass Play
############################################################################################################
class passingplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "passing"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
        
        ## Players
        self.quarterback = None
        self.receiver    = None
                
    def analyze(self, debug=False):
        self.pa.findPassing()
        self.yds.findYards()
        self.result = self.yds.playyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        

        
############################################################################################################
## Fumble Play
############################################################################################################
class fumbleplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "fumble"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)

        ## Fumble Specific
        self.rushing = None
        self.passing = None
        
        ## Player Specific
        self.fumbler   = None
        self.recoverer = None
        self.turnover  = None
                
    def analyze(self, debug=False):
        self.pa.findReturn()
        self.yds.findYards()
        self.result = self.yds.playyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items() if v is True]))) 
        
        


############################################################################################################
## Touchdown Play
############################################################################################################
class touchdownplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "touchdown"
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.yds = playyards(text=text, playtype=self)
                
    def analyze(self, debug=False):
        self.pa.findReturn()
        self.yds.findYards()
        self.result = self.yds.playyards
        self.show(debug)

    def show(self, debug=False):
        if debug:
            print("\tResult is {0} play for {1} yards".format(self.name, self.result))
            #print("\t  Keys: {0}".format(", ".format([k for k,v in self.pa.__dict__.items()]))) # if v is True]))) 