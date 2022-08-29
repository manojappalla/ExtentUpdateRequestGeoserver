#! /Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.8

# IMPORT LIBRARIES
import os
import datetime
import requests
import configparser
import xml.etree.ElementTree as ET
from qgis.core import *
from qgis.utils import *
import json
from PyQt5.QtCore import *
import xmltodict

# INTIALIZE QGIS APPLICATION
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app/Contents/Resources", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# OPEN A SHAPEFILE AND READ THE EXTENTS
layer = QgsVectorLayer("/usr/local/geoserver/data_dir/data/wellpoints/WellLocation_repr.shp", "new", "ogr")
ext = layer.extent()
qminx = ext.xMinimum()
qminy = ext.yMinimum()
qmaxx = ext.xMaximum()
qmaxy = ext.yMaximum()
print(qminx, qminy, qmaxx, qmaxy)

# MAKE A GET REQUEST TO THE XML FILE
username = 'admin'
password = 'geoserver'
response = requests.get('http://localhost:8080/geoserver/rest/workspaces/wfs_practical/datastores/wellpoints/featuretypes/WellLocation_repr.xml', auth=(username, password))
doc = ET.fromstring(response.content)
# print(doc)
tree = ET.ElementTree(doc)
# print(tree[7][0].text)

# PRINT THE PREVIOUS EXTENT
for x in tree.findall('nativeBoundingBox'):
    # print(x.find('minx').text, x.find('miny').text, x.find('maxx').text, x.find('maxy').text)
    pass

# CHANGE THE EXTENT
for x in tree.findall('nativeBoundingBox'):
    x.find('minx').text = str(qminx)
    x.find('miny').text = str(qminy)
    x.find('maxx').text = str(qmaxx)
    x.find('maxy').text = str(qmaxy)

# PRINT THE CHANGED EXTENT
for x in tree.findall('nativeBoundingBox'):
    # print(x.find('minx').text, x.find('miny').text, x.find('maxx').text, x.find('maxy').text)
    pass
tree.write('extent.xml')


# MAKE A PUT REQUEST TO GEOSERVER TO UPDATE THE EXTENT
tree = ET.parse('extent.xml')
tree = tree.getroot()
t = ET.tostring(tree)
headers = {'Content-Type': 'application/xml'}
requests.put('http://localhost:8080/geoserver/rest/workspaces/wfs_practical/datastores/wellpoints/featuretypes/WellLocation_repr.xml', auth=(username, password), headers = headers, data=t)
# print(tree)