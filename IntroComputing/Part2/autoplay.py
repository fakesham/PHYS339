# -*- coding: utf-8 -*-
"""
A demo code to show communiction with Arduino.
Very opaque black box for device itself, hopefully later parts or not too terrible.

@author: Mark Orchard-Webb
"""

# For the immediate future, ignore everything until suggested otherwise

import serial
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
       
def play_hilo(connection):
    connection.send("PLAY HIGHER_LOWER")
    resp = connection.getResp()
    if not "OK_PLAY" == resp[0:7]:
        print "Something is wrong, Arduino replied '%s'" % (resp)
        return False
    bit = 2048
    acc = 0
    while bit > 0:
        guess = acc + bit
        print "Guessing %d" % (guess)
        connection.send("GUESS %d" % (guess))
        resp = connection.getResp()
        if not "OK_GUESS" == resp[0:8]:
          print "Something is wrong, Arduino replied '%s'" % (resp)
          return False
        if "CONGRATULATIONS" == resp[10:10+15]: return resp
        if "HIGHER" == resp[10:10+6]:
            acc = guess
        bit = bit >> 1
        
def derive_midpoint(low,high):
    midpoint = (low+high)/2
    return midpoint
    
def play_warmer_colder(connection):
    
    connection.send("PLAY WARMER_COLDER")
    resp = connection.getResp()
    
    if not "OK_PLAY" == resp[0:7]:
        print "Something is wrong, Arduino replied '%s'"
        
    highlim = 4095
    lowlim = 0
    
    guess = highlim
    print "Guessing %d" % (guess)
    connection.send("GUESS %d" % (guess))
    resp = connection.getResp()
    nextGuess = lowlim
    
    while 1:
        
        guess = nextGuess
        midpoint = derive_midpoint(lowlim,highlim)
        print "Making Guess: %d" % (guess)
        connection.send("GUESS %d" % (guess))
        resp = connection.getResp()
        print resp
        
        if not "OK_GUESS" == resp[0:8]:
          print "Something is wrong, Arduino replied '%s'" % (resp)
          return False
          
            
        if "WARMER" == resp[10:10+6]:
            if guess == lowlim:
                highlim = midpoint
                
            if guess == highlim:
                lowlim = midpoint
                
            nextGuess = midpoint
            
        if "COLDER" == resp[10:10+6]:
            if guess == highlim:
                nextGuess = lowlim
                
            if guess == lowlim:
                nextGuess = highlim
        
        if "SAME" == resp[10:10+4]:
            nextGuess = midpoint
            
        if "CONGRATULATIONS" == resp[10:10+15]: return resp
       
        
    print "All is well!"
   
    
    


arduino = introArduino()
result = play_hilo(arduino)
print "result: %s" % (result)

result = play_warmer_colder(arduino)
print "result: %s" % (result)