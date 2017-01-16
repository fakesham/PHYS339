# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 17:28:03 2017

@author: mark.orchard-webb
"""

import numpy
import matplotlib.pyplot as p
#Set custom properties of matplotlib
#matplotlib will interpret all text as LaTeX
p.rcParams['text.usetex'] = True
p.rcParams['text.latex.unicode']= False
p.rcParams['mathtext.fontset'] = 'stix'
p.rcParams['font.family'] = 'STIXGeneral'
p.rcParams['figure.autolayout'] = True
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#from itertools import izip 



t = numpy.load("t.npy")
a = numpy.load("a.npy")
b = numpy.load("b.npy")
c = numpy.load("c.npy")
d = numpy.load("d.npy")

#print "Shape of Function a (blue) and b (green)",a.shape

# Plot a figure to see what the data looks like
if False:
    p.figure()
    p.xlabel(r'Time [s]')
    p.ylabel(r'Sample value')
    p.errorbar(t,a[:,0],a[:,1],fmt='none',errorevery=3,label="Signal a")
    #p.errorbar(t,b[:,0],b[:,1],fmt='none',errorevery=3)
    #p.errorbar(t,c[:,0],c[:,1],fmt='none',errorevery=3)
    #p.errorbar(t,d[:,0],d[:,1],fmt='none')

# once you have written all the required functions, the following
# should work, and give correct results
"""
def rms(t,x):
    square = multiply(x,x)
    mean = integral(t,square)[1] # not true yet!!!
    mean[1:,:] = numpy.column_stack((t,t))[1:,:]
    mean[0,:] = 0  # this is probably a matter of dogma
    return sqrt(mean)
"""
def rms(t,x):
    square = multiply(x,x)
    mean = integral(t,square) # not true yet!!!
    mean[1:,:] = numpy.column_stack((t,t))[1:,:]
    mean[0,:] = 0  # this is probably a matter of dogma
    return sqrt(mean)
    
if False:
    d_rms = rms(t,d)
    p.figure()
    p.errorbar(t,d_rms[:,0],d_rms[:,1])

# As a free gift, here is a correct implementation of add

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
        uncerty[x] = (1/(ttwo-tone))*numpy.sqrt((errY2**2)-(errY1**2))
        
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

mult = multiply(a,a)
foo = derivative(t,a)    
bar = integral(t,a)    
drms = rms(t,d)
    
"""# Plotting Graph of a"""
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'Sample value',fontsize=12)
p.errorbar(t,a[:,0],a[:,1],fmt='none',errorevery=1,label="Signal a")

p.savefig('a.png',dpi=150,pad_inches=0.4) 

"""# Plotting a^2"""
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'Sample value',fontsize=12)
p.errorbar(t,mult[:,0],mult[:,1],fmt='none')

p.savefig('asquare.png',dpi=150,pad_inches=0.4) 

""" Plotting derivative of a """
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'$ \frac{d}{dt} (signal) \left[ \displaystyle\frac{1}{s} \right] $',fontsize=16)
p.errorbar(foo[:,0],foo[:,1],foo[:,2],fmt='none')

p.savefig('aderiv.png',dpi=150,pad_inches=0.4) 


""" Plotting integral of a """
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'$\int (signal) \ dt \ [s]$',fontsize=12)
p.errorbar(t,bar[:,0],bar[:,1],fmt='none')

p.savefig('aintegral.png',dpi=150,pad_inches=0.4) 

""" Plotting Graph of d """
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'$Sample value$',fontsize=12)
p.errorbar(t,d[:,0],d[:,1],fmt='none')

p.savefig('d.png',dpi=150,pad_inches=0.4) 

""" Plotting rms of d """
p.figure(figsize=(5,4), dpi=150)
p.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
p.xlabel(r'Time [s]',fontsize=12)
p.ylabel(r'$RMS \ signal$',fontsize=12)
p.errorbar(t,drms[:,0],drms[:,1],fmt='none')

p.savefig('drms.png',dpi=150,pad_inches=0.4) 



# I can verify correctness using known quantity
## known = 2000*numpy.sqrt(2)*numpy.sin(100*2*numpy.pi*t+numpy.pi/4)
    
    


    
