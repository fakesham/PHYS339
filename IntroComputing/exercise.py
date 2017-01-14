# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 09:07:27 2017

@author: mark.orchard-webb
"""

import serial
import matplotlib.pyplot as p
import numpy

class introArduino:
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
                if "HELLO" == self.getResp()[0:5]: 
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
# The following functions download data from the arduino
# Arduino object is passed as "c" (connection)

def get_replica(c):
    c.send("getdata")
    resp = c.getResp()
    words = resp.split(" ")  # split line at spaces
    rows = int(words[1])
    columns = int(words[2])
    freq = float(words[3])
    print("rows: %d, columns: %d, freq: %f" % (rows,columns,freq))
    replica = numpy.zeros((rows,columns)) # make a box to store data
    for i in range(rows):
        resp = c.getResp()
        words = resp.split(" ") # same trick
        for j in range(columns):
            replica[i][j] = int(words[j])
    return freq,replica
    
def get_dataset(c,n):
    if n < 1:
        print "You requested %d replicas ... does that make sense?" % (n)
        exit()
    fs,replica = get_replica(c)
    data = numpy.array(replica,ndmin=3)
    for i in range(1,n):
        print("fetching replica %d" % (i))
        fs,replica = get_replica(c)
        new_data = numpy.array(replica,ndmin=3)
        data = numpy.append(data,new_data,axis=0)
    return fs,data

# This calculates mean and errorbars from 2-D raw data,
# where the first dimension is the replica index, the second
# the time step and returns a 2-D array where the first index
# is the timestep, and the second selects between mean and errorbar
def raw_to_mean_errorbar(raw):
    """Calculates an mean and uncertainty from raw data"""
    replicas = numpy.size(raw,axis=0)
    means = raw.mean(0)
    errorbars = raw.std(0)/numpy.sqrt(replicas)
    return numpy.column_stack((means,errorbars))

# Create a data set
#
a = introArduino()
replicas = 5

fs,data = get_dataset(a,replicas)

# This data is in a format you are not yet expected to be able to handle
# but for infomational purposes ...

print "Shape of data:",(data.shape)

# Sampling frequency is important, we use it to generate a time signal

print "Sampling frequency: %f",fs
timesteps = numpy.size(data,1)
t = numpy.array(range(timesteps))/fs
    
# Extract the signals from the composite.  Do not worry about this part!
a_raw = data[:,:,0]
b_raw = data[:,:,1]
c_raw = data[:,:,2]
d_raw = data[:,:,3]

# Create arrays in the format discussed
a = raw_to_mean_errorbar(a_raw)
b = raw_to_mean_errorbar(b_raw)
c = raw_to_mean_errorbar(c_raw)
d = raw_to_mean_errorbar(d_raw)

# these are now in the discussed format.  It is now your job to
# write functions which perform operations on these arrays and
# return as results arrays which correctly propagate the uncertainties
# of the operations.

print "Shape of a:",a.shape

# Plot a figure to see what the data looks like
if True:
    p.figure()
    p.xlabel("Time (s)")
    p.ylabel("Sample value")
    p.errorbar(t,a[:,0],a[:,1],fmt='none',errorevery=3,label="Signal a")
    p.errorbar(t,b[:,0],b[:,1],fmt='none',errorevery=3)
    p.errorbar(t,c[:,0],c[:,1],fmt='none',errorevery=3)
    p.errorbar(t,d[:,0],d[:,1],fmt='none')

# once you have written all the required functions, the following
# should work, and give correct results

def rms(t,x):
    square = multiply(x,x)
    mean = integrate(t,square)[1] # not true yet!!!
    mean[1:,:] /= numpy.column_stack((t,t))[1:,:]
    mean[0,:] = 0  # this is probably a matter of dogma
    return sqrt(mean)
    
if False:
    d_rms = rms(t,d)
    p.figure()
    p.errorbar(t,d_rms[:,0],d_rms[:,1])


# The following will save the arrays t,a,b,c and d into a file
# called intro_exercise_data.pyz
# See resume.py to see how to load it
if True:
        numpy.savez("intro_exercise_data.npz",t=t,a=a,b=b,c=c,d=d)
