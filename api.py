'''
Datetime Format: YYYY-MM-DDTHH:MM:SS
Date Format: YYYY-MM-DD
'''
'''
class Event:
id -- string
timestamp local time UTC - xxx -- DateTime
voltage (V) -- double
frequency (Hz) -- double
'''


from flask import Flask, request, make_response
import json


from google.cloud.firestore_v1 import FieldFilter

from event import Event
from firebase_admin import credentials, firestore, initialize_app
import datetime

import dotenv
import os
dotenv.load_dotenv()

cred = credentials.Certificate('azgfd-epics-firebase-adminsdk-k222y-b12e3ae9ac.json')
default_app = initialize_app(cred)
database = firestore.client()

app = Flask(__name__)

COLLECTION_ID = os.getenv('COLLECTION_ID')
databaseCollection = database.collection(COLLECTION_ID)
@app.route("/", methods=["GET"])
def index():

    documents = databaseCollection.stream()

    EventsList = []

    for doc in documents:
        parsedDateTime = datetime.datetime.strptime(doc.to_dict()["date"] + "T" + doc.to_dict()["time"], "%Y-%m-%dT%H:%M:%S")
        newEvent = Event(doc.id, parsedDateTime.isoformat(), doc.to_dict()["voltage"], doc.to_dict()["frequency"])
        EventsList.append(newEvent)

    response = make_response()
    response.status_code = 200
    response.content_type = "application/json"
    response.mimetype = "application/json"
    response.data = json.dumps([event.__dict__ for event in EventsList])

    return response

@app.route("/post", methods=["POST"])
def pushToDatabase():
    if request.method != "POST":
        response = make_response()
        response.status_code = 400
        return response

    currentDateTime = datetime.datetime.now().replace(microsecond=0)
    print(f"Date: {currentDateTime.date().isoformat()} Time: {currentDateTime.time().isoformat()}")
    voltage = request.form["voltage"]
    frequency = request.form["frequency"]

    if(not voltage):
        response = make_response()
        response.data = "Voltage is not present"
        response.status_code = 400
        return response

    if(not frequency):
        response = make_response()
        response.data = "Frequency is not present"
        response.status_code = 400
        return response

    try:
        voltage = float(voltage)
        frequency = float(frequency)
    except ValueError:
        response = make_response()
        response.status_code = 400
        return response

    if(voltage < 0):
        response = make_response()
        response.data = "Voltage can not be negative"
        response.status_code = 400
        return response

    if(frequency < 0):
        response = make_response()
        response.data = "Frequency can not be negative"
        response.status_code = 400
        return response

    count = databaseCollection.count().get()[0][0].value + 1

    eventId = f"event{count}"
    newEvent = Event(eventId, currentDateTime.isoformat(), voltage, frequency)

    # new date time has to be in format of object DateTimeWithNanoSeconds
    insertData = { "date": currentDateTime.date().isoformat(), "time": currentDateTime.time().isoformat(), "voltage": voltage, "frequency": frequency }
    print(insertData.__repr__())

    # insert the data in the collection
    document = databaseCollection.document(eventId)
    document.set(insertData)

    response = make_response()
    response.status_code = 200
    response.content_type = "application/json"
    response.data = json.dumps(newEvent.__dict__)
    return response

#will get the most recent entry by default
@app.route("/get", methods=["GET"])
def getFromDatabase():
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response

    databaseCount = databaseCollection.count().get()[0][0].value
    document = databaseCollection.document(f"event{databaseCount}")
    eventId = document.id
    document = document.get()
    document = document.to_dict()

    parsedDateTime = datetime.datetime.strptime(document["date"] + "T" + document["time"], "%Y-%m-%dT%H:%M:%S")

    newEvent = Event(eventId, parsedDateTime.isoformat(), document["voltage"] , document["frequency"])

    response = make_response()
    response.status_code = 200
    response.content_type = "application/json"
    response.data = json.dumps(newEvent.__dict__)
    return response

@app.route("/getdate/<dateRequest>", methods=["GET"])
def getByDate(dateRequest):
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response

    # date format should be YYYY-MM-DD

    if(not dateRequest):
        response = make_response()
        response.data = "Date is not present"
        response.status_code = 400
        return response


    datetimeformat = '%Y-%m-%d'
    # convert from string format to datetime format
    date = None
    try:
        date = datetime.datetime.strptime(dateRequest, datetimeformat)
    except ValueError:
        response = make_response()
        response.status_code = 400
        response.data = "Incorrect date format"
        return response

    dateRequest = date.date().isoformat()
    print(dateRequest)

    print(date.__repr__())
    documents = (
        databaseCollection.where(filter=FieldFilter("date", "==", dateRequest)).stream()
    )

    EventsList = []

    for doc in documents:
        data = doc.to_dict()
        parsedDateTime = datetime.datetime.strptime(data["date"] + "T" + data["time"], "%Y-%m-%dT%H:%M:%S")
        EventsList.append(Event(id=doc.id, timestamp=parsedDateTime.isoformat(), voltage=data["voltage"], frequency=data["frequency"]))

    response = make_response()
    response.data = json.dumps([event.__dict__ for event in EventsList])
    response.content_type = "application/json"
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(debug=True)
