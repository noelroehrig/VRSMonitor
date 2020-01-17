from Models.TripListModel import TripListModel
from Models.TripModel import TripModel
import requests
import os
import configparser
import xml.etree.ElementTree as ET

_config =  configparser.ConfigParser()
_config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "configure", "config.ini"))

def GetRequestXml():
    url = _config["ServerSettings"]["serverUrl"]
    payload = f'<?xml version="1.0" encoding="ISO-8859-15"?><Request><StopTimetable><Location><Classes><Stop><ASSID>{_config["StationSettings"]["stationId"]}</ASSID></Stop></Classes></Location><SearchTime SearchDirection="Departure"/><SearchInterval><Size>3600</Size></SearchInterval><Options><Output><SRSName>urn:adv:crs:ETRS89_UTM32</SRSName></Output></Options></StopTimetable></Request>'
    headers = {
    'Content-Type': 'application/xml'
    }
    requestResult = requests.request("POST", url, headers=headers, data = payload).text
    return ET.ElementTree(ET.fromstring(requestResult)).getroot()

def ParseXmlToModel(xml):
    tripListModel = TripListModel()
    for child in xml.iter("StopEvent"):
        vehicleJourney = child.find("VehicleJourney")
        if(vehicleJourney.find("DirectionNo").text != _config["StationSettings"]["direction"]):
            continue
        tripId = vehicleJourney.find("ID").text
        tripDirection = vehicleJourney.find("Direction").text
        tripArrival = "2020-01-17T12:11:00+01:00" if child.find("ArrivalTime") is None else child.find("ArrivalTime").text
        tripDeparture = child.find("DepartureTime").text
        tripListModel.Trips.append(TripModel(tripId, tripDirection, tripArrival, tripDeparture))

    return tripListModel

def CreateDataModels():
    requestResult = GetRequestXml()
    tripListModel = ParseXmlToModel(requestResult)
    return tripListModel

def GetRealTimeData():
    tripListModel = CreateDataModels()
    return tripListModel