#!/usr/bin/python

import os
import numpy
import subprocess

while True:

        command = "./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 4 | cut -c 22-23"
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        (out1, err) = proc.communicate()
        outwithoutreturn = out1.rstrip('\n')

        command2 = "./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 18 | cut -c 22-23"
        proc = subprocess.Popen(command2,stdout=subprocess.PIPE,shell=True)
        (out2, err) = proc.communicate()
        outwithoutreturn = out2.rstrip('\n')

        total = int(out1) + int(out2)
        avg = (total/2)

        if avg < 60:
                #os.popen("/home/pi/relayson.py")
                with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(['/home/pi/relayson.py'], stdout=devnull, stderr=subprocess.STDOUT)
        else:
                pass
                #os.system("/home/pi/relaysoff.py")


        if avg > 75:
                #os.system("/home/pi/relaysoff.py")
                with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(['/home/pi/relaysoff.py'], stdout=devnull, stderr=subprocess.STDOUT)
        else:
                pass
                #os.system("/home/pi/relayson.py")

#print out1
#print out2
#print total
#print avg

#sensor1 = (os.system("./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 4 | cut -c 22-23"))
#sensor2 = (os.system("./Adafruit_Python_DHT/examples/AdafruitDHT.py 2302 18 | cut -c 22-23"))


