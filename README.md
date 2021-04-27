# radiotray_stations_helper
Script to generate bookmarks.xml from radiosure.com radio stations database for radiotray (and pyradio).

This Python2.7 script downloads the radio station compilation from [radiosure.com](http://www.radiosure.com/stations/) , and writes it to [radiotray](http://radiotray.sourceforge.net/) bookmark.xml format ( and [pyradio](https://github.com/coderholic/pyradio) stations.csv file )

copy the bookmark.xml file to ~/.local/share/radiotray , and enjoy 1000+ radio stations :)

for pyradio, check for stations.csv location by below command

$ pyradio -scd

 and then copy stations.csv file to that location


## usage
### use python2 to run this script
```bash
$ python2 radiotray_stations_helper.py

$ sudo cp bookmark.xml ~/.local/share/radiotray/
```

*or*

for pyradio, copy stations.csv file to location given by following command 

```bash
$ pyradio -scd | awk -F: '{print $NF}'
```