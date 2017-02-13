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

dataXvals = [0]

i=7
while(i<256):
    dataXvals.append(i)
    i+=8


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

# Plot for raw data 
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel('Value sent to Arduino',fontsize=12)
plt.ylabel('Value received from Arduino',fontsize=12)
for i in range(6):
    exec("plt.plot(dataXvals, A%dplot, '+',label='Pin A%d')"%(i,i))
plt.plot([0,max(dataXvals)],[0,0])
legend = plt.legend(loc="upper left")

plt.savefig('analogPins.png')

# Storing linear fit data 
for i in range(6):
    exec("lineDataA%d = numpy.polyfit(dataXvals,A%dplot,1,cov=True)"%(i,i))
    exec("params%d = lineDataA%d[0]"%(i,i))
    exec("cov%d = lineDataA%d[1]"%(i,i))
    exec("m%d = params%d[0]"%(i,i))
    exec("b%d = params%d[1]"%(i,i))
    exec("mErr%d = cov%d[0][0]"%(i,i))
    exec("bErr%d = cov%d[1][1]"%(i,i))
    exec("yErr%d = [numpy.sqrt(mErr%d*dataXvals[i]**2+bErr%d) for i in range(len(dataXvals))]"%(i,i,i))
    
tableCode = open("ADCdata.txt","w+")

"""
for i in range(6): 
    exec("toWrite =('ADC%d & ' +str(m%d)+' & '+str(mErr%d)+' & '+str(b%d)+' & '+str(bErr%d)+' \\\ \hline ')"%(i,i,i,i,i))
    tableCode= tableCode+'\n'
    tableCode.write(toWrite)
"""    
tableCode.close()


predValuesA0 = [numpy.sum(numpy.multiply(m0,dataXvals[i]),b0) for i in range(len(dataXvals))]
predValuesA0 = numpy.multiply(predValuesA0,1)
residuals = numpy.subtract(predValuesA0,A0plot)
plt.figure(figsize=(12,6), dpi=150)
plt.xlabel("Value sent to Arduino",fontsize=12)
plt.ylabel("Residual value (V) \n (value predicted - value observed)",fontsize=12)
axes = plt.gca()
axes.yaxis.labelpad = 0 
axes.set_ylim([-10,10])
axes.set_xlim([0,max(dataXvals)])
plt.errorbar(dataXvals, residuals,yerr=yErr0,fmt='o')
plt.plot([0,max(dataXvals)],[0,0])
plt.savefig('A0res.png')


