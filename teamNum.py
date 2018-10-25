# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 11:03:45 2015

@author: tgadfort
"""


def stripTeamNum(line):
    pos1=line.find("src=\"")
    pos2=line.find(".png", pos1+1)
    logoaddr=line[pos1+5:pos2+4]
    pos=logoaddr.rfind("/")
    try:
        teamnum=int(logoaddr[pos+1:-4])
    except:
        print "Could not get team number",logoaddr
        f()
    return teamnum,logoaddr    
    
    
def getTeamNum(line):
    logoname="class=\"logo\">"
    if line.find(logoname) != -1:
        teamnum,logoaddr=stripTeamNum(line)
        return teamnum,logoaddr    
    return -1,"NoLogoAddr"

