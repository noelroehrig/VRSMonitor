from Models.TripListModel import TripListModel
import Connection.RequestHandler as RequestHandler
from Models.TripModel import TripModel

def ParseXmlToModel(xml):
    tripListModel = TripListModel()
    for child in xml.iter("StopEvent"):
        vehicleJourney = child.find("VehicleJourney")
        if(vehicleJourney.find("DirectionNo").text != RequestHandler._config["StationSettings"]["direction"]):
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
    requestResults = RequestHandler.GetRequestAsXml()
    stationCollection = list()
    for stationResult in requestResults:
        tripListModel = ParseXmlToModel(stationResult)
        stationCollection.append(tripListModel)
    return stationCollection

def GetRealTimeData():
    tripListModel = CreateDataModels()
    return tripListModel