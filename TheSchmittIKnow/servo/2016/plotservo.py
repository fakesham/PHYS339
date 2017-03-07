import matplotlib.pyplot as plt
import scipy.io as sio

data = sio.loadmat('servo.mat')

plt.plot(data['time'][0],data['temperature'][0])
plt.show()
