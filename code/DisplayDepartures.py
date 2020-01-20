from datetime import datetime, timezone
import time
import TripRepository
from Models.TripListModel import TripListModel
from appJar import gui, appjar

app = gui()
_stationCollection = TripRepository.GetRealTimeData()
_dataRefreshTimer = time.time()

def UpdateStation(tripListModel):
    for tripModel in tripListModel.Trips[:5]:
        countdown = tripModel.departure - datetime.now(timezone.utc)
        app.openFrame(tripListModel.stationName)
        try:
            app.setLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min")
        except appjar.ItemLookupError:
            row = app.getRow()
            app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
            app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)
        
        if(countdown.total_seconds() < 0):
            app.removeLabel(tripModel.tripId)
            app.removeLabel(f"{tripModel.tripId}-departure")

def UpdateApp():
    global _stationCollection
    for tripListModel in _stationCollection:
        UpdateStation(tripListModel)    
    if(_dataRefreshTimer + 5 < time.time()):
        _stationCollection.clear()
        _stationCollection = TripRepository.GetRealTimeData()

def PrintDepartures():
    for tripListModel in _stationCollection:
        with app.frame(tripListModel.stationName):
            app.addLabel(tripListModel.stationName, tripListModel.stationName, colspan=2)
            app.setLabelBg(tripListModel.stationName, "red")
            for tripModel in tripListModel.Trips[:5]:
                countdown = tripModel.departure - datetime.now(timezone.utc)
                
                row = app.getRow()
                app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
                app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)

    # start the GUI
    app.registerEvent(UpdateApp)
    app.go()