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

plt.ioff()

# ----------------------------- Importing data ------------------------------------

f =  1.0/360.0

x = numpy.arange(0,720,1)
xBrewster = numpy.arange(0,360,1)

intensityData = numpy.loadtxt('./intensitydata.txt')

for i in range(1,50):
    exec("filter%d = numpy.concatenate((numpy.loadtxt('./sineWaves/rawdata/polarizationwithfilter%d.txt')[0],numpy.loadtxt('./sineWaves/rawdata/polarizationwithfilter%d.txt')[1]))"%(i,i,i))
    exec("nofilter%d = numpy.concatenate((numpy.loadtxt('./sineWaves/rawdata/polarizationunfiltered%d.txt')[0],numpy.loadtxt('./sineWaves/rawdata/polarizationunfiltered%d.txt')[1]))"%(i,i,i))

for i in range(1,20):    
    exec("nopolarizer%d = numpy.concatenate((numpy.loadtxt('./sineWaves/rawdata/laserSineWave%d.txt')[0],numpy.loadtxt('./sineWaves/rawdata/laserSineWave%d.txt')[1]))"%(i,i,i))

for i in range(1,100):
    exec("brewster%d_1 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[0]"%(i,i))
    exec("brewster%d_2 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[1]"%(i,i))
error = 0.5

# ----------------------------- Least-squares fitting -----------------------------
def malusFit(p,x):
    amp = p[0]
    freq = 2*numpy.pi*f
    phase = p[1]
    offset = p[2]
    
    s = numpy.multiply(freq, numpy.subtract(x,phase))
    s = numpy.cos(s)
    s = s**2
    return numpy.add(numpy.multiply(amp,s),offset)
    
def residual(p,x,y):
    return numpy.subtract(y,malusFit(p,x))

for i in range(1,50):
    exec("amp0 = 0.5*(max(filter%d)-min(filter%d))"%(i,i))
    exec("phase0 = 0")
    exec("offset0 = numpy.mean(filter%d)"%i)
    exec("firstGuess = numpy.array([amp0, phase0, offset0],dtype=float)")
    exec("paramsF%d, successF%d = scipy.optimize.leastsq(residual,firstGuess,args=(x,filter%d))"%(i,i,i))
    exec("resF%d = residual(paramsF%d,x,filter%d)"%(i,i,i))

    exec("amp0 = 0.5*(max(nofilter%d)-min(nofilter%d))"%(i,i))
    exec("phase0 = 0")
    exec("offset0 = numpy.mean(nofilter%d)"%i)
    exec("firstGuess = numpy.array([amp0, phase0, offset0],dtype=float)")
    exec("paramsNF%d, successNF%d = scipy.optimize.leastsq(residual,firstGuess,args=(x,nofilter%d))"%(i,i,i))
    exec("resNF%d = residual(paramsNF%d,x,nofilter%d)"%(i,i,i))

# ----------------------------- Quadratic fitting -----------------------------


deltas = [0]

for i in range(1,200):
    deltas.append(numpy.abs(intensityData[1][i]-intensityData[1][i-1]))

deltas = numpy.divide(deltas,intensityData[0][1]-intensityData[0][0])

start = 0 
stop = 0 

threshold = numpy.std(deltas)

for i in range(200):
    if(numpy.abs(deltas[i])<=threshold):
        continue
    start = i 
    break

for i in range(199,start,-1): 
    if(numpy.abs(deltas[i])<=threshold):
        continue 
    stop = i 
    break

toFitX = intensityData[0][start:stop]
observedY = intensityData[1][start:stop]

params = numpy.polyfit(toFitX,observedY,2)
bfYvals = params[0]*toFitX**2+params[1]*toFitX+params[2]

residuals = []
for i in range(len(bfYvals)):
    residuals.append(bfYvals[i]-observedY[i])



# ------------------------------- Plots ----------------------------------
"""
# Intensity quadratic fitting 
plt.figure(figsize=(10,6), dpi=150)
plt.xlabel('Intensity value sent to Arduino',fontsize=12)
plt.ylabel('Photoresistor reading value returned from Arduino',fontsize=12)
plt.plot(toFitX,bfYvals,label='Best-fit quadratic curve')
plt.plot(toFitX,observedY,'.')
plt.plot(intensityData[0],intensityData[1],'.')
plt.legend(loc='upper left')
plt.savefig('./intensityQuadFit.png')

# Residuals for intensity quadratic fitting 
plt.figure(figsize=(10,5), dpi=150)
plt.xlabel('Intensity value sent to Arduino',fontsize=12)
plt.ylabel('Residual value \n(observed return value - actual return value)',fontsize=12)
plt.axhline(color='black')
plt.plot(toFitX,residuals,'.')
plt.savefig('./intensityQuadFitResiduals.png')

# Intensity calibration 
plt.figure(figsize=(10,6), dpi=150)
plt.xlabel('Intensity value sent to Arduino',fontsize=12)
plt.ylabel('Photoresistor reading value returned from Arduino',fontsize=12)
plt.plot(intensityData[0],intensityData[1],'+')
plt.savefig('./intensityCalibration.png')

# Intensity calibration - with filter 
plt.figure(figsize=(10,6), dpi=150)
plt.xlabel('Intensity value sent to Arduino filter',fontsize=12)
plt.ylabel('Photoresistor reading value returned from Arduino',fontsize=12)
plt.plot(x,nopolarizer6,'.')
plt.savefig('./polarizationCalibration.png')

# Sinusoidal - filter
for i in range(1,50):
    exec("plt.figure(figsize=(10,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.errorbar(x, filter%d,yerr=error,fmt='.',ms=5)"%i)
    exec("plt.plot(x, malusFit(paramsF%d,x),color='red')"%i)
    exec("plt.savefig('./sineWaves/filter/malusFitF%d.png',dpi=150)"%i)

# Sinusoidal - no filter
for i in range(1,50):
    exec("plt.figure(figsize=(10,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.errorbar(x, nofilter%d,yerr=error,fmt='.',ms=5)"%i)
    exec("plt.plot(x, malusFit(paramsNF%d,x),color='red')"%i)
    exec("plt.savefig('./sineWaves/nofilter/malusFitNF%d.png',dpi=150)"%i)

# Residuals - filter
for i in range(1,50):
    exec("plt.figure(figsize=(10,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Residual value',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.plot(x, resF%d,'.')"%i)
    exec("plt.savefig('./sineWaves/residualsfilter/residualF%d.png',dpi=150)"%i)

# Residuals - no filter
for i in range(1,50):
    exec("plt.figure(figsize=(10,6), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Residual value',fontsize=12)")
    exec("plt.xlim([0,720])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.plot(x, resNF%d,'.')"%i)
    exec("plt.savefig('./sineWaves/residualsnofilter/residualNF%d.png',dpi=150)"%i)

# Brewster angle 
for i in range(1,100):
    exec("plt.figure(figsize=(10,10), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,360])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.errorbar(xBrewster, brewster%d_1,yerr=error,fmt='.',ms=5)"%i)
    exec("plt.savefig('./brewsterAngles/brewster%d_1.png',dpi=150)"%i)

# Brewster angle 
for i in range(1,100):
    exec("plt.figure(figsize=(10,10), dpi=150)")
    exec("plt.xlabel('Step number',fontsize=12)")
    exec("plt.ylabel('Value returned from Arduino',fontsize=12)")
    exec("plt.xlim([0,360])")
    exec("plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))")
    exec("plt.errorbar(xBrewster, brewster%d_2,yerr=error,fmt='.',ms=5)"%i)
    exec("plt.savefig('./brewsterAngles/brewster%d_2.png',dpi=150)"%i)
"""