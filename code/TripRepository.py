from Models.TripListModel import TripListModel
from Models.TripModel import TripModel

def CreateDummyTripList():
    return {"Scheibenstr." : [TripModel("1"), TripModel("2"), TripModel("3")], "Sebastianstr." : [TripModel("4"), TripModel("5")]}

def GetRealTimeData():
    tripListModel = TripListModel()
    tripListModel.Trips = CreateDummyTripList()
    for station in tripListModel.Trips:        
        for trip in tripListModel.Trips[station]:
            trip.station = station
    return tripListModel