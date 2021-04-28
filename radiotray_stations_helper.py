#!/usr/bin/env python2.7
import io,re,csv
import requests,zipfile
import xml.etree.ElementTree as ET


url = "http://www.radiosure.com/rsdbms/stations2.zip"
response = requests.get(url)

file = zipfile.ZipFile(io.BytesIO(response.content))
stationsfile = file.read(file.namelist()[0])

stations  = re.split("(\\t-)*(\\n)",stationsfile)
stations = [i for i in stations if i is not None]
stations = [i.split("\t") for i in stations if len(i)>2]

genres = [i[2] for i in stations]
genres = set(genres)

genstations = {}

for i in stations:
	genstations[i[2]] = []

for station in stations:
	links = [i for i in station if i.find("://")!=-1]
	for i,link in enumerate(links):
		genstations[station[2]].append([station[0]+" ["+str(i)+"]",link])

bookmarks = ET.Element("bookmarks")
group = ET.SubElement(bookmarks,"group")
group.set("name","root")

for genre in genres:
	genregroup = ET.SubElement(group,"group")
	genregroup.set("name",genre)
	for s in genstations[genre]:
		bookmark = ET.SubElement(genregroup,"bookmark")
		bookmark.set("name",s[0].decode('UTF-8','ignore').encode('ascii','ignore'))
		bookmark.set("url",s[1].decode('UTF-8','ignore').encode('ascii','ignore'))

tree = ET.ElementTree(bookmarks)

# write xml file for radiotray bookmarks.xml

stationsxml = open("bookmarks.xml","w")
tree.write(stationsxml)
stationsxml.close()


# write csv file stationname,stationurl for pyradio stations.csv

with open('stations.csv',mode='w') as stationscsvfile:
	stationfile_writer = csv.writer(stationscsvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
	for genre in genres:
		for s in genstations[genre]:
			stationfile_writer.writerow([s[0],s[1]])



