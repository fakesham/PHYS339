import matplotlib.pyplot as plt
import scipy.io as sio
import numpy


data = numpy.load('./servo/servo.npz')
d = data.files


plt.plot(data['time'][0],data['temperature'][0])
plt.show()
