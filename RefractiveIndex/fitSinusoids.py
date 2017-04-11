import numpy 
from scipy.optimize import leastsq 
import matplotlib.pyplot as plt 
import scipy.io

# ----------------------------- IMPORTING DATA ------------------------------

f = open('./data/baseline.csv','r')
bl = []
for line in f:
	l = line.strip('\n').strip('\r').split(',')
	try:
		l = [float(n) for n in l]
		bl.append(l[1])
	except ValueError:
		continue
baseline = (numpy.mean(bl))
f.close()


f = open('./data/high.csv')
maxintensity = []
for line in f:
	l = line.strip('\n').strip('\r').split(',')
	try:
		l = [float(n) for n in l]
		maxintensity.append(l[1])
	except ValueError:
		continue
f.close()
maxintensity = numpy.subtract(maxintensity,baseline)

for i in range(1,4):
	exec("f = open('./data/sw%d.csv','r')"%(i))
	exec("sw%d = []"%(i))
	for line in f:
		l = line.strip('\n').strip('\r').split(',')
		try:
			l = [float(n) for n in l]
			exec("sw%d.append(l)"%(i))
		except ValueError:
			continue
	f.close()
	exec("sw%d = numpy.transpose(sw%d)"%(i,i))
	exec("sw%d[1] = sw%d[1]-min(sw%d[1])"%(i,i,i))
	exec("sw%d[0] = sw%d[0]-min(sw%d[0])"%(i,i,i))

sound = scipy.io.loadmat('./data/181hz.mat')
sound_sw1 = numpy.transpose(sound['y'])
t_sw1 = numpy.transpose(sound['x'])
sound = scipy.io.loadmat('./data/494.mat')
sound_sw2 = numpy.transpose(sound['y'])
t_sw2 = numpy.transpose(sound['x'])
sound = scipy.io.loadmat('./data/777.mat')
sound_sw3 = numpy.transpose(sound['x'])
t_sw3 = numpy.transpose(sound['y'])

# ----------------------------- DATA PARAMETERS -----------------------------

# frequency of light, Hz 
f = 1000

# ambient pressure, Pa 
patm = 101000

# tube diameter, m
d = 10.0/100

# tube length, m 
l = 56.0/100
# wavelength of sound, m - first harmonic
ws = 4*d

# wavelength of laser light
wl = 633.0*10**(-9)

# baseline refractive index of air 
n0 = 1.0

#  baseline intensity (mV)
I0 = numpy.mean(maxintensity)

# decibel level of sound 
L = -10

# frequency of sound, Hz 
fs = 343.0/ws

# reference sound pressure in air 
p0 = 2.0*10**(-5)

# predicted ntube times 
t0 = numpy.linspace(min(sw1[0]),max(sw1[0]),1500)

# -------------------------- PRED. REFRACTIVE INDEX -------------------------

# sound wave pressure, Pa 
p = 10**((p0*L)/20)
# predicted tube refractive index 
nt_pred = n0+p/patm*numpy.sin(2*numpy.pi*fs*t0+numpy.pi)

# ----------------------------- PHASE SHIFT ---------------------------------

def phi(data):
	toreturn = []
	for i in range(len(data)):
		if(numpy.sqrt(2*numpy.divide(data[i],numpy.mean(maxintensity)))>1):
			toreturn.append(2*numpy.arccos(1))
		else:
			toappend = (2*numpy.arccos(numpy.sqrt(2*numpy.divide(data[i],numpy.mean(maxintensity)))))
			#while(toappend>=2*numpy.pi):
			#	toappend = toappend-2*numpy.pi
			toreturn.append(toappend)
	return(toreturn)

# phi(t) for all data sets
for i in range(1,4): 
	exec("phi_%d = phi(sw%d[1])"%(i,i))

# phase shift with no pressure
phi0 = numpy.arccos(numpy.sqrt(2*numpy.mean(maxintensity)))

# -------------------------- OBSERVED REFRACTIVE INDEX ----------------------

for i in range(1,4):
	exec("nt_%d = 1+numpy.divide(numpy.multiply(wl,numpy.divide(phi_%d,2*numpy.pi)),d)"%(i,i))

# ----------------------------- INTENSITY FITTING DATA ---------------------------

def cos2(p,x): 
	amp = p[0]
	phase = p[1] 
	freq = p[2]
	off = p[3]

	s = numpy.multiply(freq, numpy.subtract(x,phase))
	s = numpy.cos(s)
	s = numpy.multiply(amp,s)

	return numpy.square(s)

def residual(p,x,y):
	return numpy.subtract(y,cos2(p,x))


# --------------------------- EVALUATION OF FIT ------------------------------

for i in range(1,2): 
	exec("fg = [(max(sw%d[1])-min(sw%d[1])),0.0,700,numpy.mean(sw%d[1])]"%(i,i,i))
	exec("params_%d,success%d = leastsq(residual,fg,args=(sw%d[0],sw%d[1]),maxfev=1000)"%(i,i,i,i))


# ----------------------------- PRINTING DATA --------------------------------
print("REFRACTIVE INDICES")
print(numpy.mean(nt_1))
print(numpy.mean(nt_2))
print(numpy.mean(nt_3))

# ----------------------------- GENERATING PLOTS -----------------------------
"""

for i in range(1,4):
	plt.figure(figsize=(10,6), dpi=150)
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.xlabel("Time (ms)")
	plt.ylabel("$\phi$ (rad)",fontsize=12)
	plt.title("Phase shift angle vs. time")
	exec("plt.xlim([0,max(sw%d[0])])"%(i))
	exec("plt.plot(sw%d[0],phi_%d,'+')"%(i,i))
	exec("plt.savefig('phase%d.png',dpi=500)"%(i))

for i in range(1,4):
	plt.figure(figsize=(10,6), dpi=150)
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.xlabel("Time (ms)")
	plt.ylabel("Signal (V)",fontsize=12)
	plt.title("Photodiode response to interference vs. time")
	exec("plt.xlim([0,max(sw%d[0])])"%(i))
	exec("plt.errorbar(sw%d[0],sw%d[1],yerr=0.00005,fmt='+')"%(i,i))
	exec("plt.savefig('sw%d.png',dpi=500)"%(i))

# ------------------------------- TESTING CODE -------------------------------

test = numpy.arange(0,25,0.1)
sin1 = numpy.multiply(5,numpy.sin(test))
sin1 = sin1+10
test2 = test+2
sin2 = numpy.sin(test2)
sin2 = sin2+12

amp1_fg = 0.5*(max(sin1)-min(sin1))
phase1_fg = 0.0
offset1_fg = numpy.mean(sin1)
fg1 = numpy.array([amp1_fg,phase1_fg,offset1_fg])
params1, success1 = leastsq(residual,fg1,args=(test,sin1))
print(params1)

amp2_fg = 0.5*(max(sin2)-min(sin2))
phase2_fg = 0.0
offset2_fg = numpy.mean(sin2)
fg2 = numpy.array([amp2_fg,phase2_fg,offset2_fg])
params2, success2 = leastsq(residual,fg2,args=(test,sin2))
print(params2)

guess2 = sine(params2,[test2[0],0,test2[2]])
plt.plot(test,sin2,'+')
plt.plot(test,sin2)
guess1 = sine(params1,[test[0],0,test[2]])
plt.plot(test,sin1,'+')
plt.plot(test,sin1)
plt.show()
"""