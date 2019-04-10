import re

############################################################################################################
## Play Text Yardage Play
############################################################################################################
class playyards:
    def __init__(self, text=None, playtype=None, test=False):
        self.text     = text
        self.playtype = playtype
        self.test     = test
        
        self.playyards    = None
        self.kickingyards = None
        self.runbackyards = None
        self.penaltyyards = None
        
        self.yards = None
        
    def setPlay(self, text):
        self.text = text
        
    def setPlayType(self, playtype):
        self.playtype = playtype
        
    def makeYards(self, yards, debug=False):
        if self.test:
            return yards
        
        if yards == "NET" or yards == "IGN":
            return yards
        
        if yards == None:
            return None
        
        try:
            result = int(yards)
        except:
            raise ValueError("Could not extract yards from [{0}] play with [{1}] text".format(yards, self.text))
            
        return result
        
        
    def show(self, yards, caller, debug=False):            
        if debug:
            print("\t\t===> {0} Yards -> [{1}]".format(caller, yards))
            
    
    ############################################################################################################
    ## Find Play Yardage
    ############################################################################################################
    def findYards(self, debug=False):
        sign   = 1
        result = None
        
        self.findPenaltyYards(debug)
        self.findKickingYards(debug)
        self.findReturnYards(debug)
        self.findPlayYards(debug)
        
        yards = [self.playyards, self.kickingyards, self.runbackyards, self.penaltyyards]
        if not len([x for x in yards if x is not None]):
            if self.test is True:
                if debug:
                    print("Could not find yards in this play")
                self.yards = None
            else:
                raise ValueError("Could not find any yards for this play: [{0}]".format(self.text))
        else:
            if any([isinstance(x, int) for x in yards]):
                self.yards = sum([x for x in yards if (x is not None) and (isinstance(x, int))])
            elif any([isinstance(x, str) for x in yards]):
                self.yards = ", ".join([x for x in yards if (x is not None) and (isinstance(x, str))])
            else:
                self.yards = None
            


    
    ############################################################################################################
    ## Find Play Yardage
    ############################################################################################################
    def findPlayYards(self, debug=False):
        sign   = 1
        result = None
        start  = self.text
        
        prep = ("(or|for)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
        
        #################################################################
        ### Check for yards
        #################################################################
        if result is None:
            if sum([x in self.text for x in ["no gain", "no loss", "DECLINED"]]) > 0:
                result = [0]
                if debug:
                    print("\t\t===> {0}".format(result))      

        if result is None:
            if sum([x in self.text for x in ["loss of zero", "gain of zero"]]) > 0:
                result = [0]
                if debug:
                    print("\t\t===> {0}".format(result))                

        if result is None:
            m = re.search(r"{0}\s{1}\s{2}".format(prep, num, dist), self.text)
            if m is not None:
                result = m.groups(0)
                result = result[1:]
                if debug:
                    print("\t\t===> {0}".format(result))        
        
        if result is None:
            m = re.search(r"\w+\s(-\d+)\s\w+", self.text)
            if m is not None:
                result = m.groups(0)                
                if debug:
                    print("\t\t===> {0}".format(result))

        if result is None:
            m = re.search(r"for\sa\s(\w+)\sof\s(\d+)\s{0}".format(dist), self.text)
            if m is not None:
                results = m.groups()
                sign    = results[0]
                result  = results[1:]
                if sign == "loss":
                    sign = -1
                if debug:
                    print("\t\t===> {0} ({1})".format(result, sign))
        
        if result is None:
            pattern = r"{0}\s{1}\spenalty".format(num, dist)
            m = re.search(pattern, self.text)
            if m is not None:
                sign   = -1
                result = m.groups()
                if debug:
                    print("\t\t===> {0}".format(result))
        
        if result is None:
            if sum([x in self.text for x in ["incomplete", "Incomplete"]]) > 0:
                result = [0]
                if debug:
                    print("\t\t===> {0}".format(result))
        
        if result is None:
            if sum([x in self.text for x in [" no gain", " No Gain", "failed"]]) > 0:
                result = [0]
                if debug:
                    print("\t\t===> {0}".format(result))
        
        if result is None:
            m = re.search(r"{0}\s{1}".format(num, dist), self.text)
            if m is not None:
                result = m.groups()
                if debug:
                    print("\t\t===> {0}".format(result))

        if result is None:
            result = [None]
        self.playyards = self.makeYards(result[0])
        self.show(self.runbackyards, "Drive", debug=debug)

        
        

    ############################################################################################################
    ## Find Penalty Yardage
    ############################################################################################################
    def findPenaltyYards(self, debug=False):
        kick = ("(punt|kickoff)")
        prep = ("(or|for)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
        yards = None
        
        ## False Start
        if sum([x in self.text for x in ["False Start"]]) > 0:
            yards = -5
            
        ## Offensive Pass Interference
        if sum([x in self.text for x in ["Offensive Pass Interference"]]) > 0:
            yards = "NET"
            
        ## Offensive Pass Interference
        if sum([x in self.text for x in ["Defensive Pass Interference"]]) > 0:
            yards = "NET"
            
        ## Offensive Pass Interference
        if sum([x in self.text for x in ["Illegal Block"]]) > 0:
            yards = "NET"


        if yards is None:
            yards = "IGN"
        
            

        self.penaltyyards = self.makeYards(yards)
        self.show(self.runbackyards, "Penalty", debug=debug)


        
    ############################################################################################################
    ## Find Kicking Yardage
    ############################################################################################################
    def findKickingYards(self, debug=False):
        kick = ("(punt|kickoff)")
        prep = ("(or|for)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yards|yard|Yds|yds|Yd|yd)")
        
        yards = None
        
        if yards is None:
            m = re.search(r"{0}\s{1}\s{2}\s{3}".format(kick, prep, num, dist), self.text)
            if m is not None:
                result = m.groups(0)
                yards  = result[2]

        self.kickingyards = self.makeYards(yards)
        self.show(self.kickingyards, "Kicking", debug=debug)


        
    

    ############################################################################################################
    ## Find Return Yardage
    ############################################################################################################
    def findReturnYards(self, debug=False):
        runback  = "(return|runback|returns)"
        norun    = "(downed|down)"
        prep     = "(or|for|at)"
        article  = "(the|a)"
        num      = "([+-?]\d+|\d+)"
        word     = "(\w+)"
        dist     = "(yards|yard|Yds|yds|Yd|yd)"
        
        yards = None
            
        if yards is None:
            m = re.search(r"{0}\s{1}\s{2}\s{3}".format(runback, prep, num, dist), self.text)
            if m is not None:
                result = m.groups(0)
                yards  = result[2]
        
        if yards is None:
            m = re.search(r"{0}\s{1}\s{2}\s{3}\s{4}".format(norun, prep, article, word, num), self.text)
            if m is not None:
                result = m.groups(0)
                yards  = 0
                    
        if yards is None:
            if sum([x in self.text for x in ["fair catch", "Fair Catch"]]) > 0:
                yards = 0

        self.runbackyards = self.makeYards(yards)
        self.show(self.runbackyards, "Return", debug=debug)