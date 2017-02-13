# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:38:28 2017

@author: shammamah.hossain
"""
import numpy 
import os 
from scipy import stats
import matplotlib.pyplot as plt 

data = numpy.loadtxt('calibrationData.txt')

xvals = numpy.empty(len(data))

for i in range(len(xvals)-1):
    xvals[i] = 10*i
xvals[len(data)-1] = 255

lineData = numpy.polyfit(xvals,data,2,cov=True)

params = lineData[0]
cov = lineData[1]

a = params[0]
b = params[1]
c = params[2]
aErr = cov[0][0]
bErr = cov[1][1]
cErr = cov[2][2]

plotx = numpy.arange(0,max(xvals),0.1)
ploty = [a*plotx[i]**2+b*plotx[i]+c for i in range(len(plotx))]


predValues = [a*xvals[i]**2+b*xvals[i]+c for i in range(len(xvals))]
yErr = [numpy.sqrt(aErr*xvals[i]**2+(bErr)*xvals[i]**2+cErr) for i in range(len(xvals))]

residuals = numpy.subtract(predValues,data)

os.chdir('./ADC')

plt.errorbar(xvals, residuals,yerr=yErr,fmt='o')
plt.plot([0,max(xvals)],[0,0])
plt.show

numpy.savetxt('quadFitData.txt',params)