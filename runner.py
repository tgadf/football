#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:39:51 2019

@author: tgadfort
"""

import argparse

parser = argparse.ArgumentParser(description='Example with long option names')
parser.add_argument('--id', action="store", dest="gameID")
results = parser.parse_args()

from playbyplay import playbyplay
from historical import historical
from espngames import season, game, team

import logging

logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('results.log', mode='w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

#logging.basicConfig(filename='parsing.log', level=logging.INFO)
logger.info('creating a logger message')

hist = historical()
print(hist)

logger.info('done creating a logger message')

pbp = playbyplay()
pbp.setHistorical(hist)
gameID = results.gameID
print("GameID set to [{0}]".format(gameID))
pbp.parseGames(gameID=gameID, test=False, debug=False, verydebug=False)


print("Bad + Good: ",len(pbp.badGames.keys())+len(pbp.goodGames.keys()))
print("Bad: ",len(pbp.badGames.keys()))
print("Games: ",pbp.badGames.keys())


def writeEdit(gameID, driveNo, playNo, text=None):
    print("        if gameID == '{0}':".format(gameID))
    print("            if driveNo == {0} and playNo == {1}:".format(driveNo, playNo))
    if text is not None:
        print("                newtext = \"{0}\"".format(text))
    else:
        print("                keep = False")

