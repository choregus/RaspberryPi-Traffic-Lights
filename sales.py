#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sales to Traffic Light
#
# 2016 James Welch
#

# Import the modules used in the script
import time
import urllib2
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
 
# Assign constants for the light GPIO pins
red_led = 17
yellow_led = 27
green_led = 22
RUNNING = True
 
# Configure the GPIO to BCM and set the pins to output mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
 
# Define a function to control the traffic light
def trafficState(red, yellow, green):
    GPIO.output(red_led, red)
    GPIO.output(yellow_led, yellow)
    GPIO.output(green_led, green)

# Enter the URL where you will be placing the data file that updates periodically
target_url = "http://a-url-of-yours.com/sales-instructions.txt"
 
print "Sales to Traffic Light By James Welch. Press CTRL + C to quit"

# Time to sleep (this is how often the script will poll the URL. 300 (5 mins) is good.
sleeptime = 300 

# Start the script by checking that there is an internet connection. If there isnt, then keep trying and sleep 10 seconds between.
## Used so that when booting up, there are no errors and the script always runs.
loop_value = 1
while (loop_value == 1):
	
	try:
		urllib2.urlopen(target_url)
	except urllib2.HTTPError, e:
		print e.code
		time.sleep(10)
	except urllib2.URLError, e:
		print e.args
		time.sleep(10)

	else:
		loop_value = 0

		# Main loop
		try:
			while RUNNING:
				import urllib2
		# Get the mac address of this Raspberry Pi
				from uuid import getnode as get_mac
				mac = get_mac()
				mac = hex(mac)

		# Read the data file line by line, looking for the instruction relating to this mac address			
				response = urllib2.urlopen(target_url)
				lines = response.readlines()
		# Get the current time so that we can get the flashing to work (by counting odd or even seconds)		
				import time
				curtime = lambda: int(round(time.time() * 1000))
				
				
				for line in lines:
				# Go through the motions			
					if mac in line:
				# split the data from the URL into chunks we can use
						scores = line.split(':')
				# put the first chunk of data into a variable		
						salestotal = int(scores[1])
				# if that variable is greater than the second chunk of data (half the total) then turn light amber
						if salestotal > int(scores[3]):
							trafficState(1,1,1)
							time.sleep(sleeptime)
				# if its greater than the 3rd chunk of data (the target) then turn green
						elif salestotal > int(scores[2]):
							trafficState(0,1,1)
							time.sleep(sleeptime)
				# else stay red (and flash to really annoy)
						else:
							count = 0
							while (count < sleeptime):
								if curtime() % 2 == 0:
									trafficState(0,0,1)
								else:
									trafficState(0,0,0)
								time.sleep(1)
								count = count + 1



		# If CTRL+C is pressed the main loop is broken
		except KeyboardInterrupt:
			RUNNING = False
			print "\Quitting"
 
		# Actions under 'finally' will always be called
		finally:
			# Stop and finish cleanly so the pins
			# are available to be used again
			GPIO.cleanup()
