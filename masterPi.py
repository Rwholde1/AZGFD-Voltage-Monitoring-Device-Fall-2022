import serial, time, smtplib, gspread, csv, socket, os, sys
import requests, json, urllib
import pytextnow
from datetime import datetime
from gpiozero import CPUTemperature

#Email stuff

SMTP_SERVER = 'smtp.gmail.com'              #Email Server (don't change!)
SMTP_PORT = 587                             #Server Port (don't change!)
GMAIL_USERNAME = 'voltmeterazgfd@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'asuEPICS2021'             #change this to match your gmail password
emailSubject = "SMS Alert"

MAX_VOLTS = 130.0
MIN_VOLTS = 110.0

MAX_FREQ = 65.0
MIN_FREQ = 55.0

number1 = "6026153692"
number2 = "3162109128"

consecutiveOB = 5
outOfBoundsV = 0
outOfBoundsF = 0
readError = 0
maxErrors = 4

# textnow
client = pytextnow.Client("voltmeterazgfd", "s%3As2im46Bq2CRkNHKNg1hLf6iJLG_dFoD3.Ff1minkuVvQfxYKlZQYea7KbW9nOHjjuUbVy%2Bokt%2BUs", "s%3AdGOyx3y6WK07laRLUcb7yPbU.n2nJeTvOcL7iNWR0JqCWV5hBlkb2PX1UxqOcWu2foKw")

# setup access to spreadsheet
gc = gspread.service_account(filename='/home/pi/Documents/credentials.json')
sh = gc.open_by_key('1_RyT4Af2-h3I4QhH54W8xKC2mMbebXPHp1qDH9N4BL8')

def getDateTime():
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
	return dt_string
	

def updateSheet(info):
	# find next available row on the spreadsheet
	worksheet = sh.sheet1
	str_list = list(filter(None, worksheet.col_values(1)))
	n = len(str_list)+1
	
	# insert the info into the empty row
	worksheet.insert_row(info, n)
	pass
	

if __name__ == '__main__':
	
	# Arduino connection through USB port 
	while True:
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
			ser.reset_input_buffer();
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
			
			freq = ser.readline().decode('utf-8').rstrip()
			print(freq + " Hz")
			
			
			# voltage too high
			if (float(voltage) > MAX_VOLTS):
				
				outOfBoundsV += 1
				readError += 1
				
				if outOfBoundsV >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Voltage critically high: ", voltage, " volts. Measurement taken at ", dt))
					
					client.send_sms(number1, emailContent)
					client.send_sms(number2, emailContent)
					
					updateSheet([voltage, freq, dt, "Voltage too high"])
					
					outOfBoundsV = 0
						
			# voltage too low
			elif (float(voltage) < MIN_VOLTS):
				
				outOfBoundsV += 1
				readError += 1
	
				if outOfBoundsV >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Voltage critically low: ", voltage, " volts. Measurement taken at ", dt))

					client.send_sms(number1, emailContent)
					client.send_sms(number2, emailContent)

					
					updateSheet([voltage, freq, dt, "Voltage too low"])
					
					outOfBoundsV = 0
					
			# Frequency too high
			if (float(freq) > MAX_FREQ):
				
				outOfBoundsF += 1
				readError += 1
				
				if outOfBoundsF >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Frequency critically high: ", freq, " Hz. Measurement taken at ", dt))

					client.send_sms(number1, emailContent)
					client.send_sms(number2, emailContent)

					
					updateSheet([voltage, freq, dt, "Freq too high"])
					
					outOfBoundsF = 0
				
			# Frequency too low
			elif (float(freq) < MIN_FREQ):
				
				outOfBoundsF += 1
				readError += 1
				
				if outOfBoundsF >= consecutiveOB: 
					dt = getDateTime()
					
					emailContent = "".join(("Frequency critically low: ", freq, " Hz. Measurement taken at ", dt))

					client.send_sms(number1, emailContent)
					client.send_sms(number2, emailContent)

					
					updateSheet([voltage, freq, dt, "Freq too low"])
					
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
