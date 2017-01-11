# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:42:58 2017

@author: joseph.decunha
"""

import numpy 
import matplotlib.pyplot as plt 

# Import data
gameData = numpy.loadtxt('histogramdata.txt')


def mean(trials): 
    tot = 0
    for i in range(len(trials)):
        tot += ((i)*trials[i])
    return (float)(tot/(len(trials)))
    
def variance(trials, mean): 
    varSum = 0
    for i in range(len(trials)): 
        varSum += (trials[i]-mean)**2
    return (float)(varSum/(len(trials)-1))
        
    
gameMeanData = [mean(gameData[i]) for i in range(10)]
gameVarianceData = [variance(gameData[i],gameMeanData[i]) for i in range(10)]

# Transpose data to put the columns into rows (for ease of use)
gameDataTransposed = numpy.transpose(gameData)
# Mean values of each column in the original dataset
columnMeanData = [mean(gameDataTransposed[i]) for i in range(25)]
# Variances of each column in the original dataset 
columnVarData = [variance(gameDataTransposed[i],columnMeanData[i]) for i in range(25)] 
# Standard error: take variance and mean for each column (calculated above)
columnStdErr = [(float)(numpy.sqrt(variance(gameDataTransposed[i],columnMeanData[i]))/numpy.sqrt(25)) for i in range(25)]

# x values for plot 
guessNumber = []
# y values for plot 
guessMeanFreq = []
# error values 
guessStdErr = []

# only take the non-zero columns to add into the plot
for i in range(25):
    if(columnMeanData[i]!=0):
        guessNumber.append(i+1)
        guessMeanFreq.append(columnMeanData[i])
        guessStdErr.append(columnStdErr[i])

# generating the plot 
plt.plot(guessNumber,guessMeanFreq,'o')
plt.figure(figsize=(8,8), dpi=100)
plt.errorbar(guessNumber, guessMeanFreq,yerr=guessStdErr,fmt='o')
plt.xlabel("Number of guesses",fontsize=16)
plt.ylabel("Frequency",fontsize=16)
plt.xlim(15,26)
