#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:39:51 2019

@author: tgadfort
"""


from playbyplay import playbyplay
from historical import historical
from espngames import season, game, team

hist = historical()
print(hist)

pbp = playbyplay()
pbp.setHistorical(hist)
pbp.parseGames(gameID=None, test=False, debug=False, verydebug=False)


print(len(pbp.badGames.keys())+len(pbp.goodGames.keys()))
print(len(pbp.badGames.keys()))
print(pbp.badGames.keys())


def writeEdit(gameID, driveNo, playNo, text=None):
    print("        if gameID == '{0}':".format(gameID))
    print("            if driveNo == {0} and playNo == {1}:".format(driveNo, playNo))
    if text is not None:
        print("                newtext = \"{0}\"".format(text))
    else:
        print("                keep = False")

        

writeEdit(401021670, 22, 3, "Cephus Johnson pass intercepted for a TD Alvin Ward Jr. return for 28 yds for a TD, (Tyler Bass KICK)")

