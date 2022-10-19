import json
import html
import re
from xml.etree import ElementTree as ET


feedstr = """
{
  "title": "MegaMegaDrive",
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
    }
  ],
  "longTitle": "Mega, Mega-Drive, +N64",
  "description": "A better mega-drive feed, plus some N64 titles",
  "thumbnail": "https://i.imgur.com/iXxE4KB.png",
  "background": "https://i.imgur.com/fyRoGmy.png",
  "backgroundPixelated": true
}
"""


feed = json.loads(feedstr)

#              <td><a href="007%20-%20The%20World%20is%20Not%20Enough%20%28U%29%20%5B%21%5D.zip">007 - The World is Not Enough (U) [!].zip</a> (<a href="007%20-%20The%20World%20is%20Not%20Enough%20%28U%29%20%5B%21%5D.zip/">View Contents</a>)</td>
# https://archive.org/download/n64-raspberry-pi-buenos-aires/007%20-%20The%20World%20Is%20Not%20Enough%20%28USA%29.zip/007%20-%20The%20World%20Is%20Not%20Enough%20%28USA%29.z64
n64f = open('n64.html')

htmlfile = n64f.readlines()
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


# Opening JSON file
mdf = open('src.html')

htmlfile = mdf.readlines()
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

mdf.close()

print(json.dumps(feed, indent=4))

        

        

