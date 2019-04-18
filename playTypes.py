from playYards import playyards
from playAnalysis import playanalysis

# create logger
import logging
module_logger = logging.getLogger('log.{0}'.format(__name__))


############################################################################################################
### ## Football Play Type
############################################################################################################
class playtype:
    def __init__(self):
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 4*" "
        
        
    def getPlay(self, playText):
        self.logger.debug("{0}Finding Play Type for text [{1}]".format(self.ind, playText))
        
        play = None
        self.playtext = playText
        self.valid = True
        
        playSubText = playText
        pos = playText.rfind("(")
        if pos != -1 and pos > 5:
            playSubText = playText[:pos].strip()
            
        
        if sum([x in playSubText for x in ["field goal", "Field Goal", "Field goal", "FIELD GOAL", " fg ", " FG ", "MISSED FG", "Missed FG"]]) > 0:
            play = fieldgoalplay(playText)
        elif sum([x in playText for x in ["fake field goal", "Fake Field Goal"]]) > 0:
            play = fieldgoalplay(playText)
        elif sum([x in playSubText for x in ["timeout", "Timeout"]]) > 0:
            play = timeoutplay(playText)
        elif sum([x in playSubText for x in ["kickoff", "Kickoff", "kick off", "Kick Off", "Onside Kick", "Onside kick", "onside kick", "on-side kick", " kick for "]]) > 0:
            play = kickoffplay(playText)
        elif sum([x in playSubText for x in ["punt ", "PUNT", "Punt", " punted", " Punted", " punt,", " punter ", "punts "]]) > 0:
            play = puntplay(playText)
        elif playSubText.endswith(" punt"):
            play = puntplay(playText)
        elif sum([x in playSubText for x in ["end of the ", "End Of The ", "End of the ", "end of ", "End of ", "END OF "]]) > 0:
            play = endplay(playText)
        elif sum([x in playSubText for x in ["start of the ", "Start Of The ", "Start of the ", "Begin Drive", "start of ", "Start of ", "START OF "]]) > 0:
            play = beginplay(playText)
        elif sum([x in playSubText for x in ["SAFETY", "safety", "Safety"]]) > 0:
            play = safetyplay(playText)
        elif sum([x in playSubText for x in [" sack ", " sacked ", " Sack ", " Sacked ", "sacked,"]]) > 0:
            play = sackplay(playText)
        elif sum([x in playSubText for x in [" pass ", " passed ", " Pass ", " Passed ", " spikes ", " spiked ", " pass,to ",
                                          "Interception Return", "Interception", "INTERCEPTION"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText)
            elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
                play = penaltyplay(playText)
            elif sum([x in playSubText for x in ["Pass run"]]) > 0:
                play = rushingplay(playText)
            else:
                play = passingplay(playText)
        elif sum([x in playSubText for x in [" rush ", " rushed ", " Rush ", " Rushed ", " scramble", " rush,", " run ", " Run"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText)
            elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
                play = penaltyplay(playText)
            else:
                play = rushingplay(playText)
        elif sum([x in playSubText for x in ["penalty", "PENALTY", "Penalty", "Penalty,"]]) > 0:
            play = penaltyplay(playText)
        elif sum([x in playSubText for x in ["fumble", "Fumble", " fumbled ", " Fumble ", " Fumbled ", "FUMBLE"]]) > 0:
            if sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
                play = touchdownplay(playText)
            else:
                play = fumbleplay(playText)
        elif sum([x in playSubText for x in ["downs", "Downs", "DOWNS"]]) > 0:
            play = downsplay(playText)
        elif sum([x in playSubText for x in ["touchdown", "Touchdown", "TOUCHDOWN"]]) > 0:
            play = touchdownplay(playText)
        elif sum([x in playSubText for x in ["extra point", "Extra Point", "Extra point", "PAT", "2 point", "2 Point", "two-point", "Two-point", "Two-Point"]]) > 0:
            play = patplay(playText)
        elif sum([x in playSubText for x in ["NO PLAY", "No Play"]]) > 0:
            play = noplay(playText)
        elif len(playText) > 1:
            play = tbdplay(playText)
        elif len(playText) <= 1:
            play = tbdplay(playText)
        else:
            play = tbdplay(playText)

        return play
            
        
                
    def isValid(self):
        return self.valid
            
    def getPlayText(self):
        return self.playtext
                        

############################################################################################################
### ## Football Play Data
############################################################################################################
class footballplay:
    def __init__(self, playtype, text, debug=False):
        self.playtype = playtype.title()
        self.text     = text
        self.valid    = True
        
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
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Penalty Specific
        self.penaltytype  = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
            
            
        
############################################################################################################
## Punt Play
############################################################################################################
class puntplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "punt"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.pa.findPunt()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.kicker = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
        
############################################################################################################
## Kickoff Play
############################################################################################################
class kickoffplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "kickoff"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.pa.findKickoff()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.kicker = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))

        
############################################################################################################
## Field Goal Play
############################################################################################################
class fieldgoalplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "fieldgoal"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findFieldGoal()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.kicker = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## PAT Play
############################################################################################################
class patplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "pat"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findPAT()
        self.pa.touchdown = False
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.kicker = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))

            

############################################################################################################
## Return Play
############################################################################################################
class returnplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "return"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa  = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicKicking()
        self.pa.findBasicPlay()
        self.pa.findPassing()
        self.pa.findRushing()
        self.pa.findReturn()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## Downs Play
############################################################################################################
class downsplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "downs"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## TBD Play
############################################################################################################
class tbdplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "tbd"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## No Play
############################################################################################################
class noplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "no"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## Safety Play
############################################################################################################
class safetyplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "safety"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()

        ## Safety Specific
        self.rushing = None
        self.passing = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## Timeout Play
############################################################################################################
class timeoutplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "timeout"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        
        
        
############################################################################################################
## End Play
############################################################################################################
class endplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "end"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## Begin Play
############################################################################################################
class beginplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "begin"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))
        

        
############################################################################################################
## Sack Play
############################################################################################################
class sackplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "sack"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findBasicPlay()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.quarterback = None
        self.sacker = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))        
        


############################################################################################################
## Run Play
############################################################################################################
class rushingplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "rushing"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findRushing()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Running Back
        self.runningback = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))        
            

        
############################################################################################################
## Pass Play
############################################################################################################
class passingplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "passing"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findPassing()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        ## Players
        self.quarterback = None
        self.receiver    = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))        
        

        
############################################################################################################
## Fumble Play
############################################################################################################
class fumbleplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "fumble"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findReturn()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()

        ## Fumble Specific
        self.rushing = None
        self.passing = None
        
        ## Player Specific
        self.fumbler   = None
        self.recoverer = None
        self.turnover  = None
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))     
        
        


############################################################################################################
## Touchdown Play
############################################################################################################
class touchdownplay(footballplay):
    def __init__(self, text, debug=False):
        self.name = "touchdown"
        
        self.logger = logging.getLogger('log.{0}.{1}'.format(__name__, self.__class__))
        self.ind    = 6*" "
        self.logger.debug("{0}Creating [{1}] Play from text [{2}]".format(self.ind, self.name, text))
        
        self.text = text
        footballplay.__init__(self, self.name, text, debug)
        self.pa = playanalysis(text=text, playtype=self.name)
        self.pa.findReturn()
        
        self.yds = playyards(text=text, playtype=self)
        self.yds.findYards()
        
        self.logger.debug("{0}Result of {1} play ==> Keys: {2}".format(self.ind, self.name, self.pa.getKeys()))