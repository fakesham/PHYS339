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


#the 50th entry was invalid data (all zeros)
angleOnes = numpy.delete(angleOnes,50)
angleTwos = numpy.delete(angleTwos,50)


compiledData = numpy.column_stack((angleOnes,angleTwos))

numpy.savetxt('./brewsterAngles/angleData.txt',compiledData)

<<<<<<< HEAD
normedDiff = numpy.subtract(angleOnes,angleTwos)
numBins = numpy.ceil(numpy.sqrt(len(normedDiff)))

normx = numpy.linspace(min(normedDiff),max(normedDiff),100)
p = norm.pdf(normx, numpy.mean(normedDiff),numpy.std(normedDiff))
pScaled = numpy.divide(p,numpy.sum(p))
k = numpy.random.choice(normx,size=10000,p=pScaled)

=======
rootSquareDiff = numpy.sqrt(numpy.square(numpy.subtract(angleOnes,angleTwos)))
>>>>>>> parent of 85313db... Add updated code for Brewster analysis

plt.figure(figsize=(8,6), dpi=150)
plt.hist(rootSquareDiff,bins=10,normed=True)
plt.xlabel("Root squared difference between angles (degrees)",fontsize=12)
plt.ylabel("Frequency",fontsize=12)
plt.hist(rootSquareDiff,bins=10)
plt.savefig('./brewsterAngles/angleDiff.png')

