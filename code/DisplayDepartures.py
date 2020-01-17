from datetime import datetime, timezone
import TripRepository
from Models.TripListModel import TripListModel
from appJar import gui, appjar

app = gui()
_tripListModel = TripRepository.GetRealTimeData()

def UpdateDepartures():
    _tripListModel = TripRepository.GetRealTimeData()
    for tripModel in _tripListModel.Trips[:5]:
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
    app.addLabel("Scheibenstr.", "Scheibenstr.", colspan=2)
    app.setLabelBg("Scheibenstr.", "red")
    for tripModel in _tripListModel.Trips[:5]:
        countdown = tripModel.departure - datetime.now(timezone.utc)
        
        row = app.getRow()
        app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
        app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)

    # start the GUI
    app.registerEvent(UpdateDepartures)
    app.go()