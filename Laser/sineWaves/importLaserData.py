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

# ----------------------------- Importing data ------------------------------------

f =  1/180

for i in range(1,20):
    exec("laser%d = numpy.concatenate((numpy.loadtxt('./rawdata/laserSineWave%d.txt')[0],numpy.loadtxt('./rawdata/laserSineWave%d.txt')[1]))"%(i,i,i))

for i in range(20):
    intensityData = numpy.loadtxt('../intensitydata.txt')

x = numpy.arange(0,720,1)


# ----------------------------- Least-squares fitting -----------------------------
def sineFit(p,x):
    #print("p",p)

    amp = p[0]
    freq = 2*numpy.pi*f
    phase = p[1]
    offset = p[2]
    
    s = numpy.sin(numpy.multiply(freq, numpy.subtract(x,phase)))
    return numpy.add(numpy.multiply(amp,s),offset)
    
#a, phi, b
def residual(p,x,y):
    return numpy.subtract(y,sineFit(p,x))

i = 10 
for i in range(1,20):
    exec("amp0 = 0.5*(max(laser%d)-min(laser%d))"%(i,i))
    exec("phase0 = 0")
    exec("offset0 = numpy.mean(laser%d)"%i)
    exec("firstGuess = numpy.array([amp0, phase0, offset0],dtype=float)")
    exec("print('first guess',firstGuess)")
    exec("params%d, success%d = scipy.optimize.leastsq(residual,firstGuess,args=(x,laser%d))"%(i,i,i))



print("parameters",params10)

# ------------------------------- Plots ----------------------------------
for i in range(1,20):
    exec("plt.figure(figsize=(8,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.plot(x, laser%d,'.')"%i)
    exec("plt.plot(x, sineFit(params%d,x))"%i)
    exec("plt.savefig('sineFit%d.png',dpi=150)"%i)
#plt.show()

"""


s = 2*numpy.pi*f
s = numpy.multiply(s,xvals)
s = numpy.subtract(s,p1[1])
yvals = numpy.sin(s)
yvals = numpy.multiply(p1[0],yvals)
yvals = numpy.add(yvals,p1[2])

#plt.plot(xvals,yvals)
"""

