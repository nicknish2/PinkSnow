import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import copy

''' To create a new climatology file at the start of a winter (i.e. Sept 1), download a new file for all previous years and run this script.'''

### Functions for reading in data ###

def CheckLeap(Year):  
  # Checking if the given year is leap year  
    if((Year % 400 == 0) or  
     (Year % 100 != 0) and  
     (Year % 4 == 0)):   
        return True  
  # Else it is not a leap year  
    else:  
        return False
    
# Python3 implementation of the approach
days = [31, 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31];
 
# Function to return the day number
# of the year for the given date
def dayOfYear(date):
     
    # Extract the year, month and the
    # day from the date string
    year = (int)(date[0:4]);
    month = (int)(date[5:7]);
    day = (int)(date[8:]);
 
    # If current year is a leap year and the date
    # given is after the 28th of February then
    # it must include the 29th February
    if (month > 2 and year % 4 == 0 and
       (year % 100 != 0 or year % 400 == 0)):
        day += 1;
 
    # Add the days in the previous months
    month -= 1;
    while (month > 0):
        day = day + days[month - 1];
        month -= 1;
    return day;

# Find the indices in the data corresponding to each year (2021-lastYearInClimData)
    # we want to track winter seasons, thus the year will be defined from Sept to Sept
    
def findYearIndices(startYear,endYear,dates):
    # Start and end year correspond to the year in the spring of the winter
    # The first data point is in Jan 2021, so the start year is 2021
    # ex. a start of year of 2001 would start with the winter season of 2000-2001
    # inclusive of endYear
    
    yearRange = np.arange(startYear,endYear+1)
    
    yearIndices = []
    for y in yearRange:
        currYearIndices = []
        for di in range(len(dates)):
            cond1 = float(dates[di][0:4]) == y and int(dates[di][5:7])<9
            cond2 = float(dates[di][0:4]) == y-1 and int(dates[di][5:7])>=9
            if cond1 or cond2:
                currYearIndices = currYearIndices + [di]
        yearIndices = yearIndices + [currYearIndices]
    return yearIndices

##################################################################

### Get station data ###
stationName = 'mountWashington'
# Change the path for different stations
dataPath = '{}/{}_rawData.csv'.format(stationName,stationName) # inches

### Read in the data ###
data = pd.read_csv(dataPath)

# first winter in the data
firstWinterYear = int(data.DATE.to_numpy()[0][:4])
if float(data.DATE.to_numpy()[0][5:7])>=9: # because winters are defined by the year of Jan
    firstWinterYear = firstWinterYear + 1
# last winter in the data
lastWinterYear = 2024


dates = data.DATE.to_numpy()
snowDepth = data.SNWD.to_numpy()

indicesByYear = findYearIndices(firstWinterYear,lastWinterYear,dates)

### Select the snow depth in each year ###
snowDepthByYears = []
datesByWinter = []

for iyear in indicesByYear:
    snowDepthInYear = snowDepth[iyear]
    snowDepthByYears = snowDepthByYears + [snowDepthInYear]
    
    datesByWinter = datesByWinter + [dates[iyear]]
    
    
### Turn calendar date into day of year (with Sept 1 = day 1) ###
for iy in range(len(datesByWinter)):
    for iday in range(len(datesByWinter[iy])):
        datesByWinter[iy][iday] = dayOfYear(datesByWinter[iy][iday])+122

        if datesByWinter[iy][iday]>365 and datesByWinter[iy][iday] != datesByWinter[iy][-1]:
            datesByWinter[iy][iday] = datesByWinter[iy][iday]-365
            
### Fill in the missing days in each year with NAN ###

# We have seasons ending in year firstWinterYear-lastWinterYear
stationSnowpackClim = np.empty((len(range(firstWinterYear,lastWinterYear+1)),365))

for yi in range(len(range(firstWinterYear,lastWinterYear+1))):
    year = firstWinterYear+yi
    datesByWinterInThatYear = datesByWinter[yi]
    snowByWinterInThatYear = snowDepthByYears[yi]
    if CheckLeap(year):
        endDay = 366
        snowByWinterInThatYearNew = np.empty(endDay)
    else:
        endDay = 365
        snowByWinterInThatYearNew = np.empty(endDay)
        
    for iday in range(endDay):
        if iday+1 in datesByWinterInThatYear:
            # find the index of that day
            specDayIndex = np.nonzero(datesByWinterInThatYear==iday+1)[0][0]
            snowByWinterInThatYearNew[iday] = snowByWinterInThatYear[specDayIndex]
        else:
            snowByWinterInThatYearNew[iday] = np.nan
    
    if len(snowByWinterInThatYearNew) == 366:
        snowByWinterInThatYearNew = snowByWinterInThatYearNew[:-1] # cut off leap days
    
    stationSnowpackClim[yi,:] = snowByWinterInThatYearNew


### Save the data ###

np.save('{}/{}SnowpackByYear_snowDepth.npy'.format(stationName,stationName),stationSnowpackClim)
np.save('{}/{}SnowpackByYear_endWinterYears.npy'.format(stationName,stationName),np.arange(firstWinterYear,lastWinterYear+1))