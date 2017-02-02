def Low_Pass_Filter(fs,fc,signal):
    L = numpy.size(signal,axis=0)
    result = numpy.zeros((L,2))
    alpha = 2*numpy.pi*fc/fs
    beta = 1-alpha
    signal = numpy.copy(signal) # arrays are passed by reference
    signal[:,1] *= signal[:,1]  # square the errorbars
    result[0,:] = alpha*signal[0,:]
    for i in range(1,L):
        result[i,:] = alpha*signal[i,:]+beta*result[i-1,:]
    signal
    result[:,1] = numpy.sqrt(result[:,1])
    return result

def Low_Pass_Filter_by_FFT(fs,fc,signal):
    spectra = numpy.fft.rfft(signal)
    frequency = numpy.linspace(0,fs/2,numpy.size(spectra,axis=0))
    amp = numpy.absolute(spectra)
    phase = numpy.angle(spectra)
    gain = 1./numpy.sqrt(1+(frequency/fc)**2)
    phaseshift = -numpy.arctan2(frequency,fc)
    amp *= gain;
    phase += phaseshift
    return numpy.fft.irfft(amp*(numpy.cos(phase)+1j*numpy.sin(phase)))
