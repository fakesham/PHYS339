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
            if(variance[j]==0):
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
residuals = numpy.transpose(numpy.subtract(poisson1,totalBinCounts))
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Total events per interval",fontsize=12)
plt.ylabel("Residual value \n(predicted frequency - observed frequency)",fontsize=12)
plt.plot(xvals, residuals,'o')
plt.legend(fontsize=8)
exec("plt.savefig('Poissonresiduals_%s.png',dpi=150)"%int(overallMean))

# Residuals - Gaussian 
residuals = numpy.transpose(numpy.subtract(gaussian1,totalBinCounts))
plt.figure(figsize=(8,6), dpi=150)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel("Total events per interval",fontsize=12)
plt.ylabel("Residual value \n(predicted frequency - observed frequency)",fontsize=12)
plt.plot(xvals, residuals,'o')
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
plt.plot(x,y,color='red')
plt.savefig('chisq_1024.png')

#################################### UNUSED CODE ####################################
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


observedBinCounts = numpy.empty(len(gDataTransposed))
for i in range(len(gDataTransposed)):
    observedBinCounts[i] = numpy.sum(gDataTransposed[i])

 # twice the number of intervals per replica.

    
compressed1 = compress(gData)  

gData_64 = compress(gData)
gData_32 = compress(gData_64)
gData_16 = compress(gData_32)
gData_8 = compress(gData_16)
gData_4 = compress(gData_8)
gData_2 = compress(gData_4)
gData_1 = compress(gData_2)



# 128 trials
cv = colVar

poisson128 = findPoisson(gData)
csp128 = chiSquare(gData,poisson128,cv) 
gaussian128 = findGaussian(gData)
csg128 = chiSquare(gData,gaussian128,cv)


# 64 trials 
cv = cVar(gData_64, colMean)

poisson64 = findPoisson(gData_64)
csp64 = chiSquare(gData_64,poisson64,cv) 
gaussian64 = findGaussian(gData_64)
csg64 = chiSquare(gData_64,gaussian64,cv)


# 32 trials 
cv = cVar(gData_32, colMean)

poisson32 = findPoisson(gData_32)
csp32 = chiSquare(gData_32,poisson32,cv) 
gaussian32 = findGaussian(gData_32)
csg32 = chiSquare(gData_32,gaussian32,cv)


# 16 trials 
cv = cVar(gData_16, colMean)

poisson16 = findPoisson(gData_16)
csp16 = chiSquare(gData_16,poisson16,cv) 
gaussian16 = findGaussian(gData_16)
csg16 = chiSquare(gData_16,gaussian16,cv)


# 8 trials 
cv = cVar(gData_8, colMean)

poisson8 = findPoisson(gData_8)
csp8 = chiSquare(gData_8,poisson8,cv) 
gaussian8 = findGaussian(gData_8)
csg8 = chiSquare(gData_8,gaussian8,cv)


# 4 trials 
cv = cVar(gData_4, colMean)

poisson4 = findPoisson(gData_4)
csp4 = chiSquare(gData_4,poisson4,cv) 
gaussian4 = findGaussian(gData_4)
csg4 = chiSquare(gData_4,gaussian4,cv) 


# 2 trials 
cv = cVar(gData_2, colMean)

poisson2 = findPoisson(gData_2)
csp2 = chiSquare(gData_2,poisson2,cv) 
gaussian2 = findGaussian(gData_2)
csg2 = chiSquare(gData_2,gaussian2,cv)


# 1 trial
cv = cVar(gData_1, colMean)

poisson1 = findPoisson(gData_1)
csp1 = chiSquare(gData_1,poisson1,cv) 
gaussian1 = findGaussian(gData_1)
csg1 = chiSquare(gData_1,gaussian1,cv)



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


p128 = gt(poissonChiSq,csp128)
p64 = gt(poissonChiSq,csp64) 
p32 = gt(poissonChiSq,csp32) 
p16 = gt(poissonChiSq,csp16) 
p8 = gt(poissonChiSq,csp8) 
p4 = gt(poissonChiSq,csp4) 
p2 = gt(poissonChiSq,csp2) 
p1 = gt(poissonChiSq,csp1)


print("Poisson distribution for 21 degrees of freedom: \n12.5% of values must be greater than %f\n"%(poissonChiSq))
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

"""