import numpy 
import matplotlib.pyplot as plt 
%matplotlib inline

# 2D array 
# 128 rows 
# 25 columns 

#########ROW ANALYSIS##########

# Input: trial, a 1D array of histogram data 
# Output: mean, mean of the array data
def mean(trial):
	tot = 0 
	numDataPoints = 0
	for i in range(len(trial)): 
		# weighted
		# adding 1 to index to avoid OBO
		tot+=((i)*trial[i])
		numDataPoints+=trial[i]
	return (float)(tot/numDataPoints)

# Input: trial, a 1D array of histogram data; 
#		 mean, mean of the values in the array 
# Output: variance, variance of the array data
def variance(trial, mean):
	varSum = 0
	for j in range(len(trial)):
		# must be weighted 
		# adding 1 to index to avoid OBO
		varSum += (trial[j])*(j-mean)**2
	return (float)(varSum/(len(trial)-1))

# Load data
geigerData = numpy.loadtxt('histogram.txt')
geigerDataTransposed = numpy.transpose(geigerData)

meanReplica = [mean(geigerData[i]) for i in range(len(geigerData))]
varData = [variance(geigerData[i],meanReplica[i]) for i in range(len(geigerData))]
rowStdErr = [(float)(numpy.sqrt(variance(geigerData[i],meanReplica[i]))/numpy.sqrt(len(geigerData))) for i in range(len(geigerData))]

############Column Analysis##############
# Transpose data to put the columns into rows (for ease of use)
geigerDataTransposed = numpy.transpose(gigerData)
# Mean values of each column in the original dataset
meanCol = [sum(geigerDataTransposed[i])/(len(geigerDataTransposed)) for i in range(len(geigerDataTransposed))]
# Variances of each column in the original dataset 
varCol = [(sum(geigerDataTransposed[i]-meanCol[i])**2)/(len(geigerDataTransposed)) for i in range(geigerDataTransposed)] 
# Standard error: take variance and mean for each column (calculated above)
colStdErr = [(float)(numpy.sqrt(varCol[i])/numpy.sqrt(len(geigerDataTransposed))) for i in range(geigerDataTransposed)]

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
