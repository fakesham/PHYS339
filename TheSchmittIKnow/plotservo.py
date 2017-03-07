import matplotlib.pyplot as plt
import scipy.io as sio
import numpy
import os


data = numpy.load('./servo/servo.npz')
print(len(data))

plt.plot(data['time'][0],data['temperature'][0])
plt.show()
