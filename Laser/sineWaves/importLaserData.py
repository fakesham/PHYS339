# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:22:09 2017

@author: mammam
"""

import numpy 
import scipy
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import os

timeSpacing = 2.24/1000
# seconds 
period = 180*timeSpacing
f =  1/period


for i in range(20):
    exec("laser%d = numpy.concatenate((numpy.loadtxt('laserSineWave%d.txt')[0],numpy.loadtxt('laserSineWave%d.txt')[1]))"%(i,i,i))

for i in range(20)
intensityData = numpy.loadtxt('../intensitydata.txt')

x = numpy.arange(0,720*2.24,2.24)

plt.plot(intensityData[0],intensityData[1])

# ----------------------------- Least-squares fitting -----------------------------
# First guess
fg = [3*numpy.std(laser10)/(2**0.5), 0, numpy.mean(laser10)]

#a, phi, b
def residual(p,x,data):
    amp = p[0]
    print("p",p)
    phase = p[1] 
    offset = p[2]
    
    s = 2*numpy.pi*f
    s = numpy.multiply(s,x)
    s = numpy.subtract(s,2*numpy.pi*phase)
    testfit = numpy.sin(s)
    testfit = numpy.multiply(2*amp,testfit)
    testfit = numpy.add(testfit,offset)
    return numpy.square(numpy.subtract(data,testfit))
        
        
p1, success = leastsq(residual,fg,args=(x,laser10),maxfev=10)

xvals = numpy.arange(0,max(x),max(x)/1000)

s = 2*numpy.pi*f
s = numpy.multiply(s,xvals)
s = numpy.subtract(s,p1[1])
yvals = numpy.sin(s)
yvals = numpy.multiply(p1[0],yvals)
yvals = numpy.add(yvals,p1[2])

#plt.plot(xvals,yvals)
#plt.plot(x,laser10,'+')

plt.plot()