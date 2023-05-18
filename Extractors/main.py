import requests
import lxml
import csv  
from html.parser import HTMLParser

import requests
import uuid 

Skip = -2
Start = -1
Name = 0
Author = 1
FullName = 2
Description = 3
Depends = 4
StdLink = 5

def publish_package(package):
    print("publishing: " + package[Name])
    params = {
        "component":(None, package[Name]),
        "short":(None, package[FullName]),
        "details":(None, package[Description]),
        "authors":(None, package[Author]),
        "link":(None, package[StdLink]),
        "addNote":(None, "Add"),
        "depends":(None, package[Depends])
        
    }
    cookies = {'user': '421281', "code":"47a050201d6c32b3426481b1687e4901", "PHPSESSID":"j9d5qgo2o96c1u6ue8nran0ube", "language":"en"}
    headers = {
        'user-agent': 'my-app/0.0.1',
        "Referer": "https://blackbox.oberon.org/settings/hodzanassredin" 
        }
    response = requests.post('https://blackbox.oberon.org/?pz=goods&f=add&profile=hodzanassredin&uid=12035', files=params,cookies= cookies,headers=headers)

    if response.status_code == 200:
        print("published")
    else:
        print("fail")
        with open("error.html", "w") as f:
            f.write(response.text)

URLS = [
    "http://www.zinnamturm.eu/downloadsAC.htm",
    "http://www.zinnamturm.eu/downloadsDH.htm",
    "http://www.zinnamturm.eu/downloadsIN.htm",
    "http://www.zinnamturm.eu/downloadsOS.htm",
    "http://www.zinnamturm.eu/downloadsTZ.htm",
]


# <h2 id="Ta_">Ta_</h2>
# <p>By <a href="authors.htm#Dag">Dmitry V. Dagaev</a></p>
# <h3>Transparent Architecture - communication SW for distributed systems.</h3>
# <p>This software is purposed for communication between different programs, written in Oberon and C. It uses SRPS protocol type for LANs via UDP multicast, UDP, TCP, Shared Memory, PING for ICMP and SOAP/HTTP for WANs.</p>
# <p>TA is distributed in BlackBox, XDS and C versions both for Windows and Linux compatible with each other at <a href="http://sourceforge.net/projects/ta1/">http://sourceforge.net/projects/ta1/</a>.</p>
# <p><b>Ta_</b> doesn&apos;t use any other CPC services.</p>
# <p><a href="pac/Ta_.txt">StdCoded File</a> &lt;=&gt; <a href="pac/Ta_.pac">PacCoded File</a> (641 / 283 kByte - Release 28-March-2014)</p>


# <h2 id="TboxCoderList">TboxCoderList</h2>
# <p>By <a href="authors.htm#Zin">Helmut Zinn</a></p>
# <h3>Generate a package list for StdCoded and PacCoded files.</h3>
# <p>This module generate the list of all source files of one subsystem automatically. You can select all items of this list and use the menu [Tools][Encode File List] to create a StdCoded file of your subsystem.</p>
# <p><b>TboxCoderList</b> uses the services of <a href="downloadsAC.htm#Ctls">Ctls</a>, <a href="downloadsAC.htm#CpcMenus">CpcMenus</a> and <a href="downloadsOS.htm#Pac">Pac</a>.</p>
# <p><a href="pac/TboxCoderList.txt">StdCoded File</a> &lt;=&gt; <a href="pac/TboxCoderList.pac">PacCoded File</a> (22 / 11 kByte - Release 7-Oct-2019)</p>





packages = []

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.package = None
        self.state = Skip
    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            if self.package:
                packages.append(self.package)
            self.package = ["","","","","",""]
            self.state = Name
        if tag == "a":
            for (name, val) in attrs:
                if name == "href" and val.startswith("pac/") and val.endswith(".txt"):
                    self.package[StdLink] = val
                    self.state = Skip
        if tag == "h3" and self.state == Author:
            self.state = FullName

    def handle_endtag(self, tag):
        if tag == "h2" and self.state == Name:
            self.state = Author
        if tag == "h3" and self.state == FullName:
            self.state = Description


    def handle_data(self, data):
        if ("uses the services of" in data or "doesn't use any other CPC services" in data) and self.state == Description:
            self.state = Depends
        if not self.state == Skip:
            self.package[self.state] += data

parser = MyHTMLParser()

for url in URLS:
    response = requests.get(url)
    html = response.content.decode("utf-8")
    parser.feed(html)

for package in packages:
    package[Name] = package[Name].strip()
    package[Author] = package[Author][5:].strip()
    package[FullName] = package[FullName].strip()
    package[Description] = package[Description].strip()

    if package[Description][-len(package[Name]):]==package[Name]:
        package[Description] = package[Description][:-len(package[Name])].replace('\n',"\r\n")
    package[Depends] = package[Depends] \
            .replace("doesn't use any other CPC services.","")\
            .replace("uses the services of","")\
            .replace("and","")\
            .replace(",","")\
            .replace(".","")\
            .replace("  "," ")\
            .strip()
    package[StdLink] = "http://www.zinnamturm.eu/" + package[StdLink]

pacakage_names = set([x[Name] for x in packages])
for package in packages:
    deps = [d for d in package[Depends].split(" ") if not d == package[Name] and d in pacakage_names]
    package[Depends] = ' '.join(set(deps))

# field names 

fields = ['Name', 'Author', 'FullName', 'Description', 'Depends', 'StdLink'] 
    
with open('zinnamturm.csv', 'w', encoding='utf-8') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(packages)

existing = ["Paket","Ogl","Grid","Hyper","Xmlcore","Tabs","CpcAllCaps","Svg","Vi","Master","Flash","Lists","Strings","Scl","CPfront","Комплексные числа","Sdl2","Zlib","Odf","RedBox","Cairo",
"Tetris","Collections","Russian","Tm","CpcTabs","Robust","Dia"]
existing = [e.lower() for e in existing]

for p in packages:
    if not p[Name].lower() in existing:
        publish_package(p)
                
                
