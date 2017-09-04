import requests
from bs4 import BeautifulSoup
import pprint
import datetime
import quik
from os import getcwd

guildurl = 'https://swgoh.gg/g/990/rebel-force-sullust/'
chars = []

def getGuildRoster():
    roster = []
    g = requests.get(guildurl)
    goup = BeautifulSoup(g.text, 'html.parser')
    guild = goup.findAll('tr')[1:]
    for gm in guild:
        playername = gm.a['href'].replace('/','')[1:]
        roster.append({'playername':playername,'displayname':gm.strong.text,'characters':[]})
    return roster

def doCharacter(c):
    charactername = c.img['alt']
    if charactername not in chars:
        chars.append(charactername)
    sl = c.find_all('div',{'class':'star'})
    if len(sl) == 0:
        stars = 0
        level = 0
        gear = 0
    else:
        stars = 7 - (str(sl).count('inactive'))
        level = c.find('div',{'class','char-portrait-full-level'}).text
        gear = c.find('div',{'class','char-portrait-full-gear-level'}).text
    return {'character': charactername,
            'stars': stars,
            'level': level,
            'gear-level': gear}


def doPlayer(playername):
    characters = []
    playercharacters = []
    collection_url = 'https://swgoh.gg/u/%s/collection/' % playername
    r = requests.get(collection_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for idx, val in enumerate(soup.find('li',{'class','media list-group-item p-a collection-char-list'}).find_all('a')):
        if idx%2==0:
            characters.append(val)
    for c in characters:
        playercharacters.append(doCharacter(c))
    playercharacters = sorted(playercharacters, key=lambda k: (k['character']))
    return playercharacters


roster = getGuildRoster()
for m in roster:
    m['characters'] = doPlayer(m['playername'])
updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
pp = pprint.PrettyPrinter(indent=4)
print(chars)
#pp.pprint(roster)
chars.sort()
loader = quik.FileLoader(getcwd() + '/', True)
filelist = ['template_guild.html']
for tempfile in filelist:
    outname = tempfile.replace("template", "processed")
    template = loader.load_template("templates/" + tempfile)
    f1 = open(outname, 'w+')
    f1.write(template.render(locals(), loader))
    f1.close()
