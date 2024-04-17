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
account_sid = 'AC641d027ac1e40141edc5905640ec84a6'
auth_token = '3600f40466e007accfadd350a79d5ecb'

# Twilio phone number and recipient phone number
twilio_number = '+1 844 763 5288' # Your Twilio phone numbedfr
recipient_numbers = ['+1 806 420 7601']#,'+1 602 545 6997'] # Recipient's phone number
#'+1 425 365 7514'  harwinders number?
# Store the mesasges that we want to send

client = Client(account_sid, auth_token)

voltage = 0.0
freq = 15.0

MAX_VOLTS = 130.0
MIN_VOLTS = 110.0

MAX_FREQ = 65.0
MIN_FREQ = 55.0

textSent = False
textInterval = 300.0
textSendTime = 0
currentTime = 0

#readError = 0
#maxErrors = 6

def getDateTime():
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
	return dt_string
	
#dt = getDateTime()
message = ""
#("Voltage critically high: " + voltage + " volts. Measurement taken at " + dt)


if __name__ == '__main__':
	print("Reading from Arduino")
	time.sleep(3)
	# Arduino connection through USB port 
	while True:
		try:
			ser = serial.Serial('/dev/ttyACM0', 19200, timeout=1)
			ser.reset_input_buffer()
			break
			
		# Oops! You forgot to plug in the Arduino
		except serial.serialutil.SerialException:
			print("Please plug in Arduino.")
			time.sleep(3)
		
	print("Successfully connected with arduino")
	while True:
		# check if the CPU is overheating
		if (CPUTemperature().temperature > 80.0):
			print("System overheating, shutting down.")
			dt = getDateTime()
			message = "System overheating, shutting down at " + dt + ". Please restart the script."

			for recipient_number in recipient_numbers:
				m = client.messages.create(
        						to=recipient_number,
        						from_=twilio_number,
        						body=message
								)
				print('Max Volts Message sent to', recipient_number, 'with SID:', m.sid, '\n')
			break
		
		if textSent:
			currentTime = time.time()
			timeDifference = currentTime - textSendTime
			# if the last text was sent more than 5 minutes ago
			if timeDifference > textInterval:
				# a text is allowed to be sent
				textSent = False
				textSendTime = 0
				currentTime = 0

		# collect measurements from Arduino
		if ser.in_waiting > 0:
			
			startT = time.time()

			# Add defaults
			voltage = ser.readline().decode('utf-8').rstrip()
			print(voltage + " Volts")
			
			ser.write(b'FREQ?\n')
			freq = ser.readline().decode('utf-8').rstrip()
			print(freq + " Hz")
			
			
			# voltage too high
			if ((float(voltage) > MAX_VOLTS) and (textSent == False)):
				dt = getDateTime()
					
				message = "Voltage critically high: " + voltage + " volts. Measurement taken at " + dt

				for recipient_number in recipient_numbers:
					m = client.messages.create(
        							to=recipient_number,
        							from_=twilio_number,
        							body=message
									)
					print('Max Volts Message sent to', recipient_number, 'with SID:', m.sid, '\n')
				
				textSent = True
				textSendTime = time.time()
						
			# voltage too low
			elif ((float(voltage) < MIN_VOLTS) and (textSent == False)):
				dt = getDateTime()
					
				message = "Voltage critically low: " + voltage + " volts. Measurement taken at " + dt

				for recipient_number in recipient_numbers:
					m = client.messages.create(
        							to=recipient_number,
        							from_=twilio_number,
        							body=message
									)
					print('Min Volts Message sent to', recipient_number, 'with SID:', m.sid, '\n')
					
				textSent = True
				textSendTime = time.time()
					
			# Frequency too high
			if ((float(freq) > MAX_FREQ) and (textSent == False)):
				dt = getDateTime()
					
				message = "Frequency critically high: " + freq + " hertz. Measurement taken at " + dt

				for recipient_number in recipient_numbers:
					m = client.messages.create(
        							to=recipient_number,
        							from_=twilio_number,
        							body=message
									)
					print('Max Freq Message sent to', recipient_number, 'with SID:', m.sid, '\n')
					
				textSent = True
				textSendTime = time.time()
				
			# Frequency too low
			elif ((float(freq) < MIN_FREQ) and (textSent == False)):
				dt = getDateTime()
					
				message = "Frequency critically low: " + freq + " hertz. Measurement taken at " + dt
				
				for recipient_number in recipient_numbers:
					m = client.messages.create(
        							to=recipient_number,
        							from_=twilio_number,
        							body=message
									)
					print('Min Freq Message sent to', recipient_number, 'with SID:', m.sid, '\n')
					
				textSent = True
				textSendTime = time.time()
			
			#Unused functionality, but a useful fragment if we want to reboot
			#if readError > maxErrors:
				#readError = 0
				#print("Rebooting")
				#os.system("python3 reboot.py")
				#client.auth_reset()
				#time.sleep(1)
				#quit()
			
			time.sleep(1)
			endT = time.time()
			print(int(endT-startT), "seconds")
