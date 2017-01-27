import numpy 
import matplotlib.pyplot as plt 
import scipy.stats
#%matplotlib inline

# 2D array 
# 128 rows 
# 22 columns 

#################################### ROW FUNCTIONS ####################################
  
def mean(trial):
    tot = 0
    numDataPoints = 0
    for i in range(len(trial)):
        #weighted
        tot+=((i)*trial[i])
        numDataPoints+=trial[i]
    tot = float(tot)
    numDataPoints = float(numDataPoints)
    return float(numpy.divide(tot,numDataPoints))

# Input: trial, a 1D array of histogram data; 
#        mean, mean of the values in the array 
# Output: variance, variance of the array data
def variance(trial, mean):
	varSum = 0
	for j in range(len(trial)):
		# must be weighted 
		# adding 1 to index to avoid OBO
		varSum += (trial[j])*(j-mean)**2
	return float(numpy.divide(varSum,(numpy.sum(trial))))

# Input: trial, a 1D array of histogram data;
#        var, the variance value for the data
# Output: stdErr, standard error of the array data
def stdErr(trial,var):
    N = 0
    for i in range(len(trial)):
        N+=trial[i]
    return numpy.sqrt(var/N)
              


#################################### COLUMN FUNCTIONS ####################################

# Input: trials, a 2D array of histogram data 
# Output: 1D array containing the mean of each row. 
def cMean(trials):
    return [float(sum(trials[i]))/float(len(trials[i])) for i in range(len(trials))]

# Input: trials, a 2D array of histogram data; 
#        means, a 1D array of the means of each row in trials
# Output: 1D array containing the variance of each row in trials. 
def cVar(trials,means):
    return [float(sum((trials[i] - means[i])**2))/float(len(trials[i])) for i in range(len(trials))]
  
# Input: trials, a 2D array of histogram data; 
#        variances, a 1D array of the variances of each row in trials
# Output: a 1D array containing the standard error of each row in trials.   
def cStdErr(trials,variances):
    return [numpy.sqrt(numpy.divide(variances[i],len(trials[i]))) for i in range(len(trials))]



#################################### STATS FUNCTIONS ####################################

# Input: a 2D array of trials, where each separate trial is a row
# Output: a 2D array of the expected values for each trial and bin, 
#         based on the Poisson distribution. 
def findPoisson(trials):
    poisson = numpy.empty((len(trials),len(trials[0])))
    
    for j in range(len(trials)):
        for i in range(len(trials[j])):
            poisson[j][i] = numpy.sum(trials[j])*scipy.stats.poisson.pmf(i,mean(trials[j]))
    return poisson

# Input: a 2D array of trials, where each separate trial is a row
# Output: a 2D array of the expected values for each trial and bin, 
#         based on the Gaussian distribution.           
def findGaussian(trials):
    gaussian = numpy.empty((len(trials),len(trials[0])))

    for j in range(len(trials)):
        for i in range(len(trials[j])):
            gaussian[j][i] = numpy.sum(trials[j])*scipy.stats.norm.pdf(i,mean(trials[j]),numpy.sqrt(variance(trials[j],mean(trials[j]))))

    return gaussian 
  
  
# Input: observed, a 2D array of observed data;
#        expected, a 2D array of expected values based on a PDF or PMF
#        variance, a 1D array of the variance in each bin calculated globally 
# Output: a 1D array of the chi-square values for each row (trial).
def chiSquare(observed,expected,variance):
    chisq = numpy.empty(len(observed))
    
    for i in range(len(observed)): 
        chisqTot = 0 
        for j in range(len(observed[i])):
            chisqTot+=(observed[i][j]-expected[i][j])**2/variance[j]
        chisq[i] = chisqTot
    
    return chisq


# Input: data, a 2D array of observed data 
# Output: a 2D array of observed data, with half the number of trials 
def compress(data):
    # just compress every two rows
    topHalf = numpy.empty((len(data)/2,len(data[0])))
    bottomHalf = numpy.empty((len(data)/2,len(data[0])))
    for i in range(len(data)/2):
        topHalf[i]=data[i]
    for i in range(0,len(data)/2):
        bottomHalf[i]=data[i+len(data)/2]
    return numpy.add(topHalf,bottomHalf) 

# Input: expChiSq, an expected chi square value 
#        calcChiSq, a 1D array of calculated chi square values 
# Output: the percentage of values in the 1D array greater than the expected chi square. 
def gt(expChiSq,calcChiSq):
    numGreater = 0; 
    for i in range(len(calcChiSq)):
        if(calcChiSq[i]>expChiSq):
            numGreater+=1
            
    return 100*numpy.divide(float(numGreater),float(len(calcChiSq)))
 

#################################### SAMPLE DATA ####################################

# Load sample data 
s = sample
# Row calculations
sampleMean = [mean(s[i]) for i in range(len(s))]
sampleVar = [variance(s[i],sampleMean[i]) for i in range(len(s))]
# Transpose for ease of use in column calculations
sTranspose = numpy.transpose(s)
# Column calculations 
sampleColMean = cMean(sTranspose)
sampleColVar = cVar(sTranspose,sampleColMean)



#################################### EXPERIMENTAL DATA ####################################

# Load data from run of choice
gData = run7

# Row calculations 
meanReplica = [mean(gData[i]) for i in range(len(gData))]
replicaVarData = [variance(gData[i],meanReplica[i]) for i in range(len(gData))]
replicaStdErr = [stdErr(gData[i],replicaVarData[i]) for i in range(len(gData))]

# Transpose for ease of use in column calculations 
geigerDataTransposed = numpy.transpose(gData)

# Column calculations
colMean = cMean(geigerDataTransposed)
colVar = cVar(geigerDataTransposed,colMean)
colStdErr = cStdErr(geigerDataTransposed,colVar)



#################################### STATS ANALYSIS ####################################

replicaPoissonDist = numpy.empty(len(gData))
replicaGaussianDist = numpy.empty(len(gData))

# overall mean of all collected data 
overallMean = numpy.sum(meanReplica)/len(meanReplica)

# Compressed data sets 
gData_64 = compress(gData)
gData_32 = compress(gData_64)
gData_16 = compress(gData_32)
gData_8 = compress(gData_16)
gData_4 = compress(gData_8)
gData_2 = compress(gData_4)
gData_1 = compress(gData_2)

# All distributions and chi-squared values for each compressed data set 

cv = colVar

# 128 trials
poisson128 = findPoisson(gData)
csp128 = chiSquare(gData,poisson128,cv) 
gaussian128 = findGaussian(gData)
csg128 = chiSquare(gData,gaussian128,cv)

cv = cVar(gData_64, colMean)

# 64 trials 
poisson64 = findPoisson(gData_64)
csp64 = chiSquare(gData_64,poisson64,cv) 
gaussian64 = findGaussian(gData_64)
csg64 = chiSquare(gData_64,gaussian64,cv)

cv = cVar(gData_32, colMean)

# 32 trials 
poisson32 = findPoisson(gData_32)
csp32 = chiSquare(gData_32,poisson32,cv) 
gaussian32 = findGaussian(gData_32)
csg32 = chiSquare(gData_32,gaussian32,cv)

cv = cVar(gData_16, colMean)

# 16 trials 
poisson16 = findPoisson(gData_16)
csp16 = chiSquare(gData_16,poisson16,cv) 
gaussian16 = findGaussian(gData_16)
csg16 = chiSquare(gData_16,gaussian16,cv)

cv = cVar(gData_8, colMean)

# 8 trials 
poisson8 = findPoisson(gData_8)
csp8 = chiSquare(gData_8,poisson8,cv) 
gaussian8 = findGaussian(gData_8)
csg8 = chiSquare(gData_8,gaussian8,cv)

cVar(gData_4, colMean)

# 4 trials 
poisson4 = findPoisson(gData_4)
csp4 = chiSquare(gData_4,poisson4,cv) 
gaussian4 = findGaussian(gData_4)
csg4 = chiSquare(gData_4,gaussian4,cv) 

cVar(gData_2, colMean)

# 2 trials 
poisson2 = findPoisson(gData_2)
csp2 = chiSquare(gData_2,poisson2,cv) 
gaussian2 = findGaussian(gData_2)
csg2 = chiSquare(gData_2,gaussian2,cv)

cVar(gData_1, colMean)

# 1 trial
poisson1 = findPoisson(gData_1)
csp1 = chiSquare(gData_1,poisson1,cv) 
gaussian1 = findGaussian(gData_1)
csg1 = chiSquare(gData_1,gaussian1,cv)


# expected chi-square 
poissonChiSq = scipy.stats.chi2.isf(0.125,21)
gaussianChiSq = scipy.stats.chi2.isf(0.125,20)


for i in range(numpy.log2(len(gData))):

# gt -> greater than 
p128 = gt(poissonChiSq,csp128)
p64 = gt(poissonChiSq,csp64) 
p32 = gt(poissonChiSq,csp32) 
p16 = gt(poissonChiSq,csp16) 
p8 = gt(poissonChiSq,csp8) 
p4 = gt(poissonChiSq,csp4) 
p2 = gt(poissonChiSq,csp2) 
p1 = gt(poissonChiSq,csp1)


print("Poisson distribution for 21 degrees of freedom: \n12.5 percent of values must be greater than %f\n"%(poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(128,64, p128, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(64,128, p64, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(32,256, p32, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(16,512, p16, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(8,1024, p8, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(4,2048, p4, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(2,4096, p2, poissonChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(1,8192, p1, poissonChiSq))


print("\n\n")

g1 = gt(gaussianChiSq, csg1)
g2 = gt(gaussianChiSq, csg2)
g4 = gt(gaussianChiSq, csg4)
g8 = gt(gaussianChiSq, csg8)
g16 = gt(gaussianChiSq, csg16)
g32 = gt(gaussianChiSq, csg32)
g64 = gt(gaussianChiSq, csg64)
g128 = gt(gaussianChiSq, csg128)

print("Gaussian distribution for 20 degrees of freedom: \n12.5 percent of values must be greater than %f\n"%(gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(128,64, g128, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(64,128, g64, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(32,256, g32, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(16,512, g16, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(8,1024, g8, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(4,2048, g4, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(2,4096, g2, gaussianChiSq))
print("%d replicas with %d intervals each: %f percent of values greater than %f"%(1,8192, g1, gaussianChiSq))

### PLOTS ### 
totalBinCounts = [sum(geigerDataTransposed[i]) for i in range(len(geigerDataTransposed))] 
x = plt.hist(totalBinCounts,bins=22)

"""
# g-chisquare and p-chisquare: difference between actual bin result and predicted Gaussian/Poisson bin result 
# calculate for each bin (22 bins)
# 128 x 22
def chiSquare (data,var,pdf):
	tot = 0
	for i in range (len(data)):
     # ignore if variance is zero 
		if var(i) != 0:
			tot = tot + float(((data(i)-pdf(i))**2)/var(i))
         return tot
# we get 128/2 lists of 22 chisquares
# what is the error on each bin ? difficult!!!
g-chiSquare = [chiSquare(compressed1, replicaVarData, replicaGaussianDist) for i in range(compressed1)] 
p-chiSquare = [chiSquare(compressed2, replicaVarData, replicaPoissonDist) for i in range(compressed1)]

"""
"""
observedBinCounts = numpy.empty(len(geigerDataTransposed))
for i in range(len(geigerDataTransposed)):
    observedBinCounts[i] = numpy.sum(geigerDataTransposed[i])

 # twice the number of intervals per replica.

    
compressed1 = compress(gData)  




# we must see that the result is noisy must either increase the number of intervals more than 64 or add replicas together
#we just repeat the collapse of the data set again compressed2 = compress(compressed1) 
# we do it consecutively and compare distributions 
# finally we take chisquare by meanCol,colVar if u want to get only one overall chi square for each bin so a list of 22 elements 
#g-chiSquare = [chiSquare(meanCol, varCol, replicaGaussianDist) for i in range(meanCol)] 
#p-chiSquare = [chiSquare(meanCol, varCol, replicaPoissonDist) for i in range(meanCol)]
# the variance is not it !

                
xvals = numpy.linspace(0,21,num=22)
plt.plot(xvals,replicaPoissonDist,'+')
plt.plot(xvals,observedBinCounts,'o')
#calculated values
#plt.plot(xvals,replicaGaussianDist,'o')
"""
