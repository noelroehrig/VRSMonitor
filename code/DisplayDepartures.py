from datetime import datetime, timezone
import time
import TripRepository
from Models.TripListModel import TripListModel
from appJar import gui, appjar

app = gui()
_stationCollection = TripRepository.GetRealTimeData()
_dataRefreshTimer = time.time()

def ColorizeDepartures(countdown, tripModel):
    if(countdown.total_seconds() / 60 > 10):
        app.setLabelBg(tripModel.tripId, "green")
        app.setLabelBg(f"{tripModel.tripId}-departure", "green")
    elif (countdown.total_seconds() / 60 > 5):
        app.setLabelBg(tripModel.tripId, "yellow")
        app.setLabelBg(f"{tripModel.tripId}-departure", "yellow")
    else:
        app.setLabelBg(tripModel.tripId, "red")
        app.setLabelBg(f"{tripModel.tripId}-departure", "red")

def AddDeparture(countdown, tripModel):
    row = app.getRow()
    app.addLabel(tripModel.tripId, tripModel.direction, row, 0)
    app.addLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min", row, 1)

def UpdateStation(tripListModel):
    for tripModel in tripListModel.Trips[:5]:
        countdown = tripModel.departure - datetime.now(timezone.utc)
        app.openFrame(tripListModel.stationName)
        try:
            app.setLabel(f"{tripModel.tripId}-departure", f"{'{0:.1f}'.format(countdown.total_seconds() / 60)} min")
        except appjar.ItemLookupError:
            AddDeparture(countdown, tripModel)
        
        if(countdown.total_seconds() < 0):
            app.removeLabel(tripModel.tripId)
            app.removeLabel(f"{tripModel.tripId}-departure")
        ColorizeDepartures(countdown, tripModel)

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
            app.addHorizontalSeparator(0,0,2)
            app.addLabel(tripListModel.stationName, tripListModel.stationName, colspan=2)
            app.getLabelWidget(tripListModel.stationName).config(font=("Sans Serif", "20", "bold"))
            for tripModel in tripListModel.Trips[:5]:
                countdown = tripModel.departure - datetime.now(timezone.utc)
                AddDeparture(countdown, tripModel)

                ColorizeDepartures(countdown, tripModel)

    # start the GUI
    app.registerEvent(UpdateApp)
    app.go()