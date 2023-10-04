class Event:
    def __init__(self, id, timestamp, voltage, frequency):
        self.id = id
        self.timestamp = timestamp
        self.voltage = voltage
        self.frequency = frequency

    def __repr__(self):
        print(f"[ID: {self.id}] [Timestamp: {self.timestamp}] [Voltage: {self.voltage}] [Frequency: {self.frequency}]")
