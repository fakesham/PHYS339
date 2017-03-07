# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:01:13 2017

@author: shammamah.hossain
"""

# -------------------- Basic operations ----------------------------

def add(x,y):
    values = x[:,0] + y[:,0]
    errorbars = numpy.sqrt(x[:,1]**2 + y[:,1]**2)
    return numpy.column_stack((values,errorbars))


def sqrt(y):
    values = numpy.sqrt(y[:,0])
    errorbars = numpy.sqrt(0.25 * (y[:,1]**2/y[:,0]))
    return numpy.column_stack((values, errorbars))
    
def multiply(y1,y2):
    values = y1[:,0]*y2[:,0]
    errorbars = numpy.sqrt((y1[:,0]*y2[:,1])**2+(y2[:,0]*y1[:,1])**2)
    return numpy.column_stack((values,errorbars))
    
# -------------------- Derivative/integral ----------------------------
    
# Input: t, array of time values; y, array of y values.
# Output: an array with three columns: derivative values, midtime, associated uncertainty. 
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

# Input: t, array of time values; y, array of y values.
# Output: array of output integral values and associated uncertainty 
def integral(t,y):
    totArea = 0
    values = numpy.zeros(len(y[:,1]))
    uncerty = numpy.zeros(len(y[:,1]))
    currUncerty = 0
    output = numpy.zeros((len(y[:,1]),2))
    
    length = len(y[:,1])
    # values = 0.5*(t2-t1)(y2-y1)
    
    for x in range(0, (length-1)): 
        ytwo = y[x+1,0]
        yone = y[x,0]
        ttwo = t[x+1]
        tone = t[x]
        # area of the trapezoid defined by every pair of consecutive points
        values[x] = totArea+0.5*(ttwo-tone)*(ytwo+yone)
        totArea+=0.5*(ttwo-tone)*(ytwo+yone)
        # error on integral
        errY1 = y[x,1]
        errY2 = y[x+1,1]
        combinedYerr = (errY2**2)+(errY1**2)
        uncerty[x] = numpy.sqrt(((((ttwo-tone)/2)**2)*combinedYerr)+currUncerty**2)
        currUncerty = uncerty[x]
        
    output = numpy.column_stack((values,uncerty))
    
    return output

# -------------------- Stats ----------------------------  
  
def mean(trials): 
    tot = 0
    for i in range(len(trials)):
        tot += ((i)*trials[i])
    return (float)(tot/(len(trials)))
    
# input: one row (one trial of 20)
def variance(trials, mean): 
    varSum = 0
    for j in range(len(trials)): 
        varSum += trials[j]*(trials[j]-mean)**2
    return (float)(varSum/(len(trials)-1))