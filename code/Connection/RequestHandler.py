import requests
import os
import configparser
import xml.etree.ElementTree as ET

_config =  configparser.ConfigParser()
_config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..\configure", "config.ini"))
_serverUrl = _config["ServerSettings"]["serverUrl"]
_stationIds = _config["StationSettings"]["stationId"].split(",")

def GetRequestAsXml():
    url = _serverUrl
    headers = {'Content-Type': 'application/xml'}
    requestResults = list()
    for stationId in _stationIds:
        payload = f'<?xml version="1.0" encoding="ISO-8859-15"?><Request><StopTimetable><Location><Classes><Stop><ASSID>{stationId}</ASSID></Stop></Classes></Location><SearchTime SearchDirection="Departure"/><SearchInterval><Size>3600</Size></SearchInterval><Options><Output><SRSName>urn:adv:crs:ETRS89_UTM32</SRSName></Output></Options></StopTimetable></Request>'
        requestResult = requests.request("POST", url, headers=headers, data = payload).text
        requestResults.append(ET.ElementTree(ET.fromstring(requestResult)).getroot())    
    return requestResults