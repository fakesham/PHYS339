import numpy 
import matplotlib.pyplot as plt 
import scipy.stats
#%matplotlib inline

# 2D array 
# 128 rows 
# 25 columns 

#########ROW ANALYSIS##########
  
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
	return float(numpy.divide(varSum,(len(trial)-1)))

# Input: trial, a 1D array of histogram data;
#        var, the variance value for the data
# Output: stdErr, standard error of the array data
def stdErr(trial,var):
    N = 0
    for i in range(len(trial)):
        N+=trial[i]
    return numpy.sqrt(var/N)
        
        
# Load data from run with average of 7
geigerData7 = run7

# Each bin is in a separate row 
geigerDataTransposed = numpy.transpose(geigerData7)

meanReplica = [mean(geigerData7[i]) for i in range(len(geigerData7))]
replicaVarData = [variance(geigerData7[i],meanReplica[i]) for i in range(len(geigerData7))]
replicaStdErr = [stdErr(geigerData7[i],replicaVarData[i]) for i in range(len(geigerData7))]

############Column Analysis##############
# Transpose data to put the columns into rows (for ease of use)
geigerDataTransposed = numpy.transpose(geigerData7)
# Mean values of each column in the original dataset
meanCol = [mean(geigerDataTransposed[i]) for i in range(len(geigerDataTransposed))]
colVar = [variance(geigerDataTransposed[i],meanCol[i]) for i in range(len(geigerDataTransposed))]
colStdErr = [stdErr(geigerDataTransposed[i],colVar[i]) for i in range(len(geigerDataTransposed))]

replicaPoissonDist = numpy.empty(len(geigerDataTransposed))
replicaGaussianDist = numpy.empty(len(geigerDataTransposed))

# overall mean of all collected data 
overallMean = numpy.sum(meanReplica)/len(meanReplica)

for i in range(len(geigerDataTransposed)):
    replicaPoissonDist[i] = 6.4*numpy.sum(geigerDataTransposed[i])*scipy.stats.poisson.pmf(i,overallMean)
    # probability of getting 7 counts, with given mean (this works!)
    replicaGaussianDist[i] = numpy.sum(geigerDataTransposed[i])*scipy.stats.norm.pdf(i,numpy.sqrt(colVar[i]),numpy.sqrt(colVar[i]))
    # Gaussian looks ugly 
 
# chi-p: difference between actual bin result and predicted Poisson bin result 
# calculate for each bin (22 bins)

observedBinCounts = numpy.empty(len(geigerDataTransposed))
for i in range(len(geigerDataTransposed)):
    observedBinCounts[i] = numpy.sum(geigerDataTransposed[i])

   
def compress(data):
    # just compress every two rows
    toReturn = numpy.zeros((len(data)/2,len(data[0])))
    for i in range(len(data)/2):
        toReturn[i] = numpy.add(data[i],data[i+1])
        i+=2
    return toReturn 
    
compressed = compress(geigerData7)  

for i in range(numpy.log2(len(geigerData7))):
    # calculate/store chi square
    # calculate/store poisson, Gaussian
    # 
  

xvals = numpy.linspace(0,21,num=22)
plt.plot(xvals,replicaPoissonDist,'+')
plt.plot(xvals,observedBinCounts,'o')
#calculated values
#plt.plot(xvals,replicaGaussianDist,'o')

