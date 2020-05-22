#!/usr/bin/python

import os
import subprocess
import time
import datetime
import sys
import Adafruit_DHT

minHum = 60
maxHum = 75
maxTemp = 26

while True:

        # Parse command line parameters.
        sensor_args = { '11': Adafruit_DHT.DHT11,
                        '22': Adafruit_DHT.DHT22,
                        '2302': Adafruit_DHT.AM2302 }
        if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
                sensor = sensor_args[sys.argv[1]]
                pin = sys.argv[2]
        else:
                print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
                print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
                sys.exit(1)

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
                print('Failed to get reading. Try again!')
                sys.exit(1)

        #Check Humidity and transform the value into a readable number
        proc = subprocess.Popen(["./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 18 | cut -c 22-25"],stdout=subprocess.PIPE,shell=True)
        (out, err) = proc.communicate()

	#Check Humidity and transform the value into a readable number
        proc = subprocess.Popen(["./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 18 | cut -c 6-9"],stdout=subprocess.PIPE,shell=True)
        (out2, err) = proc.communicate()

        #Convert humidity to float and ignore errors
        try:
                out = float(out)
        except ValueError:
                continue

	#Convert temperature to float and ignore errors
        try:
                out2 = float(out2)
        except ValueError:
                continue


        #If the humidity is lower than 60% turn humidifier On
        if out <= minHum:
                print "Turning Humidifier On"
                with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(['/home/pi/relayson.py'], stdout=devnull, stderr=subprocess.STDOUT)

	#If the temperature is higher than 26C turn humidifier On
        elif out2 >= maxTemp:
                print "Turning Humidifier On"
                with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(['/home/pi/relayson.py'], stdout=devnull, stderr=subprocess.STDOUT)

	 #If the humidity is higher than 75% turn humidifier Off
        elif out >= maxHum and out2 < maxTemp:
                print "Turning Humidifier Off"
                with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(['/home/pi/relaysoff.py'], stdout=devnull, stderr=subprocess.STDOUT)

	#If the temperature is higher than 26C turn humidifier On
#	elif out2 >= maxTemp:
#		print "Turning Humidifier On"
#                with open(os.devnull, 'wb') as devnull:
#                        subprocess.check_call(['/home/pi/relayson.py'], stdout=devnull, stderr=subprocess.STDOUT)

        #If the humidity is between 60% and 75% do nothing
        else:
                #pass
		#readable = datetime.datetime.fromtimestamp(1526724156).isoformat()
                print "Humidity level higher than 60%"

        time.sleep(120)
