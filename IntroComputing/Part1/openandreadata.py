# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 09:07:27 2017

@author: mark.orchard-webb
"""

import serial
import matplotlib.pyplot as p
import numpy

a = numpy.load('a.npy')
b = numpy.load('b.npy')
c = numpy.load('c.npy')
d = numpy.load('d.npy')
t = numpy.load('t.npy')

print "Shape of a:",a.shape

# Plot figure to see what the data looks like
if True:
    p.figure()
    p.xlabel("Time (s)")
    p.ylabel("Sample value")
    p.errorbar(t,a[:,0],a[:,1],fmt='none',errorevery=3,label="Signal a")
    p.errorbar(t,b[:,0],b[:,1],fmt='none',errorevery=3)
    p.errorbar(t,c[:,0],c[:,1],fmt='none',errorevery=3)
    p.errorbar(t,d[:,0],d[:,1],fmt='none')