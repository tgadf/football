class penalty:
    def __init__(self, text=None):
        self.text = text
        
        yards = None
        penaltytype = None
        
        ## False Start
        if sum([x in self.text for x in ["False Start"]]) > 0:
            yards = -5
            penaltytype = "FalseStart"
            
        ## Offensive Pass Interference
        if sum([x in self.text for x in ["Offensive Pass Interference"]]) > 0:
            yards = "NET"
            penaltytype = "OffensivePassInterference"
            
        ## Defensive Pass Interference
        if sum([x in self.text for x in ["Defensive Pass Interference"]]) > 0:
            yards = "NET"
            penaltytype = "DefensivePassInterference"
            
        ## Defensive Pass Interference
        if sum([x in self.text for x in ["Defensive Offside"]]) > 0:
            yards = 5
            penaltytype = "DefensiveOffside"
            
        ## Offensive Pass Interference
        if sum([x in self.text for x in ["Illegal Block"]]) > 0:
            yards = "NET"
            penaltytype = "IllegalBlock"

        self.yards = yards
        self.penaltytype = penaltytype
        
    def isPenalty(self, returnYards=False):
        if self.penaltytype is None:
            if returnYards:
                return 0
            else:
                return False
        else:
            if returnYards:
                return self.yards
            else:
                return True