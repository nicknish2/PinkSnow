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


### Load Data ###

# Load Historical Pinkham Notch Data
snowDepthClim_inCM = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_snowDepth_cm.npy')
datesClim = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_endWinterYears_cm.npy')

# Load the current year data
currentYearSnowDepth_inCM = np.load('/PinkSnow/data/currentSeasonSnowDepth.npy')
currentYearDates = np.load('/PinkSnow/data/currentSeasonDates.npy')

# Convert to Inches
snowDepthClim_inIn = snowDepthClim_inCM/2.54
currentYearSnowDepth_inIN = currentYearSnowDepth_inCM/2.54

# Calculate Average
averageSnowDepth = np.nanmean(snowDepthClim_inIn,axis=0)

### Make the plot ###

# Put all of these years on a plot

datesForPlotting = np.arange(1,366)

# Shading for historical plot
n = len(snowDepthClim)
colors = plt.cm.Greys(np.linspace(0,1,n))

for i in range(len(snowDepthClim)):
    plt.plot(datesForPlotting,snowDepthClim_inIn[i],c=colors[i],linewidth = .5)

# Plot the average
plt.plot(range(1,366),averageSnowDepth,label='1930-2023 Average',linewidth=2,color='dodgerblue')

# Plot the current season
plt.plot(range(1,366),averageSnowDepth,label='2023-2024',linewidth=2,color='lime')

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
