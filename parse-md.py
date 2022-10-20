from gzip import READ
import json
import html
from multiprocessing.resource_tracker import getfd
import re
from xml.etree import ElementTree as ET
import requests
import csv


def getlinesfromurl(url, pattern = ".*"):
    f = requests.get(url)
    lines = f.text.splitlines()
    output = []
    for line in lines:
        if re.search(pattern, line):
            output.append(line)
    return output

def getgroupfromurl(url, pattern = r"(.*)"):
    f = requests.get(url)
    match = re.search(pattern, f.text)
    if (match):
        print(match.groups()[0])
        return match.groups()[0]


def initfeeds():
    feedstr = """
    {
    "title": "MegaMegaDrive",
    "props": {
        "neogeo_bios": "https://archive.org/download/verifiedbiosfiles/OGA%20BIOS/NeoGeo/neogeo.zip"
        },
    "categories": [
        {
            "title": "MegaDrive",
            "items": [],      
            "description": "The Sega Genesis, known as the Mega Drive[c] outside North America, is a 16-bit fourth-generation home video game console developed and sold by Sega. The Genesis was Sega's third console and the successor to the Master System. Sega released it in 1988 in Japan as the Mega Drive, and in 1989 in North America as the Genesis. In 1990, it was distributed as the Mega Drive by Virgin Mastertronic in Europe, Ozisoft in Australasia, and Tec Toy in Brazil. In South Korea, it was distributed by Samsung as the Super Gam*Boy and later the Super Aladdin Boy.[d] In Russia, it was distributed by Bitman.",
            "longTitle": "Mega Drive/Genesis",
            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sega-Mega-Drive-JP-Mk1-Console-Set.jpg/2880px-Sega-Mega-Drive-JP-Mk1-Console-Set.jpg",
            "background": "https://github.com/CkauNui/ckau-book/raw/master/_inc/art/megadrive.jpg"
        },
        {
            "title": "N64",
            "items": [],      
            "description": "The Nintendo 64 (N64) is a home video game console developed by Nintendo. The successor to the Super Nintendo Entertainment System, it was released on June 23, 1996, in Japan, on September 29, 1996, in North America, and March 1, 1997, in Europe and Australia. It was the last major home console to use cartridges as its primary storage format until the Nintendo Switch in 2017. It competed primarily with the Sony PlayStation, the Sega Saturn, and the Sony PlayStation 2.",
            "longTitle": "Nintendo 64",
            "thumbnail": "https://commons.wikimedia.org/wiki/File:N64-Console-Set.jpg#/media/File:N64-Console-Set.jpg",
            "background": "https://en.wikipedia.org/wiki/File:Nintendo_64_Logo.svg#/media/File:Nintendo_64_Logo.svg"
        },
        {
            "title": "Arcade",
            "items": [],      
            "description": "FBNeo 1.0.2",
            "longTitle": "Arcade Machines",
            "thumbnail": "https://commons.wikimedia.org/wiki/File:N64-Console-Set.jpg#/media/File:N64-Console-Set.jpg",
            "background": "https://en.wikipedia.org/wiki/File:Nintendo_64_Logo.svg#/media/File:Nintendo_64_Logo.svg"
        }
    ],
    "longTitle": "Mega, Mega-Drive, +N64",
    "description": "A better mega-drive feed, plus some N64 titles",
    "thumbnail": "https://i.imgur.com/iXxE4KB.png",
    "background": "https://i.imgur.com/fyRoGmy.png",
    "backgroundPixelated": true
    }
    """


    return json.loads(feedstr)



if __name__ == '__main__':

    mame = {}

    with open('mame.csv', mode='r') as mamecsv:
        reader = csv.reader(mamecsv)
        mame = {rows[0]:rows[1] for rows in reader}
    mamecsv.close()

    feed = initfeeds()
    lines = getlinesfromurl("https://ia903203.us.archive.org/view_archive.php?archive=/13/items/fbneo/FBNeo/roms.zip", r'download/fbneo/FBNeo/roms.zip')
# <tr><td><a href="//archive.org/download/fbneo/FBNeo/roms.zip/roms%2Farcade%2Fcrkdown.zip">roms/arcade/crkdown.zip</a><td><td>1996-12-24 23:32<td id="size">946932</tr>
    for line in lines:
        #i += 1
      #  if (i>10):
       #     continue
        match = re.search(r'roms/arcade/(.+?)\.zip<',line)
        if (match):
            basename = match.groups()[0]
            rom = "https://archive.org/download/fbneo/FBNeo/roms.zip/roms%2Farcade%2F" + basename + ".zip"
            #name = getgroupfromurl("http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=" + basename, r'<meta name=\'twitter:description\' content="(.+?) MAME detail page - ROM')
            if (basename in mame.keys()):
                name = mame[basename]
            else:
                continue
            screenshot = "http://adb.arcadeitalia.net/media/mame.current/ingames/" + basename + ".png"
            artwork = "http://adb.arcadeitalia.net/media/mame.current/artworks_previews/" + basename + ".png"
            item = {
                "title": name,
                "longTitle": name,
                "type": "arcade",
                "background": artwork,
                "thumbnail": screenshot,
                "description": "",
                "backgroundPixelated": "true",
                "props": {
                    "rom": rom,
                },
                "added": "1641777758161"
            }
            feed["categories"][2]["items"].append(item)


    htmlfile = getlinesfromurl("https://archive.org/download/n64-raspberry-pi-buenos-aires/", r'<td><a href=".+\.zip">.+\.zip</a>\s*\(<a href=".+\.zip/">View Contents</a>\)</td>')
    for line in htmlfile:
        match = re.search('<td><a href="(.+?).zip">(.+?).zip</a>',line)
        if (match):
            longname = match.groups()[1]
            name = re.sub(r"\s*\((.*?)\)\s*", "", longname)
            path = match.groups()[0]
            rom = "https://archive.org/download/n64-raspberry-pi-buenos-aires/" + path + ".zip/" + path + ".z64"
            screenshot = "https://archive.org/download/n64-raspberry-pi-buenos-aires/screenshots/screenshots.7z/screenshots%2F" + path + ".png"
            marquee = "https://archive.org/download/n64-raspberry-pi-buenos-aires/marquees/marquees.7z/marquees%2F" + path + ".png"
            item = {
                "title": name,
                "longTitle": longname,
                "type": "n64",
                "background": screenshot,
                "thumbnail": screenshot,
                "description": "",
                "backgroundPixelated": "true",
                "props": {
                    "rom": rom,
                },
                "added": "1641777758161"
            }
            feed["categories"][1]["items"].append(item)


    # Grab MegaDrive
    htmlfile = getlinesfromurl("https://ia903006.us.archive.org/view_archive.php?archive=/18/items/RetroxReadyMegadrive/retrox%20ready%20megadrive.rar", r'<tr><td><a href=".+\.md">genesis/.+\.md</a><td>')
    for line in htmlfile:
        match = re.search('<tr><td><a href="(//archive.org/download/.+?).md">genesis/(.+?).md</a>',line)
        if (match):
            name = html.unescape(match.groups()[1])
            baseurl = "https:" + match.groups()[0]
            cover = baseurl + ".cover.png"
            md = baseurl + ".md"
            shot1 = baseurl + ".shot.1.png"
            shot2 = baseurl + ".shot.2.png"
            item = {
                "title": name,
                "longTitle": name,
                "type": "genesis",
                "background": cover,
                "thumbnail": shot2,
                "description": "",
                "backgroundPixelated": "true",
                "props": {
                    "rom": md,
                },
                "added": "1641777758161"
            }
            feed["categories"][0]["items"].append(item)

    print(json.dumps(feed, indent=4))

            

            

