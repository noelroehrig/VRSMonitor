import datetime

class TripModel:
    departure = datetime.datetime.fromtimestamp(1578046725)
    arrival = datetime.datetime.fromtimestamp(1578046725)
    stopName = "Scheibenstr."
    tripNr = "12"
    tripId = "6020276-602-006-ab9478.2.22:111800-an1307.2.22:121500-39-55"

    def __init__(self, id):
        self.tripId = f"{self.tripId}{id}"