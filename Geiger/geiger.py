# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:21:34 2017

@author: mark.orchard-webb
"""

import matplotlib.pyplot as p
import numpy
import serial

class GeigerArduino:
    def __init__(self,verbose=0):
        self.verbose = verbose
        if verbose: print "introArduino class creator: Verbose mode activated"
        for i in range(10):
            device = "/dev/ttyACM%d" % (i)
            if verbose: print("Trying '%s'"%(device))
            try:
                self.device = serial.Serial(device,baudrate=115200,timeout=2.0,)
                if verbose: print "Found device at %s" % (device)
                break
            except:
                continue
        buf = self.device.read(10000) # clean out the buffer
        if self.verbose: print("cleared %d bytes"%(len(buf)))
        self.device.setDTR(1); #reboot Arduino
        self.device.setDTR(0);
        self.device.setDTR(1);
        exception_count = 0
        attempts = 0
        while True:
            try:
                if "HELLO" == self.getResp():
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
        while True:
            if self.verbose: print "Waiting for response..."
            str = self.device.readline()
            str = str.replace("\n","")
            str = str.replace("\r","")
            if self.verbose: print "Got response: '%s'" % (str)
            if str[:6] != "DEBUG:": return str

def enlarge(a_in,out_cols):
    rows = numpy.size(a_in,axis=0)
    in_cols = numpy.size(a_in,axis=1)
    a_out = numpy.zeros((rows,out_cols),dtype=int)
    a_out[:,0:in_cols] = a_in
    return a_out,out_cols-1

def setPeriod(c,period):
    command = "%d"%(1000*period)
    c.send("%s\n"%command)
    resp = c.getResp()
    if resp != command:
        print("Seek attention: response to '%s' was '%s'"%(command,resp))
        raise ValueError
    c.getResp()
    c.getResp()

def geiger(replicas=20, intervals=100, period=0.2, savefile="geiger.npz",graphics=True):
    print("Connecting to Arduino")
    a = GeigerArduino()
    print("Setting period")
    setPeriod(a,period)
    print("Starting collection")
    max_events = 10
    h = numpy.zeros((replicas,max_events+1),dtype=int)
    e = numpy.linspace(0,max_events,max_events+1)
    rectangles = []
    if graphics:
        p.figure()
        p.xlabel("Events per %.3f s interval"%(period))
        p.ylabel("Frequency of observation")
    for i in range(replicas):
        print("replica %d"%i)
        for k in range(intervals):
            if graphics:
                for r in rectangles:
                    r.remove()
            j = int(a.getResp())
            if (j > max_events):
                h,max_events = enlarge(h,j+2)
                e = numpy.linspace(0,max_events,max_events+1)
                print("Warning, increase max_events --- enlarging to %d"%(max_events))
            h[i,j] += 1
            if graphics:
                rectangles = p.bar(e-0.5,h[i,:],width=1)
                p.pause(1e-3)
    if savefile and len(savefile) > 0:
        numpy.savez(savefile,histogram=h)
        print("histogram saved to disk as '%s'."%(savefile))
    return h
            
rc = geiger(replicas=128,intervals=64,period=0.2,graphics=False)
