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
    replicaPoissonDist[i] = numpy.sum(geigerDataTransposed[i])*scipy.stats.poisson.pmf(i,overallMean)
    # probability of getting 7 counts, with given mean (this works!)
    replicaGaussianDist[i] = numpy.sum(geigerDataTransposed[i])*scipy.stats.norm.pdf(i,numpy.sqrt(colVar[i]),numpy.sqrt(colVar[i]))
    # Gaussian looks ugly 
    
xvals = numpy.linspace(0,21,num=22)
plt.plot(xvals,replicaGaussianDist,'o')
#calculated values
plt.plot(xvals,)
#plt.plot(xvals,replicaGaussianDist,'o')



"""
# x values for plot 
guessNumber = []
# y values for plot 
guessMeanFreq = []
# error values 
guessStdErr = []

# only take the non-zero columns to add into the plot
for i in range(geigerDataTransposed):
    if(meanCol[i]!=0):
        guessNumber.append(i+1)
        guessMeanFreq.append(meanCol[i])
        guessStdErr.append(colStdErr[i])

# generating the plot 
plt.plot(guessNumber,guessMeanFreq,'o')
plt.figure(figsize=(8,8), dpi=100)
plt.errorbar(guessNumber, guessMeanFreq,yerr=guessStdErr,fmt='o')
plt.suptitle("Mean frequency of number of guesses",fontsize=20)
plt.xlabel("Number of guesses",fontsize=16)
plt.ylabel("Mean frequency",fontsize=16)
plt.xlim(15,26)
"""