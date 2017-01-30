import numpy 
import matplotlib.pyplot as plt 
import scipy.stats
from scipy.stats import chi2
#%matplotlib inline

# 2D array git add 
# 128 rows 
# 22 columns 

#################################### ROW FUNCTIONS ####################################
  
# Input: trial, a 1D array of histogram data
# Output: a single value, the mean of the 1D array 
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
    toReturn = numpy.empty(len(trials))
    for i in range(len(trials)):
        toReturn[i] = numpy.sqrt(numpy.divide(variances[i],sum(trials[i])))
    return toReturn



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
            gaussian[j][i] = numpy.sum(trials[j])/(scipy.stats.norm.sf(0,mean(trials[j]),numpy.sqrt(variance(trials[j],mean(trials[j])))))*scipy.stats.norm.pdf(i,mean(trials[j]),numpy.sqrt(variance(trials[j],mean(trials[j]))))

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
            if(variance[j]<0.0001):
                continue
            chisqTot+=(observed[i][j]-expected[i][j])**2/variance[j]
        chisq[i] = chisqTot
    
    return chisq


# Input: data, a 2D array of observed data 
# Output: a 2D array of observed data, with half the number of trials 
def compress(data):
    # just compress every two rows
    topHalf = numpy.empty((len(data)/2,len(data[0])))
    bottomHalf = numpy.empty((len(data)/2,len(data[0])))
    for i in range(int(len(data)/2)):
        topHalf[i]=data[i]
    for i in range(int(len(data)/2)):
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
 
"""
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
"""


#################################### EXPERIMENTAL DATA ####################################

# Load data from run of choice
gData = histogram
# Transpose for ease of use in column calculations 
gDataTransposed = numpy.transpose(gData)

# Data parameters
numIntervals = numpy.sum(gData[0])
numRuns = len(gData)
numBins = len(gDataTransposed)
totalDOF = 0
for i in range(len(gDataTransposed)):
    if(numpy.sum(gDataTransposed[i])!=0):
        totalDOF+=1

# Row calculations 
meanReplica = [mean(gData[i]) for i in range(len(gData))]
replicaVarData = [variance(gData[i],meanReplica[i]) for i in range(len(gData))]
replicaStdErr = [stdErr(gData[i],replicaVarData[i]) for i in range(len(gData))]

# Column calculations
colMean = cMean(gDataTransposed)
colVar = cVar(gDataTransposed,colMean)
colStdErr = cStdErr(gDataTransposed,colVar)



#################################### STATS ANALYSIS ####################################

replicaPoissonDist = numpy.empty(len(gData))
replicaGaussianDist = numpy.empty(len(gData))

# overall mean of all collected data 
overallMean = numpy.sum(meanReplica)/len(meanReplica)

# repetitions of each for loop below 
reps = int(numpy.log2(numRuns))+1

# Compressed data sets 
for i in range(reps-1):
    if(i==0):
        exec("gData_%s = compress(gData)"%int(numRuns/2**(i+1)))
    else: 
        exec("gData_%s = compress(gData_%s)"%(int(numRuns/2**(i+1)),int(numRuns/2**(i))))

# All distributions and chi-squared values for each compressed data set 

for i in range(reps):
    index = int(numRuns/2**i)
    if(i==0):
        exec("cv = colVar")
        exec("poisson%s = findPoisson(gData)"%index)
        exec("csp%s = chiSquare(gData,poisson%s,cv)"%(index, index))
        exec("gaussian%s = findGaussian(gData)"%index)
        exec("csg%s = chiSquare(gData,gaussian%s,cv)"%(index,index))

    else: 
        exec("cv%s = cVar(numpy.transpose(gData_%s), cMean(numpy.transpose(gData_%s)))"%(index, index, index))
        exec("poisson%s = findPoisson(gData_%s)"%(index, index))
        exec("csp%s = chiSquare(gData_%s,poisson%s,cv%s)"%(index, index, index, index))
        exec("gaussian%s = findGaussian(gData_%s)"%(index, index))
        exec("csg%s = chiSquare(gData_%s,gaussian%s,cv%s)"%(index, index, index, index))


# expected chi-square 
poissonChiSq = scipy.stats.chi2.isf(0.125,totalDOF-1)
gaussianChiSq = scipy.stats.chi2.isf(0.125,totalDOF-2)


# greater-than values for all Poisson and Gaussian 
for i in range(reps):
    exec("p%s = gt(poissonChiSq,csp%s)"%(int(numRuns/2**i),int(numRuns/2**i)))
    exec("g%s = gt(gaussianChiSq,csg%s)"%(int(numRuns/2**i),int(numRuns/2**i)))



#################################### PRINT STATEMENTS ####################################

exec("savefile = open('distChiSq%s.txt','w+')"%int(overallMean))

# Poisson 
savefile.write("Poisson distribution for %d degrees of freedom: \n"%(totalDOF-1))
savefile.write("12.5%% of values must be greater than %f\n\n"%(poissonChiSq))

for i in range(reps):
    n = int(numRuns/2**i)
    ints = int(numIntervals*2**i)
    varName = "p"+str(n)
    exec("savefile.write('%d replicas with %d intervals each: %f %%  of values greater than %f')"%(n,ints,eval(varName),poissonChiSq))
    savefile.write('\n')  

print('\n\n')
savefile.write("\n\n\n")

# Gaussian
savefile.write("Gaussian distribution for %d degrees of freedom: \n"%(totalDOF-2))
savefile.write("12.5%% of values must be greater than %f\n\n"%(gaussianChiSq))

for i in range(reps):
    n = int(numRuns/2**i)
    ints = int(numIntervals*2**i)
    varName = "g"+str(n)
    exec("savefile.write('%d replicas with %d intervals each: %f %%  of values greater than %f')"%(n,ints,eval(varName),gaussianChiSq))
    savefile.write('\n')
savefile.close()

#################################### PLOTS ####################################

# bar graph of total bin counts 
totalBinCounts = [sum(gDataTransposed[i]) for i in range(len(gDataTransposed))] 
xvals = numpy.arange(0,numBins)

# Poisson vs. Gaussian 
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Total events per interval",fontsize=12)
plt.ylabel("Frequency",fontsize=12)
plt.bar(xvals,totalBinCounts,color='lightgrey',yerr=numpy.transpose(colStdErr))
plt.plot(xvals,numpy.transpose(gaussian1),linewidth=2,label="Gaussian")
plt.plot(xvals,numpy.transpose(poisson1),linewidth=2,label="Poisson")
plt.legend(fontsize=8)
exec("plt.savefig('totalbincounts_%s.png',dpi=150,pad_inches=10)"%int(overallMean))

# Residuals - Poisson 
ye = [numpy.sqrt(totalBinCounts[i]) for i in range(len(totalBinCounts))]
residuals = numpy.transpose(numpy.subtract(poisson1,totalBinCounts))
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Total events per interval",fontsize=12)
plt.ylabel("Residual value \n(predicted frequency - observed frequency)",fontsize=12)
plt.errorbar(xvals, residuals, yerr=ye, fmt='o')
plt.plot([0,35],[0,0])
plt.legend(fontsize=8)
exec("plt.savefig('Poissonresiduals_%s.png',dpi=150)"%int(overallMean))


# Residuals - Gaussian 
ye = [numpy.sqrt(totalBinCounts[i]) for i in range(len(totalBinCounts))]
residuals = numpy.transpose(numpy.subtract(gaussian1,totalBinCounts))
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Total events per interval",fontsize=12)
plt.ylabel("Residual value \n(predicted frequency - observed frequency)",fontsize=12)
plt.errorbar(xvals, residuals, yerr=ye, fmt='o')
plt.plot([0,35],[0,0])
plt.legend(fontsize=8)
exec("plt.savefig('Gaussianresiduals__%s.png',dpi=150)"%int(overallMean))


# Variance vs. mean - Poisson
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Mean frequency of events observed",fontsize=12)
plt.ylabel("Variance of each value of observed events within interval",fontsize=12)
plt.plot(colMean, colVar,'o')
plt.legend(fontsize=8)
exec("plt.savefig('Poissonvarmean_%s.png',dpi=150)"%int(overallMean))


# Chi square - Poisson 
plt.figure(figsize=(8,6), dpi=150)
plt.hist(csp1024,bins=1024,color='lightgrey')
df = totalDOF-1
x = numpy.linspace(0,max(csp1024),num=512)
y = numpy.multiply(chi2.pdf(x,df),1024)
plt.xlabel("Chi-square value",fontsize=12)
plt.ylabel("Frequency",fontsize=12)
plt.plot(x,y,color='red',label="Chi-square distribution for %d degrees of freedom"%df)
plt.legend(fontsize=8)
plt.savefig('chisq_1024.png')

