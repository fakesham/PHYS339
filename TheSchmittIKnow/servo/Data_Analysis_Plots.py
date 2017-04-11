# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 01:53:04 2017

@author: joseph
"""
import serial
import numpy
from scipy import stats
import matplotlib.pyplot as p
import math
import pylab

def derivative (t,y):
    values = numpy.zeros(len(y[:,1]))
    midtime = numpy.zeros(len(y[:,1]))
    uncerty = numpy.zeros(len(y[:,1]))
    
    length = len(y[:,1])
        
    # Iterate over the length of the y array minus 1
    for x in range(0, (length-1)):
        ytwo = y[x+1,0]
        yone = y[x,0]
        ttwo = t[x+1]
        tone = t[x]
        values[x]=((ytwo-yone)/(ttwo-tone))
        midtime[x]=((ttwo+tone)/2)

        # uncertainty calculations
        errY1 = y[x,1]
        errY2 = y[x+1,1]
        #num = numpy.sqrt(numpy.square(errY1)+numpy.square(errY2))
        #denom = ytwo-yone
        uncerty[x] = (1/(ttwo-tone))*numpy.sqrt((errY2**2)+(errY1**2))
        
    #toReturn = numpy.concatenate((values,midtime,uncerty),axis=1)
    #toReturn = numpy.transpose(toReturn)
    toReturn = numpy.column_stack((midtime,values,uncerty))

    return toReturn

timeonoff = numpy.load('heatingto350_onoff/time.npy')
onoff = numpy.load('heatingto350_onoff/temperature.npy')

timeprop = numpy.load('heatingto350_proportional/time.npy')
prop = numpy.load('heatingto350_proportional/temperature.npy')

propinttime = numpy.load('heatingto350_iat8_cb0_b5/time.npy')
propint = numpy.load('heatingto350_iat8_cb0_b5/temperature.npy')

propintdertime = numpy.load('heatingto350_iat8_cb1_b5/time.npy')
propintder = numpy.load('heatingto350_iat8_cb1_b5/temperature.npy')

steadytime = numpy.load('steadystate330/time.npy')
steadytemp = numpy.load('steadystate330/temperature.npy')
steadyout = numpy.load('steadystate330/out.npy')

responsetime = numpy.load('responsetime/time.npy')
responsetemp = numpy.load('responsetime/temperature.npy')

backgroundtime = numpy.load('roomtemp/time.npy')
backgroundtemp = numpy.load('roomtemp/temperature.npy')

"""
timeprop = numpy.load('heatingto350_proportional/time.npy')
prop = numpy.load('heatingto350_proportional/temperature.npy')
"""

onoffrange = range(203,667)
onoffmod = [onoff[i] for i in onoffrange]
onoffmodtime = [timeonoff[i-203] for i in onoffrange]

proprange = range(36,1522)
propintrange = range(156,1530)
propintderange = range(49,1522)
steadytemprange = range(500,1768)
responsetemprange = range(160,329)

propmod = [prop[i] for i in proprange]
propmodtime = [timeprop[i-36] for i in proprange]

propintmod = [propint[i] for i in propintrange]
propintmodtime = [propinttime[i-156] for i in propintrange]

propintdermod = [propintder[i] for i in propintderange]
propintdermodtime = [propintdertime[i-49] for i in propintderange]

steadytempmod = [steadytemp[i] for i in steadytemprange]
steadyoutmod = [steadyout[i] for i in steadytemprange]
steadytimemod = [steadytime[i-500] for i in steadytemprange]
avgout = numpy.mean(steadyoutmod)

avgbackground = numpy.mean(backgroundtemp)
avgbackgrounstd = numpy.std(backgroundtemp)

responseregiontemp = [responsetemp[i] for i in responsetemprange]
responseregiontime = [responsetime[i] for i in responsetemprange]
linearplottime = [responsetime[i-50] for i in responsetemprange]

slope, intercept, rval, pval, stderr = scipy.stats.linregress(onoffmodtime,onoffmod)
rsquare = rval*rval

slope2, intercept2, rval2, pval2, stderr2 = scipy.stats.linregress(responseregiontime,responseregiontemp)
rsquare2 = rval2*rval2


p.figure(figsize=(8,6), dpi=90)
p.axhline(350, color = 'k')
p.plot(propmodtime,propmod,color = 'b')
p.plot(propintmodtime,propintmod,color = 'g')
p.plot(propintdermodtime,propintdermod,color = 'r')
p.xlabel("t [s]")
p.ylabel("T [K]")
p.legend(["350 Kelvin","Proportional Control","PD Control","PID Control"],loc="bottom right")
p.savefig("threecomparison.jpeg",dpi=600)

"""
p.figure(figsize=(8,6), dpi=90)
p.plot(timeonoff,onoff)
"""
p.figure(figsize=(8,6), dpi=90)
p.plot(onoffmodtime,onoffmod)
p.xlabel("t [s]")
p.ylabel("T [K]")
p.legend(["f(x) = 0.537 + 321, R^2 = 0.99"],loc="bottom right")
p.savefig("constant_heating.jpeg",dpi=600)


p.figure(figsize=(8,6), dpi=90)
p.plot(steadytimemod,steadytempmod,color = 'b')
p.plot(steadytimemod,steadyoutmod,color = 'g')
p.xlabel("t [s]")
p.legend(["Temperature [K]", "Output [Arbitrary DAC Value]"],loc="lower right")
p.savefig("steadytemperature.jpeg",dpi=600)

p.figure(figsize=(8,6), dpi=90)
p.plot(timeonoff,onoff)
p.xlabel("t [s]")
p.ylabel("T [K]")
p.savefig("schmitt.jpeg",dpi=600)

p.figure(figsize=(8,6), dpi=90)
p.plot(backgroundtime,backgroundtemp,color='r')
p.ylim([295.5,296.5])
p.xlabel("t [s]")
p.ylabel("T [K]")
p.savefig("background.jpeg",dpi=600)

p.figure(figsize=(8,6), dpi=90)
y1 = (numpy.multiply(linearplottime,slope2)+intercept2);
p.plot(linearplottime,y1,color='k')
p.plot(responsetime,responsetemp,color='r')
p.xlabel("t [s]")
p.ylabel("T [K]")
p.legend(["f(x) =  0.596 + 308, R^2 = 0.99"],loc="upper left")
p.savefig("responsetime.jpeg",dpi=600)


"""
p.figure(figsize=(8,6), dpi=90)
    p.plot(i,x)
    p.plot(i,xoutput)     
    p.figure(figsize=(8,6), dpi=600)
    p.plot(i,x)
    p.plot(i,xoutput)
    p.xlabel("t")
    p.ylabel("8-Bit Voltage Value")
    p.legend(["Desired Output","Output Sent to DAC"],loc="upper left")
    p.savefig("trianglewave.jpeg",dpi=600)
    """
    