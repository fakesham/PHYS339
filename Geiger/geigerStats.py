import numpy 
import matplotlib.pyplot as plt 
%matplotlib inline

# 2D array 
# 128 rows 
# 25 columns 

# Input: trial, a 1D array of histogram data 
# Output: mean, mean of the array data
def mean(trial):
	tot = 0 
	for i in range(len(trial)): 
		# weighted
		# adding 1 to index to avoid OBO
		tot+=((i+1)*trial[i])
	return (float)(tot/len(trial))

# Input: trial, a 1D array of histogram data; 
#		 mean, mean of the values in the array 
# Output: variance, variance of the array data
def variance(trial, mean):
	varSum = 0
	for j in range(len(trial)):
		# must be weighted 
		# adding 1 to index to avoid OBO
		varSum += (j+1)*(trial[j]-mean)**2
	return (float)(varSum/(len(trial)-1))

# Load data
geigerData = numpy.loadtxt('histogram.txt')
geigerDataTransposed = numpy.transpose(geigerData)
