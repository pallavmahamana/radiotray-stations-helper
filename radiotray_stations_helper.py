#!/usr/bin/env python2.7
import io,re,csv
import requests,zipfile
import xml.etree.ElementTree as ET


url = "http://www.radiosure.com/rsdbms/stations2.zip"
response = requests.get(url)

file = zipfile.ZipFile(io.BytesIO(response.content))
# stationsfile = file.read(file.namelist()[0],'r')
# stationsfile = file.readlines(file.namelist()[0])

# stations  = re.split("(\\t-)*(\\n)",stationsfile)
# stations = [i for i in stations if i is not None]
# stations = [i.split("\t") for i in stations if len(i)>2]
# 

file.extract(file.namelist()[0])

with open(file.namelist()[0],'r') as file:
	stations = file.readlines()

stations = [station.split("\t") for station in stations]
genres = [i[2] for i in stations]
genres = set(genres)
genstations = {}

for i in stations:
	genstations[i[2]] = []

for station in stations:
	links = [r for r in station[6:11] if r.find('http://')>-1]
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
		bookmark.set("name",s[0].decode('utf-8'))
		bookmark.set("url",s[1].decode('utf-8'))

tree = ET.ElementTree(bookmarks)
stationsxml = open("bookmarks.xml","wb")
tree.write(stationsxml)
stationsxml.close()


# write csv file stationname,stationurl for pyradio stations.csv

with open('stations.csv',mode='w') as stationscsvfile:
	stationfile_writer = csv.writer(stationscsvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
	for genre in genres:
		for s in genstations[genre]:
			stationfile_writer.writerow([s[0],s[1]])



