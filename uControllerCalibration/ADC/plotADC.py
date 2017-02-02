# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:13:49 2017

@author: shammamah.hossain
"""

import numpy 
import matplotlib.pyplot as plt 


A0data = numpy.loadtxt('A0.txt',delimiter=',')
A1data = numpy.loadtxt('A1.txt',delimiter=',')
A2data = numpy.loadtxt('A2.txt',delimiter=',')
A3data = numpy.loadtxt('A3.txt',delimiter=',')
A4data = numpy.loadtxt('A4.txt',delimiter=',')
A5data = numpy.loadtxt('A5.txt',delimiter=',')

A0plot = []
A1plot = []
A2plot = []
A3plot = []
A4plot = []
A5plot = []

for i in range(len(A0data)): 
    if(A0data[i]!=0):
        A0plot.append(i)

for i in range(len(A1data)): 
    if(A1data[i]!=0):
        A1plot.append(i)
    
for i in range(len(A2data)): 
    if(A2data[i]!=0):
        A2plot.append(i)
    
for i in range(len(A3data)): 
    if(A3data[i]!=0):
        A3plot.append(i)
   
for i in range(len(A4data)): 
    if(A4data[i]!=0):
        A4plot.append(i)
     
for i in range(len(A5data)): 
    if(A4data[i]!=0):
        A5plot.append(i)

lineParams = numpy.loadtxt('linFitData.txt')

m = lineParams[0]
b = lineParams[1]

xvals = numpy.arange(0, 256, 0.5)
yvals = numpy.multiply(m,xvals)+b

plt.plot(xvals,yvals)
plt.plot()
