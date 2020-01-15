from Models.TripListModel import TripListModel
from Models.TripModel import TripModel
import requests
import xml.etree.ElementTree as ET

def GetRequestXml():
    url = "https://apitest.vrsinfo.de:4443/vrs/cgi/service/ass"
    payload = "<?xml version=\"1.0\" encoding=\"ISO-8859-15\"?>\r\n<Request>\r\n\t<StopTimetable>\r\n\t\t<Location>\r\n\t\t\t<Classes>\r\n\t\t\t<Stop>\r\n\t\t\t\t<ASSID>337</ASSID>\r\n\t\t\t</Stop>\r\n\t\t\t</Classes>\r\n\t\t</Location>\r\n\t\t<SearchTime SearchDirection=\"Departure\"/>\r\n\t\t<SearchInterval>\r\n\t\t\t<Size>3600</Size>\r\n\t\t</SearchInterval>\r\n\t\t<Product>LongDistanceTrains</Product>\r\n\t\t<Product>RegionalTrains</Product>\r\n\t\t<Product>SuburbanTrains</Product>\r\n\t\t<Product>Underground</Product>\r\n\t\t<Product>LightRail</Product>\r\n\t\t<Product>Bus</Product>\r\n\t\t<Product>CommunityBus</Product>\r\n\t\t<Product>OnDemandServices</Product>\r\n\t\t<Product>Boat</Product>\r\n\t\t<Product>RailReplacementServcies</Product>\r\n\t\t<SupplementalPayment>false</SupplementalPayment>\r\n\t\t<Direction>2</Direction>\r\n\t\t<DisabledAccessRequired/>\r\n\t\t<Options>\r\n\t\t\t<Output>\r\n\t\t\t<SRSName>urn:adv:crs:ETRS89_UTM32</SRSName>\r\n\t\t\t</Output>\r\n\t\t</Options>\r\n\t</StopTimetable>\r\n</Request>"
    headers = {
    'Content-Type': 'application/xml'
    }
    requestResult = requests.request("POST", url, headers=headers, data = payload).text
    return ET.ElementTree(ET.fromstring(requestResult)).getroot()

def ParseXmlToModel(xml):
    tripListModel = TripListModel()
    for child in xml.iter("StopEvent"):
        tripId = child.find("VehicleJourney").find("ID").text
        tripDirection = child.find("VehicleJourney").find("Direction").text
        tripArrival = child.find("ArrivalTime").text
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