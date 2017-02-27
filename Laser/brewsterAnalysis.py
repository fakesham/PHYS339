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

xBrewster = numpy.arange(0,360,1)

angleOnes = numpy.zeros(100)
angleTwos = numpy.zeros(100)

for i in range(50): 
    exec("brewster%d_1 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[0]"%(i,i*2))
    exec("brewster%d_2 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[1]"%(i,i*2))


def getSpike(data):
	ratios = []

	for i in range(2,len(data)): 
		if(data[i-2]!=0):
			ratios.append(data[i]/data[i-2])
		else:
			ratios.append(0)
   
	return numpy.argmax(ratios)+2

def getAngles(data,index):

	angleOne = numpy.argmax(data[0:180])
	angleTwo = numpy.argmax(data[180:len(data)])+180
	spike = getSpike(data)

	angleOnes[index] = 360-spike+angleOne
	angleTwos[index] = spike-angleTwo 


for i in range(50): 
	exec("getAngles(brewster%d_1,%d)"%(i,i))
for i in range(50):
	exec("getAngles(brewster%d_2,%d)"%(i,50+i))

    
compiledData = numpy.zeros(100)

compiledData = numpy.column_stack((angleOnes,angleTwos))

numpy.savetxt('./brewsterAngles/angleData.txt',compiledData)