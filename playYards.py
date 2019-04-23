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
        
        assert self.findKickoffYards("Joseph Bulovas kickoff for 63 yds , Hassan Hall return for 61 yds to the Alab 37") == 63, "Should be 63"
        assert self.findKickReturnYards("Joseph Bulovas kickoff for 63 yds , Hassan Hall return for 61 yds to the Alab 37") == 61, "Should be 61"
        assert self.findKickoffYards("Evan O'Hara kickoff for 65 yds for a touchback") == 65, "Should be 65"
        assert self.findKickReturnYards("Evan O'Hara kickoff for 65 yds for a touchback") == 25, "Should be 25"
        assert self.findPuntYards("Skyler DeLong punt for 32 yds, downed at the Lvile 15") == 32, "Should be 32"
        assert self.findKickReturnYards("Skyler DeLong punt for 32 yds, downed at the Lvile 15") == 0, "Should be 0"
        assert self.findPenaltyYards("ALABAMA Penalty, Delay of Game (-5 Yards) to the Lvile 9") == -5, "Should be -5"
        
        
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
                self.yards = None
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
                    result = [int(result[0])*sign]
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
    ## Find Punt Yardage
    ############################################################################################################
    def findPuntYards(self, text):
        kick = ("(punt|Punt|PUNT)")
        prep = ("(for|For|FOR|or|Or|OR)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yard|Yard|YARD|yd|Yd|YD)")
        
        m = re.search(r"{0}\s{1}\s{2}\s{3}".format(kick, prep, num, dist), text)
        if m is not None:
            result = m.groups(0)
            yards  = int(result[2])
            return yards
        return None
        
        
    ############################################################################################################
    ## Find Kickoff Yardage
    ############################################################################################################
    def findKickoffYards(self, text):
        kick = ("(kickoff|Kickoff|KICKOFF)")
        prep = ("(for|For|FOR)")
        num  = "([+-?]\d+|\d+)"  
        dist = ("(yard|Yard|YARD|yd|Yd|YD)")
        
        m = re.search(r"{0}\s{1}\s{2}\s{3}".format(kick, prep, num, dist), text)
        if m is not None:
            result = m.groups(0)
            yards  = int(result[2])
            return yards
        return None
        
        
    ############################################################################################################
    ## Find Kick Return Yardage
    ############################################################################################################
    def findKickReturnYards(self, text):
        kick = "(return|Return|RETURN|returns|Returns|RETURNS)"
        prep = "(for|For|FOR)"
        num  = "([+-?]\d+|\d+)"  
        dist = "(yard|Yard|YARD|yd|Yd|YD)"

        if "fair catch" in text:
            return 0
        
        if "downed at the" in text:
            return 0
        
        if "no gain" in text:
            return 0
        
        if "touchback" in text:
            return 25
        
        m = re.search(r"{0}\s{1}\s{2}\s{3}".format(kick, prep, num, dist), text)
        if m is not None:
            result = m.groups(0)
            yards  = int(result[2])
            return yards
        
        if "return" not in text:
            return 0
        
        return None


    ############################################################################################################
    ## Find Penalty Yardage
    ############################################################################################################
    def findPenaltyYards(self, text):
        num    = "([+-?]\d+|\d+)"  
        dist   = "(yard|Yard|YARD|yd|Yd|YD)"
        
        pos  = text.find("(")
        if pos > 0:
            text = text[pos:text.find(")")]
            m = re.search(r"{0}\s{1}".format(num, dist), text)
            if m is not None:
                result = m.groups(0)
                yards  = int(result[0])
                return yards

        if "declined" in text:
            return 0
        
        return None
        


        
    ############################################################################################################
    ## Find Kicking Yardage
    ############################################################################################################
    def findKickingYards(self, text):
        return
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