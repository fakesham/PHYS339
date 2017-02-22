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

x = numpy.arange(0,720,1)
xBrewster = numpy.arange(0,360,1)

intensityData = numpy.loadtxt('./intensitydata.txt')

for i in range(1,20):
    exec("laser%d = numpy.concatenate((numpy.loadtxt('./sineWaves/rawdata/laserSineWave%d.txt')[0],numpy.loadtxt('./sineWaves/rawdata/laserSineWave%d.txt')[1]))"%(i,i,i))

for i in range(1,20):
    exec("brewster%d_1 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterAngle%d.txt')[0]"%(i,i))
    exec("brewster%d_2 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterAngle%d.txt')[1]"%(i,i))
    


# ----------------------------- Least-squares fitting -----------------------------
def sineFit(p,x):
    amp = p[0]
    freq = 2*numpy.pi*f
    phase = p[1]
    offset = p[2]
    
    s = numpy.sin(numpy.multiply(freq, numpy.subtract(x,phase)))
    return numpy.add(numpy.multiply(amp,s),offset)
    
def residual(p,x,y):
    return numpy.subtract(y,sineFit(p,x))

for i in range(1,20):
    exec("amp0 = 0.5*(max(laser%d)-min(laser%d))"%(i,i))
    exec("phase0 = 0")
    exec("offset0 = numpy.mean(laser%d)"%i)
    exec("firstGuess = numpy.array([amp0, phase0, offset0],dtype=float)")
    exec("params%d, success%d = scipy.optimize.leastsq(residual,firstGuess,args=(x,laser%d))"%(i,i,i))


# ------------------------------- Plots ----------------------------------

for i in range(1,20):
    exec("plt.figure(figsize=(8,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.plot(x, laser%d,'.')"%i)
    exec("plt.plot(x, sineFit(params%d,x))"%i)
    exec("plt.savefig('./sineWaves/sineFit%d.png',dpi=150)"%i)

for i in range(1,20):
    exec("plt.figure(figsize=(8,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.plot(xBrewster, brewster%d_1,'.')"%i)
    exec("plt.savefig('./brewsterAngles/brewster%d_1.png',dpi=150)"%i)
    exec("plt.plot(xBrewster, brewster%d_2,'.')"%i)
    exec("plt.savefig('./brewsterAngles/brewster%d_2.png',dpi=150)"%i)
"""


s = 2*numpy.pi*f
s = numpy.multiply(s,xvals)
s = numpy.subtract(s,p1[1])
yvals = numpy.sin(s)
yvals = numpy.multiply(p1[0],yvals)
yvals = numpy.add(yvals,p1[2])

#plt.plot(xvals,yvals)
"""

