'''
Datetime Format: YYYY-MM-DDTHH:MM:SS.NS
Date Format: YYYY-MM-DD



'''


from flask import Flask, request, make_response
import json
from event import Event
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

cred = credentials.Certificate('azgfd-epics-firebase-adminsdk-k222y-b12e3ae9ac.json')
default_app = initialize_app(cred)
database = firestore.client()

app = Flask(__name__)
'''
class Event:
id (auto generated) - integer auto incremented
timestamp local time UTC - xxx -- DateTime
voltage (V) -- double
frequency (Hz) -- double
'''

@app.route("/", methods=["GET"])
def index():
    testcollection = database.collection("testcollection1")
    docs = testcollection.stream()

    EventsList = []
    Dumps = []

    for doc in docs:
        newEvent = Event(doc.id, doc.to_dict()["date"].isoformat(), doc.to_dict()["voltage"], doc.to_dict()["frequency"])
        EventsList.append(newEvent)
        Dumps.append(json.dumps(newEvent.__dict__))
        print(f"{doc.id} => {doc.to_dict()}")



    event = Event(10, "timestamp", "voltage", "frequency")

    for event in EventsList:
        print(event.__repr__())

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

    currentDateTime = datetime.utcnow()
    print(f"{currentDateTime.isoformat()}")
    voltage = request.form["voltage"]
    frequency = request.form["frequency"]

    if(not voltage or not frequency):
        response = make_response()
        response.status_code = 400
        return response

    try:
        voltage = float(voltage)
        frequency = float(frequency)
    except ValueError:
        response = make_response()
        response.status_code = 400
        return response

    if(voltage < 0 or frequency < 0):
        response = make_response()
        response.status_code = 400
        return response

    testcollection = database.collection("testcollection1")
    count = testcollection.count().get()[0][0].value + 1

    id = f"event{count}"
    newEvent = Event(id, currentDateTime.isoformat(), voltage, frequency)

    # new date time has to be in format of object DateTimeWithNanoSeconds
    insertData = { "date": currentDateTime, "voltage": voltage, "frequency": frequency }
    print(insertData.__repr__())

    document = testcollection.document(id)
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

    testcollection = database.collection("testcollection1")
    count = testcollection.count().get()[0][0].value
    document = testcollection.document(f"event{count}")
    document = document.get()
    document = document.to_dict()
    print(document)

    #TODO: Find a way to return the correct id of the event
    newEvent = Event(0, document["date"].isoformat(), document["voltage"] , document["frequency"])

    response = make_response()
    response.status_code = 418
    response.data = json.dumps(newEvent.__dict__)
    return response

@app.route("/getdate/<date>", methods=["GET"])
def getByDate(date):
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response




    firstName = request.args.get('firstname')
    lastName = request.args.get('lastname')
    id = request.args.get('id')
    if(firstName and lastName and id):
        if firstName == "Nick" and lastName == "Roberts" and id == "101":
            return json.dumps(Event(10, "timestamp", "voltage", "frequency").__dict__)
    response = make_response()
    response.status_code = 418
    return response

@app.route("/getdate/<date>", methods=["GET"])
def getByDateTime(datetime):
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response




    firstName = request.args.get('firstname')
    lastName = request.args.get('lastname')
    id = request.args.get('id')
    if(firstName and lastName and id):
        if firstName == "Nick" and lastName == "Roberts" and id == "101":
            return json.dumps(Event(10, "timestamp", "voltage", "frequency").__dict__)
    response = make_response()
    response.status_code = 418
    return response

@app.route("/getlast", methods=["GET"])
def getLast():
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response

    count = request.args.get('count')

    if(not count):
        response = make_response()
        response.status_code = 400
        return response




    response = make_response()
    response.status_code = 418
    return response

@app.route("/delete", methods=["DELETE"])
def deleteFromDatabase():
    if request.method != "DELETE":
        response = make_response()
        response.status_code = 400
        return response
    return "DELETE"

@app.route("/put", methods=["PUT"])
def updateDatabase():
    if request.method != "PUT":
        response = make_response()
        response.status_code = 400
        return response
    return "PUT"


if __name__ == "__main__":
    app.run(debug=True)
    print("Hello world!")