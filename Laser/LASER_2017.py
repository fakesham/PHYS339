# -*- coding: utf-8 -*-
"""
This is only an example, it requires the LASER_2017.ino to be loaded on the Arduino.

What it does imply what you need to do, merely gives an example interaction with the Arduino
and is primarily useful for me verifying operation of the hardware provided.
"""

import serial
import matplotlib.pyplot as p
import numpy
import string
import os 
from time import sleep 

# This is pretty familiar

class Arduino:
    def __init__(self,verbose=0):
        self.verbose = verbose
        if verbose: print "introArduino class creator: Verbose mode activated"
        for i in range(10):
            device = "/dev/ttyACM%d" % (i)
            try:
                self.device = serial.Serial(device,baudrate=115200,timeout=1.0)
                if verbose: print "Found device at %s" % (device)
                break
            except:
                continue   
        self.device.setDTR(1); #reboot Arduino
        self.device.setDTR(0);
        self.device.setDTR(1);
        exception_count = 0
        attempts = 0
        while True:
            try:
                if "LASER 2017" == self.getResp()[0:10]: 
                    if verbose: print "Arduino is communicating"
                    return
            except:
                if self.verbose: print "Exception"
                exception_count = exception_count + 1
            attempts = attempts + 1
            if 5 == attempts:
                print "Unable to communicate with Arduino...%d exceptions" % (exception_count)
                exit
    def send(self,str):
        self.device.write("%s\n" % (str))
        if self.verbose: print "Sent '%s'" % (str)
    def getResp(self):
        if self.verbose: print "Waiting for response..."
        str = self.device.readline()
        str = str.replace("\n","")
        str = str.replace("\r","")
        if self.verbose: print "Got response: '%s'" % (str)
        return str

#
# START PAYING ATTENTION HERE
#

a = Arduino()

steps = 360
a.send("LASER 0")
a.getResp()
a.send("STEPS %d"%(steps))
a.send("DELAYS 20")
a.send("START")
p.figure()
p.xlabel("Step index")
p.ylabel("ADC reading")
vector = numpy.zeros((2,steps))
lines = [False,False]

index = -1
while True:
    resp = a.getResp()
    if 9 == len(resp) and resp[4] == ':':
        words = string.split(resp,":")
        step = int(words[0])
        adc = int(words[1])
        if 0 == step:
            if lines[index & 1]:
                for i in lines[index & 1]:
                    i.remove()
            lines[index & 1] = p.plot(range(steps),vector[index & 1,:])  
            p.pause(0.01)
            exec("numpy.savetxt('laserSineWave%d.txt',vector)"%index)
            index += 1
        vector[index&1,step] = adc
    else:
        print("Unexpected response: %s"%(resp))
        print("Length: %d"%(len(resp)))
    if -1 == index:
        break
a.send("STOP")
a.send("LASER 0")

adcVals = []
for i in range(100):
    a.send("LASER %d"%(i*40))
    sleep(0.2)
    a.getResp()
    respLaser = string.split(a.getResp(),":")
    if(respLaser[0]!=("Timeout!")):
        adcVals.append(respLaser[1])
    
p.figure()
x = numpy.linspace(0,4080,len(adcVals))
p.plot(x,adcVals)
