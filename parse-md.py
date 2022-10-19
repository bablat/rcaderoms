import json
import re
from xml.etree import ElementTree as ET


feedstr = """
{
  "title": "MegaMegaDrive",
  "categories": [
    {
        "title": "MegaMegaDrive",
        "items": [],      
        "description": "The Sega Genesis, known as the Mega Drive[c] outside North America, is a 16-bit fourth-generation home video game console developed and sold by Sega. The Genesis was Sega's third console and the successor to the Master System. Sega released it in 1988 in Japan as the Mega Drive, and in 1989 in North America as the Genesis. In 1990, it was distributed as the Mega Drive by Virgin Mastertronic in Europe, Ozisoft in Australasia, and Tec Toy in Brazil. In South Korea, it was distributed by Samsung as the Super Gam*Boy and later the Super Aladdin Boy.[d] In Russia, it was distributed by Bitman.",
        "longTitle": "Mega Drive/Genesis",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sega-Mega-Drive-JP-Mk1-Console-Set.jpg/2880px-Sega-Mega-Drive-JP-Mk1-Console-Set.jpg",
        "background": "https://github.com/CkauNui/ckau-book/raw/master/_inc/art/megadrive.jpg"
    }
  ],
  "longTitle": "Mega, Mega-Drive",
  "description": "A better mega-drive feed",
  "thumbnail": "https://i.imgur.com/iXxE4KB.png",
  "background": "https://i.imgur.com/fyRoGmy.png",
  "backgroundPixelated": true
}
"""


feed = json.loads(feedstr)

# # Opening JSON file
# f = open('src.json')
  
# # returns JSON object as 
# # a dictionary
# data = json.load(f)
  
# # Iterating through the json
# # list
# for i in data['emp_details']:
#     print(i)
  
# # Closing file
# f.close()

# Opening JSON file
f = open('src.html')

html = f.readlines()
for line in html:
    match = re.search('<tr><td><a href="(//archive.org/download/.+?).md">genesis/(.+?).md</a>',line)
    if (match):
        name = match.groups()[1]
        baseurl = "https:" + match.groups()[0]
        cover = baseurl + ".cover.png"
        md = baseurl + ".md"
        shot1 = baseurl + ".shot.1.png"
        shot2 = baseurl + ".shot.2.png"
        item = {
            "title": name,
            "longTitle": name,
            "type": "genesis",
            "background": shot1,
            "thumbnail": cover,
            "description": "",
            "backgroundPixelated": "true",
            "props": {
                "rom": md,
            },
            "added": "1641777758161"
        }
        feed["categories"][0]["items"].append(item)

print(json.dumps(feed, indent=4))

        

        

