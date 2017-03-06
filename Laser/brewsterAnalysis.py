# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:22:09 2017

@author: mammam
"""

import numpy 
import scipy
from scipy.optimize import leastsq
from scipy.stats import norm 
import matplotlib.pyplot as plt
import os

# ----------------------------- Importing data ------------------------------------

xBrewster = numpy.arange(0,360,1)

angleOnes = numpy.zeros(100)
angleTwos = numpy.zeros(100)

for i in range(50): 
    exec("brewster%d_1 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[0]"%(i,i*2))
    exec("brewster%d_2 = numpy.loadtxt('./brewsterAngles/rawdata/brewsterbesteverest%d.txt')[1]"%(i,i*2))

# ----------------------------- Getting Brewster angles -----------------------------

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
stderr1 = numpy.std(angleOnes)/numpy.sqrt(len(angleOnes))
stderr2 = numpy.std(angleTwos)/numpy.sqrt(len(angleTwos))

print("Angle ones: "+str(numpy.mean(angleOnes))+" (+/-) "+str(stderr1))
print("Angle twos: "+str(numpy.mean(angleTwos))+" (+/-) "+str(stderr2))

# ----------------------------- Compiling/saving processed data -----------------------------

compiledData = numpy.column_stack((angleOnes,angleTwos))
numpy.savetxt('./brewsterAngles/angleData.txt',compiledData)

q = numpy.ndarray.flatten(compiledData)

print("Final angle: "+str(numpy.mean(q))+"(+/-) "+str(numpy.std(q)/numpy.sqrt(len(q))))

stderr = numpy.std(q)/numpy.sqrt(len(q))

# ----------------------------- Index of refraction -----------------------------

meanAngle = numpy.mean(q)*numpy.pi/180.0
meanAngleOne = numpy.mean(angleOnes)*numpy.pi/180.0
meanAngleTwo = numpy.mean(angleTwos)*numpy.pi/180.0
stderr = numpy.std(q)/numpy.sqrt(len(q))*numpy.pi/180.0
stderr1 = numpy.std(angleOnes)/numpy.sqrt(len(angleOnes))*numpy.pi/180.0
stderr2 = numpy.std(angleTwos)/numpy.sqrt(len(angleTwos))*numpy.pi/180.0

print("n1 overall = "+str(numpy.tan(meanAngle))+" (+/-) "+str(numpy.square(stderr/numpy.cos(meanAngle)**2)))
print("n1 angle 1 = "+str(numpy.tan(meanAngleOne))+" (+/-) "+str(numpy.square(stderr1/numpy.cos(meanAngleOne)**2)))
print("n1 angle 2 = "+str(numpy.tan(meanAngleTwo))+" (+/-) "+str(numpy.square(stderr2/numpy.cos(meanAngleTwo)**2)))

manAngle = 57.64*numpy.pi/180.0
manErr = 0.01*numpy.pi/180.0
print("n1 manual = "+str(numpy.tan(manAngle))+" (+/-) "+str(numpy.square(manErr/numpy.cos(manAngle)**2)))
# ----------------------------- T-test -----------------------------

t,pval = scipy.stats.ttest_rel(angleOnes,angleTwos)
print("T-test p value: "+str(pval))

# ----------------------------- Comparison with Gaussian  -----------------------------

normedDiff = numpy.subtract(angleOnes,angleTwos)
numBins = numpy.ceil(numpy.sqrt(len(normedDiff)))

normx = numpy.linspace(min(normedDiff),max(normedDiff),100)
p = scipy.stats.norm.pdf(normx, numpy.mean(normedDiff),numpy.std(normedDiff))
pScaled = numpy.divide(p,numpy.sum(p))
k = numpy.random.choice(normx,size=10000,p=pScaled)

plt.figure(figsize=(10,5), dpi=150)
plt.xlabel('Difference between Brewster angles (degrees)',fontsize=12)
plt.ylabel('Frequency (normalized)',fontsize=12)
plt.hist(normedDiff,normed=True,color='lightgrey',label='Observed data')
plt.plot(normx,p,color='blue',label='Gaussian distribution')
plt.hist(k,normed=True,fill=None,edgecolor='red',label='Data generated from Gaussian distribution')
plt.legend(fontsize=10,loc='upper left')
plt.savefig('./brewsterAngles/angleDiff.png')

