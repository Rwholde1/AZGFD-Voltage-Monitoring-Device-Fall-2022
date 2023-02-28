import serial, time, smtplib, csv, socket, os, sys
import requests, json, urllib
from twilio.rest import Client
from datetime import datetime
from gpiozero import CPUTemperature

#Email stuff

SMTP_SERVER = 'smtp.gmail.com'              #Email Server (don't change!)
SMTP_PORT = 587                             #Server Port (don't change!)
GMAIL_USERNAME = 'voltmeterazgfd@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'asuEPICS2023!'             #change this to match your gmail password
emailSubject = "SMS Alert"

# Message using twilio
account_sid = 'ACfbe365f13dc7f6f8cdec26fc68fc3195'
auth_token = '4b77e0347770efe28a39e1479351d536'

# Twilio phone number and recipient phone number
twilio_number = '+1 812 398 7121' # Your Twilio phone number
recipient_numbers = ['+1 602 615 3692', '+1 425 365 7514'] # Recipient's phone number

# Store the mesasges that we want to send
message = 'Hi'

client = Client(account_sid, auth_token)

MAX_VOLTS = 130.0
MIN_VOLTS = 110.0

MAX_FREQ = 65.0
MIN_FREQ = 55.0


consecutiveOB = 5
outOfBoundsV = 0
outOfBoundsF = 0
readError = 0
maxErrors = 4

def getDateTime():
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
	return dt_string


if __name__ == '__main__':
	
	# Arduino connection through USB port 
	while True:
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
			ser.reset_input_buffer()
			break
			
		# Oops! You forgot to plug in the Arduino
		except serial.serialutil.SerialException:
			print("Please plug in Arduino.")
			time.sleep(3)
		
	while True:
		#try:
		
		# check if the CPU is overheating
		if (CPUTemperature().temperature > 80.0):
			print("System overheating, shutting down.")
			break
		
		# collect measurements from Arduino
		if ser.in_waiting > 0:
			
			startT = time.time()
			#start = datetime.now()

			# Add defaults
			voltage = ser.readline().decode('utf-8').rstrip()
			print(voltage + " Volts")
			
			ser.write(b'FREQ?\n')
			freq = ser.readline().decode('utf-8').rstrip()
			print(freq + " Hz")
			
			
			# voltage too high
			if (float(voltage) > MAX_VOLTS):
				
				outOfBoundsV += 1
				readError += 1
				
				if outOfBoundsV >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Voltage critically high: ", voltage, " volts. Measurement taken at ", dt))
					
					message = emailContent

					for recipient_numbers in recipient_numbers:
						m = client.messages.create(
        								to=recipient_numbers,
        								from_=twilio_number,
        								body=message
										)
						print('Message sent to', recipient_numbers, 'with SID:', m.sid, '\n')
					outOfBoundsV = 0
						
			# voltage too low
			elif (float(voltage) < MIN_VOLTS):
				
				outOfBoundsV += 1
				readError += 1
	
				if outOfBoundsV >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Voltage critically low: ", voltage, " volts. Measurement taken at ", dt))

					message = emailContent

					for recipient_numbers in recipient_numbers:
						m = client.messages.create(
        								to=recipient_numbers,
        								from_=twilio_number,
        								body=message
										)
						print('Message sent to', recipient_numbers, 'with SID:', m.sid, '\n')
					
					outOfBoundsV = 0
					
			# Frequency too high
			if (float(freq) > MAX_FREQ):
				
				outOfBoundsF += 1
				readError += 1
				
				if outOfBoundsF >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Frequency critically high: ", freq, " Hz. Measurement taken at ", dt))

					message = emailContent

					for recipient_numbers in recipient_numbers:
						m = client.messages.create(
        								to=recipient_numbers,
        								from_=twilio_number,
        								body=message
										)
						print('Message sent to', recipient_numbers, 'with SID:', m.sid, '\n')
					
					outOfBoundsF = 0
				
			# Frequency too low
			elif (float(freq) < MIN_FREQ):
				
				outOfBoundsF += 1
				readError += 1
				
				if outOfBoundsF >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Frequency critically low: ", freq, " Hz. Measurement taken at ", dt))

					message = emailContent
					for recipient_numbers in recipient_numbers:
						m = client.messages.create(
        								to=recipient_numbers,
        								from_=twilio_number,
        								body=message
										)
						print('Message sent to', recipient_numbers, 'with SID:', m.sid, '\n')
					
					outOfBoundsF = 0
			
			if readError > maxErrors:
				readError = 0
				print("Rebooting")
				os.system("python3 reboot.py")
				client.auth_reset()
				time.sleep(1)
				quit()
			
			time.sleep(1)
			#end = datetime.now()
			endT = time.time()
			print(int(endT-startT), "seconds")
			
			#print(end-start)
