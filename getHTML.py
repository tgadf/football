# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:44:29 2015

@author: tgadfort
"""


import requests
import urllib2


def checkURL(url):
    try:
        urllib2.urlopen(url)
        return True
    except urllib2.HTTPError:
        return False


def getHTML(url, savename):
    if checkURL(url):
        page  = requests.get(url)
        f = open(savename, "w")
        f.write(page.text)
        f.close()
        return True
    else:
        return False