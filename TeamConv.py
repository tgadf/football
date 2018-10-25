# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 11:01:33 2015

@author: tgadfort
"""
def fillConv():    
    convs={}
    convs["Miami (FL)"] = "Miami (Florida)"
    convs["Miami (OH)"] = "Miami (Ohio)"
    convs["Florida Intl"] = "Florida International"
    convs["UCF"] = "Central Florida"
    convs["San José State"] = "San Jose State"
    convs["San Jos\xe9 State"] = "San Jose State"
    convs["UNLV"] = "Nevada-Las Vegas"
    convs["Kent State"] = "Kent"
    convs["BYU"] = "Brigham Young"
    convs["LSU"] = "Louisiana State"
    convs["Louisiana Monroe"] = "Louisiana-Monroe"
    convs["Louisiana Lafayette"] = "Louisiana-Lafayette"
    convs["TCU"] = "Texas Christian"
    convs["MTSU"] = "Middle Tennessee State"
    convs["Middle Tennessee"] = "Middle Tennessee State"
    convs["SMU"] = "Southern Methodist"
    convs["UTEP"] = "Texas-El Paso"
    convs["Texas San Antonio"] = "Texas-San Antonio"
    convs["BGSU"] = "Bowling Green State"
    convs["Bowling Green"] = "Bowling Green State"
    #convs["NCSU"] = "North Carolina State"
    convs["NC State"] = "North Carolina State"
    convs["USC"] = "Southern California"
    convs["Ole Miss"] = "Mississippi"
    
    convs["Presbyterian College"] = "Presbyterian"
    convs["The Citadel"] = "Citadel"
    convs["UC Davis"] = "California-Davis"
    convs["VMI"] = "Virginia Military Institute"
    convs["Stephen F Austin"] = "Stephen F. Austin"
    
    invconvs={}
    for k,v in convs.iteritems():
        invconvs[v] = k
    return convs, invconvs

def InvTeamConv(team):
    convs, invconvs = fillConv()
    if invconvs.get(team):
        return invconvs[team]
    return team
    
def TeamConv(team):
    convs, invconvs = fillConv()
    if convs.get(team):
        return convs[team]
    return team