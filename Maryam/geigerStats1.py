import numpy 
import matplotlib.pyplot as plt 
import scipy.stats
#%matplotlib inline

# 2D array 
# 128 rows 
# 22 columns 

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
#the mean and variance should not be weighted!

# Input: trials, a 2D array of histogram data 
# Output: 1D array containing the mean of each row. 
def colMean(trials):
    return [float(sum(trials[i]))/float(len(trials[i])) for i in range(len(trials))]

# Input: trials, a 2D array of histogram data; 
#        means, a 1D array of the means of each row in trials
# Output: 1D array containing the variance of each row in trials. 
def colVar(trials,means):
    return [float((sum(trials[i] - means[i])**2)/(len(trials))) for i in range(len(trials))]
  
# Input: trials, a 2D array of histogram data; 
#        variances, a 1D array of the variances of each row in trials
# Output: a 1D array containing the standard error of each row in trials.   
def colStdErr(trials,variances):
    return [numpy.sqrt(numpy.divide(variances[i],len(trials[i]))) for i in range(len(trials))]
        

colMean = colMean(geigerDataTransposed)
colVar = colVar(geigerDataTransposed,colMean)
colStdErr = colStdErr(geigerDataTransposed,colVar)


# i think it must be geigerData7 because we need the distribution for all 128 replicas 
replicaPoissonDist = numpy.empty(len(geigerData7))
replicaGaussianDist = numpy.empty(len(geigerData7))
"""
# overall mean of all collected data 
overallMean = numpy.sum(meanReplica)/len(meanReplica)

####parameters of the distributions are calculated from each replica#####
### we must get 128 distributions####
# do we have to also exclude the ones with variance 0?#
for i in range(len(geigerData7)):
    #the probability of getting i counts in a time interval 
    replicaPoissonDist = numpy.sum(geigerData7[i])*scipy.stats.poisson.pmf(i,meanReplica[i])
    replicaGaussianDist = numpy.sum(geigerData7[i])*scipy.stats.norm.pdf(i,numpy.sqrt(replicaVarData[i]),numpy.sqrt(replicaVarData[i]))
    #  multiply it by the number of points in your data set (64) because the functions are normalized to unit area.
    # gaussian with a small mean requires a different normalization scipy.stats.norm.sf(b,meanReplica,numpy.sqrt(replicaVarData))
 
observedBinCounts = numpy.empty(len(geigerDataTransposed))
for i in range(len(geigerDataTransposed)):
    observedBinCounts[i] = numpy.sum(geigerDataTransposed[i])

 # twice the number of intervals per replica.
def compress(data):
    # just compress every two rows
    toReturn = numpy.zeros((len(data)/2,len(data[0])))
    for i in range(len(data)/2):
        toReturn[i] = numpy.add(data[i],data[i+1])
        i+=2
    return toReturn 
    
compressed1 = compress(geigerData7)  

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
