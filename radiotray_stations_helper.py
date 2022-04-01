#!/usr/bin/env python2.7
import io,re,csv,sys
import requests,zipfile
import xml.etree.ElementTree as ET

# download stations zip file from radiosure, unzip it and load it in stations
url = "http://www.radiosure.com/rsdbms/stations2.zip"


if len(sys.argv)-1 == 0:
	try:
		response = requests.get(url)
		file = zipfile.ZipFile(io.BytesIO(response.content))
		file.extract(file.namelist()[0])

	except Exception as ex:
		print("Error downloading stations zip !!!", ex)
		sys.exit(3)


if len(sys.argv)-1 == 1:
	try:
		with open(sys.argv[1],'r') as file:
			stations = file.readlines()

	except Exception as ex:
		print("Problem reading zipfile from system !!!",ex)
		sys.exit(3)

stations = [station.split("\t") for station in stations]
genres = [i[2] for i in stations]
genres = set(genres)
genstations = {}

for i in stations:
	genstations[i[2]] = []


for station in stations:
	links = [r.rstrip('/;') for r in station[5:11] if r.find('http://')>-1]
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
		bookmark.set("name",s[0].encode().decode('utf-8'))
		bookmark.set("url",s[1].encode().decode('utf-8'))

tree = ET.ElementTree(bookmarks)

# write xml file for radiotray bookmarks.xml

stationsxml = open("bookmarks.xml","wb")
tree.write(stationsxml)
stationsxml.close()


# write csv file stationname,stationurl for pyradio stations.csv

with open('stations.csv',mode='w') as stationscsvfile:
	stationfile_writer = csv.writer(stationscsvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
	for genre in genres:
		for s in genstations[genre]:
			stationfile_writer.writerow([s[0],s[1]])
	stationscsvfile.close()


# write m3u file for pyradio stations.m3u

with open('stations.m3u',mode='w') as stationsmufile:
	stationsmufile.write('#EXTM3U')
	for genre in genres:
		for s in genstations[genre]:
			stationsmufile.write("EXTINF:-1,"+s[0]+"\n")
			stationsmufile.write(s[1]+"\n")
	stationsmufile.close()
