# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:19:50 2017

@author: mark.orchard-webb
"""

import numpy
import matplotlib.pyplot as p

def load_geiger(filename="geiger.npz"):
    return numpy.load(filename)["histogram"]

h = load_geiger("sample.npz");
replicas = numpy.size(h,axis=0)
columns = numpy.size(h,axis=1)

