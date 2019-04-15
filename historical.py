#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:31:11 2019

@author: tgadfort
"""

from os.path import join
from fsUtils import mkSubDir, setFile, isFile, removeFile, isDir
from ioUtils import getFile, saveFile
from fileUtils import getBaseFilename, getBasename, getDirname
from webUtils import getWebData, getHTML
from timeUtils import printDateTime, getDateTime, addMonths
from searchUtils import findExt
from time import sleep
from random import random
import re

from espngames import espn, output
from espngames import team, game, season


############################################################################################################
# Historical Class
############################################################################################################
class historical(espn, output):
    def __init__(self):
        self.name = "historical"
        espn.__init__(self)
        output.__init__(self)
        
        
        
        ## 2015
        self.noGameData2003 = ['232350023', '232400195', '232400254', '232402006', '232402050', '232412439', '232420021', '232420062', '232420167', '232420235', '232420248', '232420276', '232422005', '232422426', '232422440', '232422751', '232442132', '232470005', '232490068', '232490309', '232490349', '232492638', '232492649', '232492655', '232550276', '232560005', '232560036', '232560070', '232560167', '232560189', '232560202', '232560309', '232562005', '232562084', '232562572', '232562638', '232610023', '232630021', '232630036', '232630097', '232630202', '232630278', '232630349', '232632005', '232632006', '232632084', '232632426', '232632439', '232700036', '232700062', '232700068', '232700149', '232700167', '232700193', '232700235', '232700252', '232700278', '232700349', '232702084', '232702440', '232702638', '232702653', '232730151', '232770021', '232770036', '232770041', '232770058', '232770166', '232770167', '232770193', '232770202', '232770235', '232770242', '232772132', '232772309', '232772348', '232772426', '232772440', '232772567', '232820252', '232840005', '232840023', '232840062', '232840068', '232840070', '232840097', '232840254', '232840276', '232840328', '232842005', '232842006', '232842638', '232842655', '232890036', '232900097', '232910021', '232910202', '232910242', '232910248', '232910249', '232910349', '232912006', '232912084', '232912309', '232912348', '232912439', '232912567', '232912751', '232980021', '232980062', '232980068', '232980151', '232980202', '232980278', '232980328', '232982050', '232982084', '232982132', '232982426', '232982439', '232982440', '232982572', '232982655', '233040252', '233050005', '233050023', '233050166', '233050167', '233050235', '233050242', '233050276', '233052005', '233052426', '233052567', '233052572', '233052638', '233052649', '233052751', '233110167', '233120005', '233120087', '233120151', '233120195', '233120242', '233120248', '233122005', '233122032', '233122132', '233122348', '233122439', '233122440', '233122638', '233190036', '233190087', '233190097', '233190167', '233190202', '233190249', '233190254', '233190278', '233190328', '233190349', '233192006', '233192440', '233192567', '233192572', '233260021', '233260023', '233260058', '233260062', '233260070', '233260097', '233260235', '233260242', '233260252', '233262309', '233262426', '233262439', '233262655', '233262751', '233290166', '233320276', '233322132', '233330151', '233330154', '233330235', '233330248', '233332348', '233332638', '233332751', '233402426']
        self.noGameData2003 += ['232352306']
        self.noGameData2004 = ['242480068', '242480195', '242480242', '242480252', '242480276', '242482751', '242550058', '242550189', '242550235', '242550349', '242552005', '242552006', '242552426', '242552628', '242620023', '242620166', '242620202', '242620242', '242620248', '242622439', '242622440', '242690005', '242690021', '242690036', '242690166', '242690195', '242692567', '242692655', '242730276', '242742005', '242760023', '242760036', '242760058', '242760062', '242760235', '242760249', '242760349', '242762084', '242762132', '242762439', '242762649', '242812572', '242820252', '242830062', '242830195', '242830242', '242830278', '242830328', '242830349', '242832005', '242832006', '242832116', '242890005', '242900058', '242900189', '242900235', '242900252', '242902032', '242902116', '242902426', '242902439', '242902440', '242902567', '242902649', '242960036', '242970062', '242970195', '242970249', '242970276', '242972005', '242972006', '242972132', '242972393', '242972426', '242972440', '242972572', '242972628', '242972649', '242972655', '243040023', '243040036', '243040189', '243040202', '243040248', '243040276', '243040278', '243042132', '243042393', '243042426', '243042751', '243102006', '243110062', '243110070', '243110189', '243110242', '243110252', '243110349', '243112116', '243112439', '243112440', '243112655', '243142459', '243162032', '243170278', '243180005', '243180036', '243180058', '243180189', '243180195', '243180249', '243180252', '243182005', '243182050', '243182084', '243182567', '243182655', '243232032', '243250021', '243250062', '243250151', '243250167', '243250202', '243250276', '243250278', '243250349', '243252005', '243252132', '243252628', '243282116', '243282649', '243320023', '243322572', '243322628', '243340242', '243392426']
        self.noGameData2005 = ['252460008', '252460023', '252460066', '252460204', '252460258', '252462032', '252462567', '252530008', '252530084', '252530096', '252530239', '252600024', '252600025', '252600154', '252600264', '252600265', '252602005', '252670070', '252670238', '252672306', '252672567', '252740023', '252740062', '252740070', '252740204', '252770249', '252810008', '252810166', '252810328', '252812348', '252812440', '252880062', '252880068', '252880278', '252882440', '252950023', '252950154', '252952306', '253020068', '253020096', '253020204', '253020252', '253022306', '253022348', '253090068', '253090328', '253092440', '253160062', '253160070', '253160166', '253160238', '253160349', '253162032', '253230008', '253230023', '253230068', '253230152', '253230328', '253230349', '253232306', '253232426', '253232439', '253300023', '253300166', '253300249', '253302348']
        self.noGameData2006 = ['262440278', '262450084', '262450152', '262450264', '262452306', '262452509', '262520008', '262520059', '262520096', '262520239', '262520252', '262520258', '262522306', '262590070', '262590166', '262590258', '262590264', '262590265', '262590333', '262592348', '262660024', '262660145', '262660238', '262660239', '262660252', '262730096', '262730204', '262730238', '262730239', '262730328', '262800070', '262800328', '262870024', '262870265', '262870278', '262942032', '262942348', '262942440', '263010023', '263012306', '263012440', '263080070', '263080166', '263080204', '263080249', '263080265', '263080328', '263082393', '263082653', '263150062', '263150096', '263150264', '263150278', '263150309', '263152032', '263152226', '263152229', '263152440', '263220062', '263220096', '263220249', '263220276', '263220278', '263222348', '263222653', '263282348', '263290070', '263290145', '263290309', '263290328', '263292393', '263292433', '263360023', '263360166', '263360309', '263362229']
        self.noGameData2007 = ['272440009', '272440058', '272440150', '272440153', '272440195', '272440238', '272440242', '272440245', '272442226', '272442579', '272510012', '272510070', '272510167', '272510197', '272510218', '272510265', '272512567', '272580202', '272580204', '272580235', '272582032', '272650009', '272650021', '272650070', '272650195', '272650248', '272650249', '272652084', '272652638', '272702032', '272720008', '272720195', '272720197', '272720202', '272720248', '272790150', '272790218', '272792084', '272792309', '272792638', '272860005', '272860024', '272860036', '272860193', '272862032', '272862084', '272930005', '272930197', '272930218', '272930242', '273002084', '273002638', '273070005', '273070070', '273070145', '273070150', '273070193', '273070236', '273070242', '273072032', '273072633', '273140005', '273140167', '273140202', '273140276', '273142459', '273142567', '273210036', '273210098', '273210218', '273210242', '273210248', '273210333', '273212084', '273212348', '273212567', '273212638', '273280021', '273280070', '273280167', '273280242', '273280248', '273280276', '273282229', '273282459', '273352653']
        self.noGameData2008 = ['282430005', '282430012', '282430084', '282500012', '282500036', '282500070', '282500183', '282502032', '282570248', '282572032', '282642655', '282710218', '282712649', '282780166', '282782649', '282850021', '282990070', '282990249', '282992649', '283060258', '283062638', '283132393', '283250059', '283262649', '283270218', '283330218', '283412229']
        self.noGameData2009 = ['292460218', '292480193', '292480238', '292550249', '292622348', '292760021', '292762084', '292830218', '292830235', '292830265', '292832084', '292900195', '292970193', '293042638', '293180235', '293250023', '293312006', '293392348']        
        self.noGameData2010 = ['302452309', '302470103', '302472199', '302540077', '302540142', '302612638', 
                               '302680077', '302680183', '302820195', '302820249', '302890098', '302890249',
                               '302960070', '302962032', '303030062', '303032226', '303100249', '303172116', 
                               '303310278', '303312229', '303312653']            
        self.noGameData2011 = ['312462633', '312532006', '312600235', '312602439', 
                               '312670235', '312672653', '313160202', '313160235', '313302348']        
        self.noGameData2012 = ['322430328', '322450154', '322450167', '322520036', '322592572',
                               '322592638', '322662655', '322730113', '322732459', '322732655',
                               '322870195', '322872655', '323152006', '323220113']
        self.noGameData2013 = ['333580204']
        self.noGameData2014 = ['400548012', '400548062', '400548068', '400548080', '400548081',
                               '400548095', '400548125', '400548227', '400548409', '400547715',
                               '400547809', '400547919', '400548223', '400548269', '400548416']
        self.noGameData2015 = ['400787481', '400763646', '400763654', '400787345',
                               '400787363', '400787107', '400787357']
        self.noGameData2016 = ['400868914', '400868922', '400868930', '400868960', '400869143',
                               '400869274', '400869306', '400869182', '400869229', '400869241',
                               '400869370', '400869569', '400869156', '400869353', '400869383',
                               '400869390', '400869539', '400869819', '400869828', '400869842']
        self.noGameData2017 = ['400941794', '400944828', '400935239', '400944873', '400944860']
        self.noGameData2018 = []
        
        self.noGameData  = self.noGameData2003 + self.noGameData2004 + self.noGameData2005 + self.noGameData2006 + self.noGameData2007 + self.noGameData2008 + self.noGameData2009 
        self.noGameData += self.noGameData2010 + self.noGameData2011 + self.noGameData2012 + self.noGameData2013 + self.noGameData2014 + self.noGameData2015 + self.noGameData2016 
        self.noGameData += self.noGameData2017 + self.noGameData2018
                
        
        subdir    = "season"
        outputdir = mkSubDir(self.getSaveDir(), subdir)
        self.seasonDir = outputdir
        
        subdir    = "statistics"
        outputdir = mkSubDir(self.getSaveDir(), subdir)
        self.statisticsDir = outputdir
        
        subdir    = "results"
        outputdir = mkSubDir(self.getSaveDir(), subdir)
        self.resultsDir = outputdir
        
        subdir    = "games"
        outputdir = mkSubDir(self.getSaveDir(), subdir)
        self.gamesDir = outputdir
        
        
        subdir    = "season"
        outputdir = mkSubDir(self.getResultsDir(), subdir)
        self.seasonResultsDir = outputdir
        
        subdir    = "statistics"
        outputdir = mkSubDir(self.getResultsDir(), subdir)
        self.statisticsResultsDir = outputdir
        
        subdir    = "games"
        outputdir = mkSubDir(self.getResultsDir(), subdir)
        self.gamesResultsDir = outputdir
        
        
        
    def getSeasonDir(self):
        return self.seasonDir
    
    def getStatisticsDir(self):
        return self.statisticsDir
        
    def getGamesDir(self):
        return self.gamesDir
        
    def getResultsDir(self):
        return self.resultsDir

        
    def getSeasonResultsDir(self):
        return self.seasonResultsDir
        
    def getSeasonResultsFile(self, year):
        filename = setFile(self.getSeasonResultsDir(), "{0}.p".format(year))
        print(filename)
        return filename
        
    def getSeasonResultsData(self, year):      
        from espngames import team, game, season
        print("Getting {0}".format(self.getSeasonResultsFile(year)))
        data = getFile(self.getSeasonResultsFile(year), debug=True)
        return data

        
    def getStatisticsResultsDir(self):
        return self.statisticsResultsDir
        
    def getStatisticsResultsFile(self, year):
        filename = setFile(self.getStatisticsResultsDir(), "{0}-stats.json".format(year))
        print(filename)
        return filename
        
    def getStatisticsResultsData(self, year):        
        data = getFile(self.getStatisticsResultsFile(year))
        return data
    
    def getStatisticsAugmentedFile(self, year):
        filename = setFile(self.getStatisticsResultsDir(), "{0}-stats-extra.json".format(year))
        print(filename)
        return filename

    def getStatisticsAugmentedData(self, year):  
        data = getFile(self.getStatisticsAugmentedFile(year))
        return data
    
        
    def getGamesResultsDir(self):
        return self.gamesResultsDir
        
    def getGamesResultsFiles(self):
        files = findExt(self.getGamesResultsDir(), ext=".p", debug=False)
        return files
        
        
    def getYearlySeasonDir(self, year):
        outputdir = mkSubDir(self.getSeasonDir(), str(year))
        return outputdir
        
        
    def getYearlyStatisticsDir(self, year):
        outputdir = mkSubDir(self.getStatisticsDir(), str(year))
        return outputdir
        
        
    def getYearlyGamesDir(self, year):
        outputdir = mkSubDir(self.getGamesDir(), str(year))
        return outputdir
        
        
    
    ############################################################################################################
    # Team Standings + Games
    ############################################################################################################
    def downloadTeamStandingsByYear(self, year, debug=False):
        baseurl  = self.getBase()
        suburl   = "college-football/standings/_/season"
        url      = join(baseurl, suburl, str(year))
        
        savename  = setFile(self.getSeasonDir(), str(year)+".p")
        if isFile(savename):
            return
        
        if debug:
            print("Downloading {0}".format(url))        
        getWebData(base=url, savename=savename, useSafari=False)
        sleep(10+2*random())


    def downloadTeamStandings(self, startYear=2003, endYear=2018, debug=False):
        for year in range(startYear, endYear+1):
            self.downloadTeamStandingsByYear(year, debug)
        
        
    def downloadTeamDataByYear(self, idval, name, year, debug=False):
        baseurl  = self.getBase()
        suburl   = "college-football/team/schedule/_/id/{0}/season".format(idval)
        url      = join(baseurl, suburl, str(year))
        
        outputdir = self.getYearlySeasonDir(year)
        savename  = setFile(outputdir, "{0}-{1}.p".format(name, year))
        if isFile(savename):
            return
        
        if debug:
            print("Downloading {0} to {1}".format(url, savename))
        getWebData(base=url, savename=savename, useSafari=False)
        sleep(15+2*random())
            
            
    def parseAndDownloadTeamYearlyStandings(self):
        files = findExt(self.getSeasonDir(), ext=".p", debug=False)
        for ifile in files:
            year     = getBaseFilename(ifile)
            htmldata = getFile(ifile)
            bsdata   = getHTML(htmldata)
            
            idVals = {}
            links  = bsdata.findAll("a")
            for link in links:
                attrs = link.attrs
                if attrs.get("data-clubhouse-uid") is not None:
                    href  = attrs['href']
                    name  = getBasename(href)
                    idval = getBasename(getDirname(href))
                    
                    if idVals.get(idval) is not None:
                        if idVals[idval] != name:
                            raise ValueError("Error in ID for this year!")
                    idVals[idval] = name

            for idVal,name in idVals.items():
                self.downloadTeamDataByYear(idVal, name, season=str(year), debug=True)
    #http://www.espn.com/college-football/team/schedule/_/id/201/season/2005"
            
            
    def parseTeamYearlyStandings(self, startYear=2003, endYear=2018, debug=False, verydebug=False):
        for year in range(startYear, endYear+1):
            seasonDir = self.getYearlySeasonDir(year)
            files = findExt(seasonDir, ext=".p", debug=False)
            
            seasonData = season(year)
            
            for ifile in files:
                nameyear = getBaseFilename(ifile)
                htmldata = getFile(ifile)
                bsdata   = getHTML(htmldata)
                teamName = nameyear.replace("-{0}".format(year), "")
                
                
                metadata = bsdata.find("meta", {"property": "og:url"})
                if metadata is None:
                    raise ValueError("Could not find basic team meta data for this file! {0}".format(ifile))
                    
                try:
                    content = metadata.attrs['content']
                    year    = getBasename(content)
                    teamID  = getBasename(getDirname(getDirname(content)))
                except:
                    raise ValueError("Could not get team year and ID from meta data: {0}".format(metadata))
                    
                if verydebug:
                    print(year,'\t',teamID,'\t',ifile)
                
                
                ## Create Team Object
                teamData = team(year=year, teamName=teamName, teamMascot=None, teamID=teamID)
                
                tables = bsdata.findAll("table", {"class": "Table2__table"})
                if verydebug:
                    print("\tFound {0} game tables".format(len(tables)))
                for it,table in enumerate(tables):
                    trs = table.findAll("tr")
                    
                    headers = trs[1]
                    headers = [x.text for x in headers.findAll("td") if x is not None]
                    
                    gameRows = trs[2:]
                    totalGames = len(gameRows)
                    
                    if verydebug:
                        print("\tFound {0} potential games".format(totalGames))
                    
                    for ig,tr in enumerate(gameRows):
                        tds = tr.findAll("td")
                        gameData = dict(zip(headers, tds))
                        extra    = {"OT": False, "Bowl": False}
                        
                        
                        ## Get the Date
                        try:
                            date = gameData["Date"]
                        except:
                            print(ifile)
                            raise ValueError("No date for this game! {0}".format(gameData))                            
                        date = date.text
                        
                        ## Only Keep Games With Regular Dates
                        try:
                            dateval = "{0} {1}".format(date.split(", ")[-1], year)
                            date    = getDateTime(dateval)
                        except:
                            date    = None
                        
                        if date is None:
                            continue
                        
                        ## Check for January Games (in the following year)
                        if date.month == 1:
                            date = addMonths(date, 12)
                            
                        
                        ## Get the Opponent
                        try:
                            opponent = gameData["Opponent"]
                        except:
                            raise ValueError("No opponent for this game! {0}".format(game))   
                            
                        try:
                            oppolink = opponent.find("a")
                            oppohref = oppolink.attrs['href']
                            opponame = getBasename(oppohref)
                            oppoID   = getBasename(getDirname(oppohref))
                        except:
                            opponame = opponent.text
                            oppoID   = 0
                            #raise ValueError("Could not find href in link! {0}".format(opponent))


                        
                        try:
                            gamespan = opponent.find("span", {"class": "pr2"})
                            gametype = gamespan.text
                        except:
                            raise ValueError("Could not find game type from {0}".format(opponent))
                        
                        if gametype == "vs":
                            location = teamID
                        elif gametype == "@":
                            location = oppoID
                        else:
                            raise ValueError("Location --> {0}".format(gametype))
                            
                            
                        if verydebug:
                            print("\t{0}/{1}\t{2}\t{3: <4}{4: <50}".format(ig, totalGames, printDateTime(date), gametype, opponame), end="\t")


                        
                        ## Get the Result
                        try:
                            result = gameData["Result"]
                        except:
                            raise ValueError("No result for this game! {0}".format(game))
                            
                        spans = result.findAll("span")
                        if len(spans) == 0:
                            continue
                        if len(spans) != 2:
                            raise ValueError("There are {0} spans in this row!: {1}".format(len(spans), result))
                        outcome = spans[0].text.strip()
                        score   = spans[1].text.strip()
                        
                        if score.endswith("OT"):
                            extra = {"OT": True}
                            score = score[:-3].strip()
                            
                        try:
                            scores  = [int(x) for x in score.split('-')]
                        except:
                            raise ValueError("Could not create integer scores from {0}".format(spans))

                        if outcome == 'W':                            
                            teamScore  = scores[0]
                            oppoScore  = scores[1]
                            teamResult = "W"
                            oppoResult = "L"
                        elif outcome == "L":
                            teamScore = scores[1]
                            oppoScore = scores[0]
                            teamResult = "L"
                            oppoResult = "W"
                        elif outcome == "T":
                            teamScore = scores[0]
                            oppoScore = scores[1]
                            teamResult = "T"
                            oppoResult = "T"
                        else:
                            raise ValueError("Did not recognize game outcome {0}".format(outcome))


                        ## Get the Game
                        try:
                            gamelink = result.find("a")
                            gamehref = gamelink.attrs['href']
                        except:
                            raise ValueError("Could not find href in link! {0}".format(result))

                            
                        if verydebug:
                            print("{0}  {1}".format(teamResult, "-".join(str(x) for x in [teamScore,oppoScore])))
                            
                            
                        ## Create game object
                        gameData = game(gameID=gameID, date=date, teamA=teamID, teamB=oppoID,
                                        teamAResult=teamResult, teamBResult=oppoResult,
                                        teamAScore=teamScore, teamBScore=oppoScore, location=location)
                        
                        
                        ## Append game to team data
                        teamData.addGame(gameData)
                        

                ## Show Summary
                teamData.setStatistics()
                if debug:
                    teamData.summary()
                    if teamData.ngames == 0:
                        removeFile(ifile, debug=True)
                        
                seasonData.addTeam(teamData)
                
            #http://www.espn.com/college-football/team/schedule/_/id/201/season/2005"

            savename = setFile(self.getSeasonResultsDir(), "{0}.p".format(year))            
            saveFile(idata=seasonData, ifile=savename, debug=True)
                        
         
    ############################################################################################################
    # Team Games
    ############################################################################################################   
    def downloadGameDataByID(self, gameID, year, test=False, debug=False):        
        gamesDir   = self.getYearlyGamesDir(year)
        url="http://www.espn.com/college-football/playbyplay?gameId={0}".format(gameID)
        savename = setFile(gamesDir, "{0}.p".format(gameID))

        if isFile(savename):
            from os.path import getsize                    
            size = round(getsize(savename)/1e3)
            if size < 1:
                removeFile(savename, debug=True)

        if test:
            print("Downloading {0} to {1}".format(url,savename))
            return
        getWebData(base=url, savename=savename, dtime=6, useSafari=True, debug=True)
        sleep(6)
            
            
    def downloadGameData(self, debug=False, verydebug=False):
        resultsDir = self.getSeasonResultsDir()
        files = findExt(resultsDir, ext=".p", debug=False)

        gameType = "playbyplay"
        print("Sleeping for 5 seconds...")
        sleep(5)

        
        for ifile in files:
            seasonData = getFile(ifile)
            year       = seasonData.getYear()
            if year not in [2013,2014,2015]:
                continue
            gamesDir   = self.getYearlyGamesDir(year)
            
            teams = seasonData.teams
            for teamID,teamData in teams.items():
                teamGames = teamData.games
                for gameData in teamGames:
                    gameResult = gameData["Result"]
                    gameObject = gameData["Game"]
                    gameID     = gameObject.gameID
                    
                    if False:
                        prevLocation = "/Volumes/Seagate/Football/Games/Plays/{0}.html".format(gameID)
                        if isFile(prevLocation):
                            savename = setFile(gamesDir, "{0}.p".format(gameID))
                            if not isFile(savename) or True:
                                data = open(prevLocation, "rb").read()
                                saveFile(idata=data, ifile=savename, debug=True)
                                continue
                        continue

                    self.downloadGameDataByID(gameID, year, debug)
                        
                        
            
            
    def parseGameData(self, startYear=2003, endYear=2018, debug=False, verydebug=False):
        noData = {}
        for year in range(startYear, endYear+1):
            
            yearData = {}
            
            gamesDir = self.getYearlyGamesDir(year)        
            files    = findExt(gamesDir, ext=".p", debug=False)
            
            
            noData[year] = []
            for i,ifile in enumerate(files):
                gameID   = getBaseFilename(ifile)
                
                if gameID in self.noGameData:
                    continue
                
                htmldata = getFile(ifile)
                bsdata   = getHTML(htmldata)
                #print(bsdata)
                
                
                #verydebug=True
                #if gameID not in ['400603866']:
                #    continue
                
                teamData  = bsdata.findAll("div", {"class": "team-container"})
                
                longNames = [x.find("span", {"class": "long-name"}) for x in teamData]
                longNames = [x.text for x in longNames if x is not None]
                
                shortNames = [x.find("span", {"class": "short-name"}) for x in teamData]
                shortNames = [x.text for x in shortNames if x is not None]
                
                teamAbbrevs = [x.find("span", {"class": "abbrev"}) for x in teamData]
                teamNames   = [x.attrs for x in teamAbbrevs if x is not None]
                teamNames   = [x['title'] for x in teamNames]
                teamAbbrevs = [x.text for x in teamAbbrevs]
                
                teamIDs = [x.find("img", {"class": "team-logo"}) for x in teamData]
                teamIDs = [x.attrs for x in teamIDs if x is not None]
                teamIDs = [x['src'] for x in teamIDs]
                teamIDs = [re.search(r"(\d+).png", x) for x in teamIDs]
                teamIDs = [x.groups()[0] for x in teamIDs]

                awayTeam = {"Name": longNames[0], "Mascot": shortNames[0], "Abbrev": teamAbbrevs[0], "ID": teamIDs[0]}
                homeTeam = {"Name": longNames[1], "Mascot": shortNames[1], "Abbrev": teamAbbrevs[1], "ID": teamIDs[1]}
                
                    
                
                metadata = bsdata.find("meta", {"property": "og:title"})
                title    = None
                if metadata is not None:
                    title = metadata.attrs['content']
                    if verydebug:
                        print("==> {0}".format(title))
                
                ## Possesions
                posData = bsdata.find("ul", {"class": "css-accordion"})
                if posData is None:
                    posData = bsdata.find("article", {"class": "play-by-play"})
                if posData is None:
                    noData[year].append(gameID)
                    if verydebug:
                        print("Could not find possession data! {0}".format(gameID))
                    continue
                    #print(bsdata)
                    #1/0
                    #removeFile(ifile, debug)
                    #continue
                
                
                gameData = {"Teams": {"Away": awayTeam, "Home": homeTeam}, "Plays": []}

                if i % 10 == 0:
                    print("{0}/{1} with {2} no data games".format(i,len(files),len(noData[year])))
                
                    
                ###################
                ## Get Full Drive Data
                ###################

                drives = posData.findAll("li", {"class": "accordion-item"})
                if verydebug:
                    print("Drives {0}".format(len(drives)))

                for idr,drive in enumerate(drives):                                            

                    ## Get Drive Summary
                    headlines = [x.text.strip() for x in drive.findAll("span", {"class": "headline"})]
                    if verydebug:
                        print("Headlines {0}".format(len(headlines)))


                    ## Get Drive Details
                    details = [x.text.strip() for x in drive.findAll("span", {"class": "drive-details"})]
                    if verydebug:
                        print("Details {0}".format(len(details)))


                    ## Get Home Score
                    homescores = drive.findAll("span", {"class": "home"})
                    homescores = [x.find("span", {"class": "team-score"}) for x in homescores]
                    homescores = [x.text for x in homescores if x is not None]
                    if verydebug:
                        print("Home Scores {0}".format(len(homescores)))


                    ## Get Away Score
                    awayscores = drive.findAll("span", {"class": "away"})
                    awayscores = [x.find("span", {"class": "team-score"}) for x in awayscores]
                    awayscores = [x.text for x in awayscores if x is not None]
                    if verydebug:
                        print("Away Scores {0}".format(len(awayscores)))


                    ## Get Possession
                    possessions = drive.findAll("span", {"class": "home-logo"})
                    possessions = [x.find("img", {"class": "team-logo"}) for x in possessions]
                    possessions = [x.attrs['src'] for x in possessions if x is not None]
                    possessions = [x.split('&')[0] for x in possessions]
                    possessions = [getBaseFilename(x) for x in possessions]
                    if verydebug:
                        print("Possessions {0}".format(len(possessions)))


                    ## Check for valid headline (parsed correctly?)
                    if len(headlines) == 0:
                        continue
                        
                    validFGs    = ["Missed FG", "Field Goal", "FIELD GOAL", "MISSED FG", "Made FG",
                                   "Field Goal Good", "Field Goal Missed", "Blocked FG"]
                    validTDs    = ["Touchdown", "TOUCHDOWN", "END OF HALF Touchdown", "Downs Touchdown",                                  
                                   "Missed FG Touchdown", "End of Half Touchdown", "End of Game Touchdown", 
                                   "PUNT Touchdown", "FUMBLE Touchdown", "INTERCEPTION Touchdown",
                                   "FIELD GOAL Touchdown", "MISSED FG Touchdown", "Rushing Touchdown", "Passing Touchdown",
                                  "Kickoff Return Touchdown", "Interception Return Touch", "Turnover on Downs Touchdown",
                                  "Field Goal Missed Touchdown", "Field Goal Touchdown", "Rushing Touchdown Touchdown",
                                  "Field Goal Good Touchdown", "Passing Touchdown Touchdown",
                                   "Fumble Return Touchdown Touchdown", "Rushing TD", "Passing TD",
                                   "Blocked Punt TD", "Punt Return TD", "Fumble Ret. TD",
                                   "Interception TD", "Fumble TD", "Rushing TD Touchdown",
                                   "Blocked Punt TD Touchdown", "Blocked FG (TD)",
                                   "Punt Return TD Touchdown", "Kick Return TD",
                                   "Kickoff Return Touchdown Touchdown",
                                   "Missed FG (TD) Touchdown", "Blocked FG (TD) Touchdown",
                                   "Punt Return Touchdown Touchdown", "Interception Return Touch Touchdown"]
                    validEnds   = ["End of Half", "End of Game", "END OF HALF", "END OF GAME", "End of 4th Quarter"]
                    validTOs    = ["Fumble", "Interception", "FUMBLE", "INTERCEPTION", "Kickoff", "KICKOFF",
                                  "Blocked Punt"]
                    validTOPnts = ["Interception Touchdown", "Safety", "Punt Touchdown", "Fumble Touchdown",
                                   "Punt Return Touchdown", "Fumble Return Touchdown", "SAFETY"]
                    validDowns  = ["Punt", "Downs", "PUNT", "Possession (For OT Drives)", "DOWNS",
                                   "Possession (For OT Drives) Touchdown", "Turnover on Downs",
                                  "Poss. on downs", "Penalty"]
                    validPlay   = ["Rush", "Pass", "Sack", "Timeout", "Incomplete", "Pass Complete"]
                    valid2PT    = ["2PT Pass failed", "Missed PAT Return"]
                    validOdds   = ["on-side kick"]
                    validHeadlines  = validFGs + validTDs + validEnds + validTOs + validTOPnts + validDowns + validPlay + valid2PT
                    isValidHeadline = sum([x in validHeadlines for x in headlines])
                    if headlines[0] == '':
                        continue
                    if isValidHeadline == 0 and idr < len(drives) - 1:
                        print(idr,'/',len(drives))
                        print(title)
                        print(ifile)
                        #print(bsdata)
                        raise ValueError("No valid headline in {0}".format(headlines))
                        print("No valid headline in {0}".format(headlines))
                        continue


                    ## Analyze Play-by-Play
                    try:
                        driveList = drive.find("ul", {"class": "drive-list"})                        
                        plays = driveList.findAll("li")
                    except:
                        raise ValueError("Could not find drive list in drive {0}".format(drive))

                    driveData = []
                    for ip,play in enumerate(plays):

                        ## Check for Starting Position
                        startPos = play.find("h3")
                        if startPos is None:
                            raise ValueError("Could not find Starting Position in Play! {0}".format(play))
                        startData = startPos.text.strip()


                        ## Check for Play Text
                        span = play.find("span", {"class": "post-play"})
                        if span is None:
                            raise ValueError("Could not find post play data! {0}".format(play))
                        playData = span.text.strip()


                        driveData.append({"Play": ip, "Start": startData, "Data": playData})

                        #print(idr,'\t',ip,'\t',startData,'\t',playData)


                    ## Save Drive Data
                    gameData["Plays"].append({"Drive": len(gameData), "Headline": headlines, "Detail": details, 
                                              "HomeScore": homescores, "AwayScore": awayscores,
                                              "Possession": possessions, "Data": driveData})



                    if verydebug:
                        print(idr,'\t',headlines)
                        print(idr,'\t',details)
                        print(idr,'\t',homescores)
                        print(idr,'\t',awayscores)
                        print(idr,'\t',possessions)
                        print("")

                if verydebug:
                    print("Found {0} drives for gameID {1}".format(len(gameData), gameID))
                yearData[gameID] = gameData
                
            print("Parsed {0}/{1} games in {2}".format(len(yearData), len(files), year))
            savename = setFile(self.getGamesResultsDir(), "{0}-games.p".format(year))
            saveFile(idata=yearData, ifile=savename, debug=True)
            
        return noData

        

            
        
        
    
    ############################################################################################################
    # Team Statistics
    ############################################################################################################
    def downloadTeamStatisticsDataByYear(self, idval, name, year, debug=False):
        baseurl  = self.getBase()
        suburl   = "college-football/team/stats/_/id/{0}/season".format(idval)
        url      = join(baseurl, suburl, str(year))
        
        outputdir = self.getYearlyStatisticsDir(year)
        savename  = setFile(outputdir, "{0}-{1}.p".format(name, year))
        if isFile(savename):
            return
        
        if debug:
            print("Downloading {0} to {1}".format(url, savename))
        getWebData(base=url, savename=savename, useSafari=False)
        sleep(15+2*random())        
        
        
    def downloadTeamStatisticsData(self, debug=False):
        resultsDir = self.getSeasonResultsDir()
        files = findExt(resultsDir, ext=".p", debug=False)

        sleep(3)
        
        for ifile in files:
            seasonData = getFile(ifile)
            year       = seasonData.getYear()
            gamesDir   = self.getYearlyGamesDir(year)
            
            if year != 2014:
                continue
            
            teams = seasonData.teams
            for teamID,teamData in teams.items():
                name = teamData.teamName
                self.downloadTeamStatisticsDataByYear(teamID, name, year, debug)
                

    def parseTeamStatisticsData(self, startYear=2014, endYear=2018, debug=False, verydebug=False):
        for year in range(startYear, endYear+1):
            
            yearData = {}
            
            statsDir = self.getYearlyStatisticsDir(year)        
            files    = findExt(statsDir, ext=".p", debug=False)
            
            
            for i,ifile in enumerate(files):
                teamStatistics = {}

                print(ifile)
                htmldata = getFile(ifile)
                bsdata   = getHTML(htmldata)
                
                divs       = bsdata.findAll("div", {"class": "Table2__Title"})
                tableNames = [x.text for x in divs]
                
                tables = bsdata.findAll("table", {"class": "Table2__table__wrapper"})
                
                ## Skip the team leaders table
                tableNames = tableNames[1:]
                #tables     = tables[1:]
                if len(tables) != len(tableNames):
                    for it,table in enumerate(tables):
                        ths     = table.findAll("th")
                        headers = [x.text for x in ths]
                        print(it,headers)
                        
                    raise ValueError("There are {0} tables and {1} names".format(len(tables), tableNames))
                #print("  Found {0} tables and {1} names".format(len(tables), len(tableNames)))
                
                    
                    
                tableData = dict(zip(tableNames, tables))                
                for tableName, table in tableData.items():
                    ths     = table.findAll("th")
                    headers = [x.text for x in ths]
                    
                    trs     = table.findAll("tr")[2:]
                    
                    players = {}
                    iData   = -1
                    for tr in trs:
                        linedata = [x for x in tr.strings]
                        
                        ## Get player first
                        if len(linedata) == 3:
                            try:
                                name     = linedata[0]
                                position = linedata[2]
                            except:
                                raise ValueError("Could not parse line data: {0}".format(linedata))
                                
                            key = ":".join([name,position])
                            players[key] = None
                        elif len(linedata) == 1:
                            players["TOTAL:ALL"] = None
                            playerNames = list(players.keys())
                        elif len(linedata) == len(headers) - 1:
                            if iData == -1:
                                header = linedata
                                iData += 1
                                continue
                            else:
                                try:
                                    playerData = dict(zip(header, linedata))
                                except:
                                    raise ValueError("Could not combine header [{0}] with data [{1}]".format(header, linedata))
                                    
                            try:
                                players[playerNames[iData]] = playerData
                            except:
                                raise ValueError("Could not set data for [{0}] with data: {1}".format(iData,playerData))
                            #print(iData,'\t',playerNames[iData],'\t',playerData)
                            iData += 1
                            
                    #print(tableName,'-->',players)
                    teamStatistics[tableName] = players

            yearData[year] = teamStatistics
                
            print("Parsed {0}/{1} games in {2}".format(len(yearData), len(files), year))
            savename = setFile(self.getStatisticsResultsDir(), "{0}-stats.p".format(year))
            saveFile(idata=yearData, ifile=savename, debug=True)


