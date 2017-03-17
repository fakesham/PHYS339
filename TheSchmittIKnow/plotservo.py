import matplotlib.pyplot as plt
import scipy.io as sio
import numpy
import os 

files = os.listdir('./servo')

numpy.load('./servo/cooling.npz')

"""
for f in files: 
    if('.npz' in f):
        toOpen = './servo/'+f
        numpy.load(toOpen)
        break
"""