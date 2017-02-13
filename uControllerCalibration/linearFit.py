# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:38:28 2017

@author: shammamah.hossain
"""
import numpy 
import os 
import matplotlib.pyplot as plt 

data = numpy.loadtxt('calibrationData.txt')

xvals = numpy.empty(len(data))

for i in range(len(xvals)-1):
    xvals[i] = 10*i
xvals[len(data)-1] = 255

lineData = numpy.polyfit(xvals,data,1,cov=True)

params = lineData[0]
cov = lineData[1]

m = params[0]
b = params[1]
mErr = cov[0][0]
bErr = cov[1][1]

plotx = numpy.arange(0,max(xvals),0.1)
ploty = [m*plotx[i]+b for i in range(len(plotx))]


predValues = [m*xvals[i]+b for i in range(len(xvals))]
yErr = [numpy.sqrt(mErr*xvals[i]**2+bErr) for i in range(len(xvals))]

residuals = numpy.subtract(predValues,data)

os.chdir('./ADC')

plt.figure(figsize=(8,6), dpi=150)
plt.xlabel("Value sent to Arduino",fontsize=12)
plt.ylabel("Voltage measured (V)",fontsize=12)
axes = plt.gca()
axes.set_xlim([0,max(xvals)])
plt.plot(xvals,predValues,color='red',label="Line of best fit")
plt.plot(xvals,data,'+')
plt.legend(fontsize=8)
plt.savefig('linFit.png')

plt.figure(figsize=(12,6), dpi=150)
plt.xlabel("Value sent to Arduino",fontsize=12)
plt.ylabel("Residual value (V) \n (voltage predicted - voltage observed)",fontsize=12)
axes = plt.gca()
axes.yaxis.labelpad = 0 
axes.set_xlim([0,350])
plt.errorbar(xvals, residuals,yerr=yErr,fmt='o')
plt.plot([0,max(xvals)],[0,0])
plt.savefig('linFitRes')

numpy.savetxt('linFitData.txt',params)