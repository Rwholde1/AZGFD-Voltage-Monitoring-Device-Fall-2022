from flask import Flask, request, make_response
import json
from event import Student



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
    student = Student(10, "James", "Franco")

    return json.dumps(student.__dict__)

@app.route("/post", methods=["POST"])
def pushToDatabase():
    if request.method != "POST":
        response = make_response()
        response.status_code = 400
        return response

    studentFirstName = request.form["firstname"]
    studentLastName = request.form["lastname"]
    studentId = request.form["id"]
    return json.dumps(Student(studentId, studentFirstName, studentLastName).__dict__)

@app.route("/get", methods=["GET"])
def getFromDatabase():
    if request.method != "GET":
        response = make_response()
        response.status_code = 400
        return response
    firstName = request.args.get('firstname')
    lastName = request.args.get('lastname')
    id = request.args.get('id')
    if(firstName and lastName and id):
        if firstName == "Nick" and lastName == "Roberts" and id == "101":
            return json.dumps(Student(id, firstName, lastName).__dict__)
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