import serial
import numpy
import matplotlib.pyplot as p
import math
import pylab



class arduino :
  def __init__(self,debug=0) :
    self.handle = 0
    self.debug = debug
    self.pages = -1;
    for index in range(0,9) :
      self.path = "/dev/ttyACM%d" % index
      if self.debug != 0 : print "trying %s" % self.path
      try :
        self.handle = serial.Serial(port=self.path, baudrate=115200)
        print "Found Arduino at %s" % self.path
        break
      except :
        pass
    if 0 == self.handle :
      raise "Can't open device"
    self.handle.setDTR(0) # this resets the Arduino
    self.handle.setDTR(1)
    fails = 0
    while 0 == self.get_signature() :
      fails = fails + 1
      if fails > 5 : raise "Failed to read signature, is correct sketch loaded on Arduino?"
  def dumpbuffer(self,verb,buf) :
    dbgstr = "%s %d bytes :" % (verb,len(buf))
    for i in range(0,len(buf)) :
      if i > 0 : dbgstr = dbgstr + ","
      ch = buf[i]
      dbgstr = dbgstr + "0x%02x" % ord(ch)
      if ((ch >= 'A') and (ch <= 'Z')) or ((ch >= 'a') and (ch <= 'z')) or ((ch >= '0') and (ch <= '9')) :
        dbgstr = dbgstr + "(%c)" % ch
    return dbgstr
  def read(self,length,timeout=None,acceptFail=0) :
    self.handle.timeout = timeout
    data = ""
    while len(data) < length :
      newdata = ""
      newdata = self.handle.read(length-len(data))
      if len(newdata) > 0 :
        if 0 != self.debug : print self.dumpbuffer("read",newdata)
        data = data + newdata
      else :
        if 0 != self.debug : print "read zero bytes"
        if 0 != acceptFail : return data
    return data
  def write(self,buf) :
    if 0 != self.debug : print self.dumpbuffer("write",buf)
    return self.handle.write(buf)
  def get_signature(self) :
    data = self.read(4096,timeout=2,acceptFail=1)
    self.write("\x01")
    signature = "ARDUINO"
    index = 0
    fails = 0
    while index < 7 :
      try :
        ch = self.read(1)
        if self.debug != 0 : print "Read 0x%02x" % ord(ch)
        if signature[index] == ch :
          index = index + 1
          if self.debug != 0 : print "index = %d" % index
        elif signature[0] == ch :
          index = 1
        else :
          index = 0
      except :
        fails = fails + 1
        if fails > 5 : return 0
    data = self.read(4096,timeout=1,acceptFail=1);
    if len(data) > 0 :
      if 0 != self.debug : print "read %d bytes unexpected (%s)" % (len(data),data)
      return 0
    return 1
  def get_pages(self) :
    if self.pages > 0 : return
    data = "\x02"
    self.write(data)
    data = self.read(1)
    self.pages = int(ord(data[0]))
    if 0 != self.debug : print "pages = %d" % self.pages
  def sampling_time(self, iterations=1000) :
    if iterations < 0 : raise "iterations must be non negative"
    if iterations > 0xffff : raise "iterations must be less than %d" % 0x10000
    data = "\x03%c%c" % (iterations & 0xff, (iterations >> 8) & 0xff)
    self.write(data)
    data = self.read(4)
    return 1e-6*(ord(data[0]) | (ord(data[1]) << 8) | (ord(data[2]) << 16) | (ord(data[3]) << 24))/iterations
  def out_buffer_length(self) :
    if self.pages < 0 : self.get_pages();
    return self.pages<<3;
  def in_buffer_length(self) :
    if self.pages < 0 : self.get_pages();
    return self.pages<<2;
  def analogRead(self,pin) :
    data = "\x04%c" % pin
    self.write(data)
    data = self.read(2)
    return ord(data[0])+(ord(data[1])<<8)
  def analogWrite(self,pin,value) :
    data = "\x05%c%c%c" % (pin, value & 0xff, (value >> 8) & 0xff)
    self.write(data)
    data = self.read(2)
    if value != ord(data[0])+(ord(data[1])<<8) : raise "analogWrite fails"
  def analogReadVector(self,ipin,count) :
    if count < 0 : raise "count must be non negative"
    if self.pages < 0 : self.get_pages();
    if count > (self.pages << 2) : raise "count is too high, use .in_buffer_length() to get max length (%d > %d)" % (count, self.pages << 2)
    data = "\x06%c%c%c" % (ipin, count & 0xff, (count >> 8) & 0xff)
    self.write(data)
    data = self.read(2)
    rc = ord(data[0])+(ord(data[1])<<8)
    if rc != count : raise "Returned count (%d) is not equal send count (%d)" % (rc, count)
    data = self.read(2*count)
    return_vector = numpy.zeros(count)
    for i in range(0,count) : return_vector[i] = ord(data[2*i])+(ord(data[2*i+1])<<8)
    return return_vector
  def analogWriteVector(self,pin,vector) :
    if vector.min() < 0 : raise "vector contains negative value"
    if vector.max() > 255 : raise "vector contains value greater 255"
    length = len(vector)
    if self.pages < 0 : self.get_pages();
    if length > (self.pages << 3) : raise "vector is too long, use .out_buffer_length() to get max length (%d > %d)" % (length, self.pages << 3)
    data = "\x07%c%c%c" % (pin, length & 255, (length >> 8) & 255)
    for v in vector : data += ("%c" % v)
    self.write(data)
    data = self.read(2)
    rc = ord(data[0])+(ord(data[1])<<8)
    if rc != length : raise "Returned length (%d) is not equal send length (%d)" % (rc, length)
    if 0 != self.debug : print "Successfully sent vector of length %d to pin %d" % (rc, pin)
  def analogWriteReadVector(self,opin,ipin,vector,iterations=0) :
    if iterations < 0 : raise "iterations must be non negative"
    if iterations > 0xffff : raise "iterations must be less than %d" % 0x10000
    if vector.min() < 0 : raise "vector contains negative value"
    if vector.max() > 255 : raise "vector contains value greater 255"
    length = len(vector)
    if self.pages < 0 : self.get_pages();
    if length > (self.pages << 3) : raise "vector is too long, use .out_buffer_length() to get max length (%d > %d)" % (length, self.pages << 3)
    data = "\x08%c%c%c%c%c%c" % (opin, ipin, iterations & 0xff, (iterations >> 8) & 0xff, length & 255, (length >> 8) & 255)
    for v in vector : data += ("%c" % v)
    self.write(data)
    data = self.read(2)
    rc = ord(data[0])+(ord(data[1])<<8)
    if rc != length : raise "Returned length (%d) is not equal send length (%d)" % (rc, length)
    if 0 != self.debug : print "Successfully sent vector of length %d to pin %d, waiting for pin %d data" % (rc, opin, ipin)
    data = self.read(length)
    return_vector = numpy.zeros_like(vector)
    for i in range(0,length) : return_vector[i] = ord(data[i])
    return return_vector

  def inverseLowPass(self,fs, fc, signal) :
    spectra = numpy.fft.rfft(signal)
    frequency = numpy.linspace(0,fs/2,numpy.size(spectra,axis=0))
    amp = numpy.absolute(spectra)
    phase = numpy.angle(spectra)
    gain = numpy.sqrt(1+(frequency/fc)**2)
    phaseshift = -numpy.arctan2(frequency,fc)
    amp *= gain
    phase -= phaseshift
    #return numpy.fft.irfft(amp*(numpy.cos(phase)+1j*numpy.sin(phase)))
    lastvalue = numpy.fft.irfft(amp*(numpy.cos(phase)+1j*numpy.sin(phase)))
    for i in range(2,(numpy.size(amp,axis=0)),100) :
        value = numpy.fft.irfft((frequency < frequency[i])*amp*(numpy.cos(phase)+1j*numpy.sin(phase)))
        if (value.max()) > 255  or (value.min() < 0):
            value = lastvalue
            print ("Breaking on %d,%f"%(i,frequency[i]))
            break
        else:
            lastvalue = value
    
    return value
 
  def inverseLowPassSine(self,fs, fc, signal) :
    spectra = numpy.fft.rfft(signal)
    frequency = numpy.linspace(0,fs/2,numpy.size(spectra,axis=0))
    amp = numpy.absolute(spectra)
    phase = numpy.angle(spectra)
    gain = numpy.sqrt(1+(frequency/fc)**2)
    phaseshift = -numpy.arctan2(frequency,fc)
    amp *= gain
    phase -= phaseshift
    return numpy.fft.irfft(amp*(numpy.cos(phase)+1j*numpy.sin(phase)))

  def generate_sine(self,frequency,amplitude) :
    ts = self.sampling_time()
    amp = ((amplitude*255)/5)
    output_length = int(1/(frequency*ts)) 
    
    i = numpy.array(range(output_length))
    x = numpy.array((((numpy.sin(2*numpy.pi*i/len(i)))*amp)+127),dtype=int)
    
    xiterations = int(50000/output_length)
    xconcact = numpy.hstack((x,x))
    for m in range(0,(xiterations-1)) :
        xconcact = numpy.hstack((xconcact,x))
        m = m + 1
    
    xcorrected = a.inverseLowPassSine(frequency*4, 73, xconcact)    
    
    xcorrected = numpy.rint(xcorrected)
    xcorrected = numpy.array(xcorrected,dtype=int)
    
    xoutput = xcorrected[0:output_length]
    
    p.figure(figsize=(8,6), dpi=90)
    p.plot(i,x)
    p.plot(i,xoutput)  
    a.analogWriteVector(10,xoutput)
    return xoutput    
    
    
  def generate_sawtooth(self,frequency,amplitude) :
    ts = self.sampling_time()
    amp = ((amplitude*255)/5)
    output_length = int(1/(frequency*ts))
    #output_length = 1000
    
    i = numpy.array(range(output_length))
    x = numpy.array(((((i+1)*amp)/len(i))+127),dtype=int)  
    
    #I want to create an iterator that will concatenate an array of 50,000 points
    xiterations = int(50000/output_length)
    xconcact = numpy.hstack((x,x))
    for m in range(0,(xiterations-1)) :
        xconcact = numpy.hstack((xconcact,x))
        m = m + 1
    
    xcorrected = a.inverseLowPass(8900, 73, xconcact)
    if xcorrected.min() < 0 :
        xcorrected = xcorrected + numpy.abs(xcorrected.min())
    if xcorrected.max() > 255 :
        numpy.clip(xcorrected,0,255,out=xcorrected)
        #scalefac = xcorrected.max()/255
        #xcorrected /= scalefac
        print "Clipping is occuring"
    
    xcorrected = numpy.rint(xcorrected)
    xcorrected = numpy.array(xcorrected,dtype=int)
    
    xoutput = xcorrected[0:output_length]
    
    p.figure(figsize=(8,6), dpi=90)
    p.plot(i,x)
    p.plot(i,xoutput)
    a.analogWriteVector(10,xoutput)
    return xoutput
    
  def calculate_sine_limitations(self) :
      f = numpy.linspace(1,400,400)
      gain1v = numpy.sqrt(1+(f/73)**2)
      gain2v = (2*numpy.sqrt(1+(f/73)**2))
      gain3v = (3*numpy.sqrt(1+(f/73)**2))
      gain4v = (4*numpy.sqrt(1+(f/73)**2))
      p.figure(figsize=(8,6), dpi=150)
      p.axhline(y=5,xmin=0,xmax=400,color="black")
      p.plot(f,gain1v,label="1v sine")
      p.plot(f,gain2v)
      p.plot(f,gain3v)
      p.plot(f,gain4v)
      p.xlabel("Frequency [hz]")
      p.ylabel("Output Voltage [V]")
      p.title("Necessary Output Voltage to accommodate for attenuation")
      p.legend(["5v","1v sine","2v sine","3v sine","4v sine",],loc="upper left")

  def generate_square(self,frequency,amplitude) :
    ts = self.sampling_time()
    amp = ((amplitude*255)/5)
    output_length = int(1/(frequency*ts))
    #output_length = 1000
    
    i = numpy.array(range(output_length))
    x = numpy.array(range(output_length))
    for b in range(0,(output_length/2)) :
        x[b] = amp+127
    for b in range((output_length/2),(output_length)) :
        x[b] = 127
    
    #I want to create an iterator that will concatenate an array of 50,000 points
    
    xiterations = int(50000/output_length)
    xconcact = numpy.hstack((x,x))
    for m in range(0,(xiterations-1)) :
        xconcact = numpy.hstack((xconcact,x))
        m = m + 1
    
    xcorrected = a.inverseLowPass(8900, 73, xconcact)
    if xcorrected.min() < 0 :
        xcorrected = xcorrected + numpy.abs(xcorrected.min())
    if xcorrected.max() > 255 :
        numpy.clip(xcorrected,0,255,out=xcorrected)
        #scalefac = xcorrected.max()/255
        #xcorrected /= scalefac
        print "Clipping is occuring"
    
    xcorrected = numpy.rint(xcorrected)
    xcorrected = numpy.array(xcorrected,dtype=int)
    
    xoutput = xcorrected[0:output_length]
    
    p.figure(figsize=(8,6), dpi=90)
    p.plot(i,x)
    p.plot(i,xoutput)
    a.analogWriteVector(10,xoutput)
    return xoutput   
    

  def generate(self,signal,amplitude, frequency) :
      if signal == "sine" or signal == "wave" or signal == "sin" :
          out = a.generate_sine(frequency,amplitude)
          
      if signal == "sawtooth" or signal == "ramp"  :
          out = a.generate_sawtooth(frequency,amplitude)
          
      if signal == "square" or signal == "pulse" or signal == "clock"  :
          out = a.generate_square(frequency,amplitude)
          
      if signal == "triangle" :
          out = a.generate_triangle(frequency,amplitude)
          
      return out
          
  def generate_triangle(self,frequency,amplitude) :
    ts = self.sampling_time()
    amp = ((amplitude*255)/5)
    output_length = int(1/(frequency*ts))
    #output_length = 1000
    
    i = numpy.array(range(output_length))
    x = numpy.array(range(output_length))
    for b in range(0,(output_length/2)) :
        x[b] = (((b*amp)/(output_length/2))+127)
    for b in range((output_length/2),(output_length)) :
        x[b] = (((2*amp)-(b*amp)/(output_length/2))+127)
    
    #I want to create an iterator that will concatenate an array of 50,000 points
    xiterations = int(50000/output_length)
    xconcact = numpy.hstack((x,x))
    for m in range(0,(xiterations-1)) :
        xconcact = numpy.hstack((xconcact,x))
        m = m + 1
    
    xcorrected = a.inverseLowPass(8900, 73, xconcact)
    if xcorrected.min() < 0 :
        xcorrected = xcorrected + numpy.abs(xcorrected.min())
    if xcorrected.max() > 255 :
        numpy.clip(xcorrected,0,255,out=xcorrected)
        #scalefac = xcorrected.max()/255
        #xcorrected /= scalefac
        print "Clipping is occuring"
    
    xcorrected = numpy.rint(xcorrected)
    xcorrected = numpy.array(xcorrected,dtype=int)
    
    xoutput = xcorrected[0:output_length]
    p.figure(figsize=(8,6), dpi=90)
    p.plot(i,x)
    p.plot(i,xoutput)
    a.analogWriteVector(10,xoutput)
    return xoutput
    

  

a = arduino()

#arduino.generate(type, amplitude, frequency)
a.generate("triangle",0.5,400)

#a.calculate_sine_limitations()
