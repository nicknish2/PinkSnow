### Make the plot of snow depth

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import copy
import glob

# Function to return the day number
# of the year for the given date
def dayOfYear(date):
    
    days = [31, 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31];
     
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

# Function used to load current year data
def snowpackOnDate(stationName,dataPath):
    dataOnDate = pd.read_csv(dataPath, sep = "|",header=1)
    snowpack = dataOnDate[dataOnDate.Name == stationName].Amount.values[0]
    dateString = dataOnDate[dataOnDate.Name == stationName]['DateTime_Report(UTC)'].values[0][:-3]
    return snowpack,dateString


### Load Data ###

# Load data for the current year
currentSeasonSnowDepth_inCM = np.array([])
currentSeasonDates = np.array([])

stationsOfInterest = ['PINKHAM NOTCH']

dir_path = '/PinkSnow/data/*/*.txt' # path with the daily downloads of data, select the 12Z (morning EST)

for ifile,file in enumerate(glob.glob(dir_path, recursive=True)):
    currentSnowDepth,currentDateString = snowpackOnDate(stationsOfInterest[0],file)
    currentSeasonSnowDepth_inCM = np.append(currentSeasonSnowDepth,currentSnowDepth)
    currentSeasonDates = np.append(currentSeasonDates,dayOfYear(currentDateString))

# Load Historical Pinkham Notch Data
snowDepthClim_inCM = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_snowDepth_cm.npy')
datesClim = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_endWinterYears_cm.npy')


# Convert to Inches
snowDepthClim_inIN = snowDepthClim_inCM/2.54
currentSeasonSnowDepth_inIN = currentSeasonSnowDepth_inCM/2.54

# Calculate Average
averageSnowDepth_inIN = np.nanmean(snowDepthClim_inIN,axis=0)

### Make the plot ###

# Put all of these years on a plot

datesForPlotting = np.arange(1,366)

# Shading for historical plot
n = len(snowDepthClim_inIN)
colors = plt.cm.Greys(np.linspace(0,1,n))

for i in range(len(snowDepthClim_inIN)):
    plt.plot(datesForPlotting,snowDepthClim_inIN[i],c=colors[i],linewidth = .5)

# Plot the average
plt.plot(range(1,366),averageSnowDepth_inIN,label='1930-2023 Average',linewidth=2,color='dodgerblue')

# Plot the current season
plt.plot(currentSeasonDates,currentSeasonSnowDepth_inIN,label='2023-2024',linewidth=2,color='lime')

plt.legend()

plt.xticks([dayOfYear('2000-09-01')+122-365, dayOfYear('2000-10-01')+122-365,
            dayOfYear('2000-11-01')+122-365, dayOfYear('2000-12-01')+122-365,
            dayOfYear('2001-01-01')+122, dayOfYear('2001-02-01')+122,
            dayOfYear('2001-03-01')+122, dayOfYear('2001-04-01')+122,
            dayOfYear('2001-05-01')+122, dayOfYear('2000-06-01')+122,
            dayOfYear('2000-07-01')+122, dayOfYear('2000-08-01')+122],
           ['Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']);

plt.ylabel('Inches of Snow')

plt.title('Pinkham Notch Snowpack')
