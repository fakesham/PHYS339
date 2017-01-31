import arduino
import numpy
import matplotlib.pyplot as plt
import os

print "Creating an arduino object a"
a = arduino.arduino(debug=0)

print "Calling a.out_buffer_length() to get maximum output vector length"
length =  a.out_buffer_length()
print "Output buffer can take maximum of %d entries" % length

print "Calling a.sampling_time(10000) to determine sampling frequency"
t_sample = a.sampling_time(10000)
f_sample = 1/t_sample;
print "Sampling frequency: %f Hz" % f_sample

# generate vector 0...length-1
index = numpy.fromiter(range(0,length),int)
# generate vector 0..2pi
x = index*2*numpy.pi/length
# generate time base (for plotting)
t = t_sample * index

print "About to characterize lowpass filter on pin 10"
print "Since the sampling frequency is %f Hz, and vector length is %d," % (f_sample, length)
print "a single cycle of a sine wave spanning the vector will have the frequency"
print "f_s/length = %f Hz, I denote this the fundamental frequency."
indexes = range(0,8)
harmonics = numpy.power(2,numpy.fromiter(indexes,int))
frequencies = f_sample / length * harmonics
amplitudes = numpy.zeros_like(frequencies)
phases = numpy.zeros_like(frequencies)
for i in indexes :
  print "Generating vectors for harmonic %d (%f Hz)" % (harmonics[i],frequencies[i])
  c = numpy.cos(harmonics[i]*x)
  s = numpy.sin(harmonics[i]*x)
  # generate sine wave to send to Arduino
  values = (128+127*c).round().astype(int)
  # send vector and read back response after 1 iteration
  print "calling a.analogWriteReadVector(10,0,values,iterations=1)"
  print "PWM output pin: 10, ADC input 0, values is vector of integer values to be written"
  iv = a.analogWriteReadVector(10,0,values,iterations=1)
  print "a.analogWriteReadVector has returned vector of ADC readings"
  print "Analyzing amplitude and phase of returned vector modeled as"
  print "iv = Amplitude cos(2*pi*%f Hz t + Phase)" % frequencies[i]
  sum_c = 2*numpy.sum(c*iv)/length
  sum_s = 2*numpy.sum(s*iv)/length
  amplitudes[i] = numpy.sqrt(sum_c*sum_c + sum_s*sum_s)
  phases[i] = numpy.arctan2(sum_s,sum_c)
  print "Amplitude = %f, Phase = %f"  % (amplitudes[i],phases[i])

print "Fitting Amplitude(f) = A / sqrt(1 + (f/fc)^2) to determine fc (and less importantly A)"
### this part may not be very useful for general use
### I just happen to fall back on using my own fitting
### program
# create datafile
dh = open("lowpass.data","w")
for i in indexes :
  str = "%f %f\n" % (frequencies[i],amplitudes[i])
  dh.write(str)
dh.close()
# create fit descriptor
dh = open("lowpass.moo","w")
dh.write("function y = a / sqrt (1 + f ^ 2 / fc ^ 2)\n")
dh.write("independent f\n")
dh.write("a = 125\n")
dh.write("fc = 90\n")
dh.write("data \"lowpass.data\"\n")
dh.write("weighting equal\n")
dh.close()
# perform fit
os.system("moosefit -aF lowpass.moo")
dh = open("moosefit_save_on_exit.fit","r")
while 0 != 1 :
  line = dh.readline()
  if 0 == len(line) :
    break
  tokens = line.split()
  if len(tokens) > 2 :
    if "a" == tokens[0] : amp = float(tokens[2])
    if "fc" == tokens[0] : fc = float(tokens[2])
dh.close()
print "A = %f, fc = %f" % (amp,fc)

def lowpass_amplitude(f,fc) :
  return 1/numpy.sqrt(1+numpy.power(f/fc,2))

def lowpass_phase(f,fc) :
  return numpy.arctan(f/fc)

print "Plotting measured amplitude to compare with fit results"
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.xlabel(r'\textbf{Frequency} (Hz)')
plt.ylabel(r'\textbf{Amplitude} (V)')
plt.loglog(frequencies,amplitudes,"x")
plt.loglog(frequencies,amp*lowpass_amplitude(frequencies,fc),"-")
plt.show()

print "Plotting measured phase to compare with fit results"
plt.xlabel(r'\textbf{Frequency} (Hz)')
plt.ylabel(r'\textbf{Phase} (radians)')
plt.semilogx(frequencies,phases,"x")
plt.semilogx(frequencies,lowpass_phase(frequencies,fc),"-")
plt.show()

print "Generating an arbitrary wave, raw, to demo amplitude phase correction"
# sketch Mount Royal
raw = numpy.zeros(length)
quanta = int(numpy.floor(length/9))
for i in range(0,length) :
  if i < quanta : raw[i] = 0
  elif i < 3*quanta : raw[i] = i-quanta
  elif i < 4*quanta : raw[i] = 5*quanta-i
  elif i < 6*quanta : raw[i] = i-3*quanta
  else : raw[i] = 9*quanta-i

print "Calculating amplitudes and phases of frequency components in wave, raw"
f_fund =  f_sample / length
fft = numpy.fft.rfft(raw)
amplitudes = numpy.sqrt(fft.real**2+fft.imag**2)*2/length
phases = numpy.arctan2(fft.imag,fft.real)

print "Constructing a wave, synth, which when sent through lowpass filter will resemble raw"
angle = numpy.fromiter(range(0,length),int)*2*numpy.pi/length
synth = numpy.zeros(length)
for i in range(1,length/2) :
  synth = synth + amplitudes[i]*numpy.cos(i*angle+phases[i]-lowpass_phase(f_fund*i,fc))/lowpass_amplitude(f_fund*i,fc)

# normalize wave to bounds of PCM
synth = synth - synth.min()
synth = synth * 255 / synth.max()

print "calling a.analogWriteVector(10,synth.astype(int))"
a.analogWriteVector(10,synth.astype(int))

print "Plot raw, which should be what appears on oscilloscope, and synth which is what is sent"
plt.plot(raw)
plt.plot(synth)
plt.show()
