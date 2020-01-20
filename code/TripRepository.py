from Models.TripListModel import TripListModel
from Models.TripModel import TripModel
import requests
import os
import configparser
import xml.etree.ElementTree as ET

_config =  configparser.ConfigParser()
_config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "configure", "config.ini"))
_serverUrl = _config["ServerSettings"]["serverUrl"]
_stationIds = _config["StationSettings"]["stationId"].split(",")


def GetRequestXml():
    url = _config["ServerSettings"]["serverUrl"]
    headers = {'Content-Type': 'application/xml'}
    requestResults = list()
    for stationId in _stationIds:
        payload = f'<?xml version="1.0" encoding="ISO-8859-15"?><Request><StopTimetable><Location><Classes><Stop><ASSID>{stationId}</ASSID></Stop></Classes></Location><SearchTime SearchDirection="Departure"/><SearchInterval><Size>3600</Size></SearchInterval><Options><Output><SRSName>urn:adv:crs:ETRS89_UTM32</SRSName></Output></Options></StopTimetable></Request>'
        requestResult = requests.request("POST", url, headers=headers, data = payload).text
        requestResults.append(ET.ElementTree(ET.fromstring(requestResult)).getroot())    
    return requestResults

def ParseXmlToModel(xml):
    tripListModel = TripListModel()
    tripListModel.Trips.clear()
    for child in xml.iter("StopEvent"):
        vehicleJourney = child.find("VehicleJourney")
        if(vehicleJourney.find("DirectionNo").text != _config["StationSettings"]["direction"]):
            continue
        tripId = vehicleJourney.find("ID").text
        tripDirection = vehicleJourney.find("Direction").text
        tripArrival = "2020-01-17T12:11:00+01:00" if child.find("ArrivalTime") is None else child.find("ArrivalTime").text
        tripDeparture = child.find("DepartureTime").text
        tripListModel.Trips.append(TripModel(tripId, tripDirection, tripArrival, tripDeparture))
    # TODO: Ugly, change 
    for stop in xml.iter("Stop"):
        if(stop.findtext("Class") == "Stop"):
            tripListModel.stationName = stop.findtext("Name")
            break
    return tripListModel

def CreateDataModels():
    requestResults = GetRequestXml()
    stationCollection = list()
    for stationResult in requestResults:
        tripListModel = ParseXmlToModel(stationResult)
        stationCollection.append(tripListModel)
    return stationCollection

def GetRealTimeData():
    tripListModel = CreateDataModels()
    return tripListModel