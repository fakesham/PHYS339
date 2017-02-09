# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:32:42 2017

@author: mammam
"""
import numpy
import matplotlib.pyplot as plt  

t = 0.5
# length of time to generate data for (s) 
intLen = 0.001
# interval length between each data point (s) 
fc = 0
# critical frequency (Hz)

xVals = numpy.arange(0,t+intLen,intLen)
# x-values spaced intLen apart from 0 to t inclusive


# Input: frequency of sine wave
# Output: scaling factor to compensate for attenuation
def scale(f):
    # correct for amplitude 
    # some function of dF that gives us the scaling value 
    if(fc-f>=0):
        return 1 
    scaleFactor = 1 
    return scaleFactor
   
   
# Input: 1D x-value data, period 
# Output: all entries of x modulo t 
def modulus(x,t):
    toReturn = numpy.copy(x)
    for i in range(len(x)):
        while(toReturn[i]-t>=0):
            toReturn[i] = toReturn[i]-t
    return toReturn


# Input: desired frequency, desired amplitude,
#        input vector, desired degree of approximation 
# Output: sum of sine waves required to generate a 
#         sawtooth wave with given parameters
def fourierSawtooth(freq,amp,x,d): 
    
    y = numpy.zeros(len(x))
    xMod = modulus(x,1/freq)
    
    for n in range(d): 
        s = numpy.multiply((n+1),numpy.pi)            
        s = numpy.multiply(s,xMod)
        s = numpy.multiply(s,2*freq)
        s = numpy.sin(s)
        w = numpy.multiply(1/(n+1),s)
        w = w*scale((n+1)*freq)
        y = numpy.add(y,w)
        if(n=10)
        
    y = numpy.multiply(y,amp)
    y = numpy.divide(y,numpy.pi)
    toReturn = numpy.subtract(0,y)
    
    return toReturn 
      
      
def fourierTriangle(freq,amp,x,d): 
    
    y = numpy.zeros(len(x))
    xMod = modulus(x,1/freq)
    
    for n in range(d): 
        s = numpy.multiply((2*n+1),numpy.pi)            
        s = numpy.multiply(s,xMod)
        s = numpy.multiply(s,2*freq)
        s = numpy.sin(s)
        c = numpy.divide((-1)**n,(2*n+1)**2)
        w = numpy.multiply(c,s)
        w = w*scale((2*n+1)*freq)
        y = numpy.add(y,w)
        
    y = numpy.multiply(y,amp/2)
    toReturn = numpy.multiply(y,8/(numpy.pi)**2)
    
    return toReturn 
    
def fourierSquare(freq,amp,x,d): 
    
    y = numpy.zeros(len(x))
    xMod = modulus(x,1/freq)
    
    for n in range(d): 
        s = numpy.multiply((2*n+1),numpy.pi)            
        s = numpy.multiply(s,xMod)
        s = numpy.multiply(s,2*freq)
        s = numpy.sin(s)
        w = numpy.multiply(1/(2*n+1),s)
        w = w*scale((2*n+1)*freq)
        y = numpy.add(y,w)
        
    y = numpy.multiply(y,amp/2)
    toReturn = numpy.multiply(y,4/numpy.pi)
    
    return toReturn 
        
fSaw = fourierSawtooth(2,10,xVals,50)
fTri = fourierTriangle(2,10,xVals,50)
fSqu = fourierSquare(2,10,xVals,50)

plt.plot(xVals,fTri)
plt.plot(xVals,fSaw)
plt.plot(xVals,fSqu)