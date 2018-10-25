from lxml import html
import requests
import json
import csv



def TeamConv(team):
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
    convs["NCSU"] = "North Carolina State"
    convs["NC State"] = "North Carolina State"
    convs["USC"] = "Southern California"
    convs["Ole Miss"] = "Mississippi"
    
    convs["Presbyterian College"] = "Presbyterian"
    convs["The Citadel"] = "Citadel"
    convs["UC Davis"] = "California-Davis"
    convs["VMI"] = "Virginia Military Institute"
    convs["Stephen F Austin"] = "Stephen F. Austin"
    if convs.get(team):
        return convs[team]
    return team


##########################################
#
# This is the output line to the csv file
#
##########################################
def writeLine(outfile, Date, Team1, Team2, Score1, Score2, Winner):
    lout=[]
    lout.append(Date)
    lout.append(Team1)
    lout.append(Team2)
    lout.append(Score1)
    lout.append(Score2)
    lout.append(Winner)
    lout=[str(x) for x in lout]
    outfile.write(",".join(lout))
    outfile.write("\n")
    


##########################################
#
# Write file based on start/end date
#
##########################################
def writeAbrvFile(fname, abrvdata):
    f=open(fname, "w")
    nline = 0
    teams = sorted(abrvdata.keys())
    for team in teams:
        abrv = abrvdata[team]["Abrv"]
        city = abrvdata[team]["City"]
        state = abrvdata[team]["State"]

        f.write(team+"\t"+city+"\t"+state+"\t"+abrv+"\n")
        nline += 1
    print "\tWrote",nline,"lines to",fname
    f.close()

def writeConfFile(fname, yeardata):
    f=open(fname, "w")
    teams=sorted(yeardata.keys())
    nline = 0
    for team in teams:
        conf = yeardata[team]["conf"]
        f.write(team+"\t"+conf+"\n")
        nline += 1
    print "\tWrote",nline,"lines to",fname
    f.close()
    

def writeGraphFile(fname, yeardata):
    f=open(fname, "w")
    teams=sorted(yeardata.keys())
    nline=0
    for team in teams:
        games = yeardata[team]["games"]
        opponents=[]
        opponents.append(team)
        for game in games:
            opponent = game['opponent']
            f.write(team+"\t"+opponent+"\n")
            nline += 1
    print "\tWrote",nline,"lines to",fname
    f.close()


def writeFile(fname, yeardata):
    f=open(fname, "w")
    writeLine(f, "Date", "Team1", "Team2", "Score1", "Score2", "Winner")
    nline=0
    teams=sorted(yeardata.keys())
    for team in teams:
        games = yeardata[team]["games"]
        for game in games:
            if game['result'] == 'W':
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], team)
            elif game['result'] == 'L':
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], game['opponent'])
            else:
                writeLine(f, game['date'], team, game['opponent'], game['score'], game['against'], team)
            nline += 1
    print "\tWrote",nline,"lines to",fname
    f.close()




def getScores(htm, txt):
    page  = requests.get('http://www.jhowell.net/cf/scores/Sked2015.htm')
    fname = txt
    f = open(fname, "w")
    f.write(page.text)
    f.close()


def getAbrv(htm, txt):
    page  = requests.get('https://en.wikipedia.org/wiki/List_of_colloquial_names_for_universities_and_colleges_in_the_United_States')
    fname = txt
    f = open(fname, "w")
    f.write(page.text)
    f.close()


def getName(line):
    pos = line.find("<p align=\"center\">")
    if pos == -1:
        print "Could not parse:",line
        exit()
    name = line[pos+18:]
    
    pos = name.rfind("(")
    conf = name[pos:]
    conf = conf.replace("(", "")
    conf = conf.replace(")", "")
    name = name[:pos-1]
    return name,conf


def getGame(line):
    line = line.replace("<td align=\"right\">", ":")
    line = line.replace("<td>", ":")
    line = line.replace("<tr>", "")
    linevals = line.split(":")
    site = None
    if len(linevals) == 8:
        try:
            dummy,date,day,home,opp,res,score,against = linevals
        except:
            print "SPLIT ERROR:",line
            exit()
    elif len(linevals) == 9:
        try:
            dummy,date,day,home,opp,res,score,against,site = linevals
        except:
            print "SPLIT ERROR:",line
            exit()

    opp = opp.replace("*", "")
    if home == "vs.":
        home = 1
    elif home == "@":
        home = -1
    else:
        print "ERROR with Home:",home
        exit()
    if site != None:
        home = 0

    if len(res) == 0:
        return None

    try:
        game={}
        game['date'] = date
        game['day'] = day
        game['home'] = home
        game['opponent'] = opp
        game['result'] = res
        game['score'] = int(score)
        game['against'] = int(against)
    except:
        print "DICT ERROR\t",date,day,home,opp,res,score,against
        exit()
        

    return game    


def parseTable(table):
    table = [x.replace("</tr>", "") for x in table]
    table = [x.replace("</td>", "") for x in table]

    teamdata={}
    teamdata["games"] = []
    
    table = table[1:]
    name,conf = getName(table[0])
    teamdata["name"] = name
    teamdata["conf"] = conf

    table = table[1:]

    for line in table:
        gamedata = getGame(line)
        if gamedata:
            teamdata["games"].append(gamedata)

    return teamdata
    exit()

    

def parseScores(txt):
    fdata = open(txt).readlines()
    fdata = [x.strip('\r\n') for x in fdata]

    yeardata={}

    i=0
    while i < len(fdata):
        line = fdata[i]
        tdata=[]
        if line.find("<table") != -1:
            while line.find("</table>") == -1:
                tdata.append(line)
                i += 1
                line = fdata[i]

            teamdata = parseTable(tdata)
            yeardata[teamdata['name']] = {}
            yeardata[teamdata['name']]['conf'] = teamdata['conf']
            yeardata[teamdata['name']]['games'] = teamdata['games']
            print len(yeardata)
        i += 1
    return yeardata


def parseAbrv(txt):
    print txt
    fdata = open(txt).readlines()
    fdata = [x.strip('\r\n') for x in fdata]
    fdata = [x.strip('\t') for x in fdata]
    i=0
    adata={}
    while i < len(fdata):
        line = fdata[i]
        if line.find('----') != -1:
            i += 1
            continue
        vals = line.split(' = ')
        if len(vals) == 2:
            adata[vals[0]] = vals[1]
        else:
            print line,'\t',vals
            exit()
        i += 1

    return adata

def parseLocation(locdata, abrvdata):
    print locdata
    fdata = open(locdata).readlines()
    fdata = [x.strip('\r\n') for x in fdata]
    fdata = [x.strip('\t') for x in fdata]
    states={}
    missing={}
    print abrvdata.keys()
    fteam={}
    for team in abrvdata.keys():
        fteam[team] = {}
        fteam[team]["Abrv"] = abrvdata[team]
        fteam[team]["City"] = None
        fteam[team]["State"] = None
    
    for line in fdata:
        lvals = line.split('\t')
        name = lvals[0]
        mascot = lvals[1]
        city = lvals[2]
        state = lvals[3]
        if state == "Hawai'i":
            state = "Hawaii"
        conf = lvals[4]
        states[state] = 1
        
        if fteam.get(name) == None:
            print "#",name,city,state
            print "            fteam[\""+name+"\"][\"City\"] = "
            print "            fteam[\""+name+"\"][\"State\"] = "
        else:               
            fteam[name]["City"] = city
            fteam[name]["State"] = state
        
    print sorted(fteam.keys())
    
    fteam["Army"]["City"] = "West Point"
    fteam["Army"]["State"] = "New York"
    fteam["Bowling Green State"]["City"] = "Bowling Green"
    fteam["Bowling Green State"]["State"] = "Ohio"
    fteam["Brigham Young"]["City"] = "Provo"
    fteam["Brigham Young"]["State"] = "Utah"
    fteam["Central Florida"]["City"] = "Orlando"
    fteam["Central Florida"]["State"] = "Florida"
    fteam["Kent"]["City"] = "Kent"
    fteam["Kent"]["State"] = "Ohio"
    fteam["Louisiana State"]["City"] = "Baton Rouge"
    fteam["Louisiana State"]["State"] = "Louisiana"
    fteam["Miami (Florida)"]["City"] = "Coral Gables"
    fteam["Miami (Florida)"]["State"] = "Florida"
    fteam["Middle Tennessee State"]["City"] = "Murfreesboro"
    fteam["Middle Tennessee State"]["State"] = "Tennessee"
    fteam["Mississippi"]["City"] = "Oxford"
    fteam["Mississippi"]["State"] = "Mississippi"
    fteam["North Carolina State"]["City"] = "Raleigh"
    fteam["North Carolina State"]["State"] = "North Carolina"
    fteam["Northern Illinois"]["City"] = "DeKalb"
    fteam["Northern Illinois"]["State"] = "Illinois"
    fteam["Southern California"]["City"] = "Los Angeles"
    fteam["Southern California"]["State"] = "California"
    fteam["Southern Methodist"]["City"] = "University Park"
    fteam["Southern Methodist"]["State"] = "Texas"
    fteam["Southern Mississippi"]["City"] = "Hattiesburg"
    fteam["Southern Mississippi"]["State"] = "Mississippi"
    fteam["Texas Christian"]["City"] = "Fort Worth"
    fteam["Texas Christian"]["State"] = "Texas"
    fteam["Hawaii"]["City"] = "Honolulu"
    fteam["Hawaii"]["State"] = "Hawaii"
    fteam["Miami (Ohio)"]["City"] = "Oxford"
    fteam["Miami (Ohio)"]["State"] = "Ohio"
    fteam["Texas-El Paso"]["City"] = "El Paso"
    fteam["Texas-El Paso"]["State"] = "Texas"
    fteam["Texas-San Antonio"]["City"] = "San Antonio"
    fteam["Texas-San Antonio"]["State"] = "Texas"
    fteam["Nevada-Las Vegas"]["City"] = "Las Vegas"
    fteam["Nevada-Las Vegas"]["State"] = "Nevada"
    fteam["Florida International"]["City"] = "Miami"
    fteam["Florida International"]["State"] = "Florida"
            
    for k,v in fteam.iteritems():
        if v["City"] == None:
            print k

    return fteam
            
#    print sorted(states.keys())        
#    print abrvdata

#getAbrv('', 'Abvr.dat')
abrvdata = parseAbrv('Abrv.txt')
locdata = parseLocation('Location.csv', abrvdata)
json.dump(locdata, open("Teams.json", "w"))

yeardata = parseScores('2015.dat')
json.dump(yeardata, open("2015games.json", "w"))

writeAbrvFile('Teams.csv', locdata)
#writeFile('2015.csv', yeardata)
#writeConfFile('2015.conf', yeardata)
#writeGraphFile('2015.graph', yeardata)
