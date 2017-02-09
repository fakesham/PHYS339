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

params = lineData[0]
cov = lineData[1]

m = params[0]
b = params[1]
mErr = cov[0][0]
bErr = cov[1][1]

plotx = numpy.arange(0,max(xvals),0.1)
ploty = [m*plotx[i]+b for i in range(len(plotx))]


lineData = numpy.polyfit(xvals,data,1,cov=True)


predValues = [m*xvals[i]+b for i in range(len(xvals))]
yErr = [numpy.sqrt(mErr*xvals[i]**2+bErr) for i in range(len(xvals))]

residuals = numpy.subtract(predValues,data)

os.chdir('./ADC')

plt.errorbar(xvals, residuals,yerr=yErr,fmt='o')
plt.plot([0,max(xvals)],[0,0])
plt.show

numpy.savetxt('linFitData.txt',params)