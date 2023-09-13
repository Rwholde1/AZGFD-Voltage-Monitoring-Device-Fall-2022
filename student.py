class Student:
    def __init__(self, id, firstName, lastName):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName

    def __repr__(self):
        print("Student ID: {{self.id}}")
