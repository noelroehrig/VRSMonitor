import datetime
import TripRepository
from Models.TripListModel import TripListModel
from appJar import gui

app = gui()
_tripListModel = TripRepository.GetRealTimeData()

def UpdateDepartures():
    for station in _tripListModel.Trips:
        for tripModel in _tripListModel.Trips[station]:
            countdown = (tripModel.departure - datetime.timedelta(0,1)) - datetime.datetime.now()
            app.setLabel(f"{tripModel.tripId}-departure", countdown.total_seconds() // 60)

def PrintDepartures():
    for station in _tripListModel.Trips:
        app.addLabel(station, station, colspan=2)
        app.setLabelBg(station, "red")
        for tripModel in _tripListModel.Trips[station]:
            countdown = tripModel.departure - datetime.datetime.now()
            # add & configure widgets - widgets get a name, to help referencing them later
            row = app.getRow()
            app.addLabel(tripModel.tripId, tripModel.tripNr, row, 0)
            app.addLabel(f"{tripModel.tripId}-departure", countdown.total_seconds() // 60, row, 1)

    # start the GUI
    app.registerEvent(UpdateDepartures)
    app.go()