from datetime import datetime, timezone
import TripRepository
from Models.TripListModel import TripListModel
from appJar import gui, appjar

app = gui()
_stationCollection = TripRepository.GetRealTimeData()

def UpdateDepartures():
    _stationCollection = TripRepository.GetRealTimeData()
    for tripListModel in _stationCollection:
        for tripModel in tripListModel.Trips[:5]:
            countdown = tripModel.departure - datetime.now(timezone.utc)
            try:
                app.setLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min")
            except appjar.ItemLookupError:
                row = app.getRow()
                app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
                app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)
            if(countdown.total_seconds() < 0):
                app.removeLabel(tripModel.tripId)
                app.removeLabel(f"{tripModel.tripId}-departure")


def PrintDepartures():
    for tripListModel in _stationCollection:
        app.addLabel(tripListModel.stationName, tripListModel.stationName, colspan=2)
        app.setLabelBg(tripListModel.stationName, "red")
        for tripModel in tripListModel.Trips[:5]:
            countdown = tripModel.departure - datetime.now(timezone.utc)
            
            row = app.getRow()
            app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
            app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)

    # start the GUI
    app.registerEvent(UpdateDepartures)
    app.go()