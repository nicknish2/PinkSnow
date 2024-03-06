import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import copy
import glob


# Function that returns the snow depth in cm and the date (as a string)
# for a given station name and datafile corresponding to a specific day

# NOTE: right now, only set up to handle one station #
def snowpackOnDate(stationName,dataPath):
    dataOnDate = pd.read_csv(dataPath, sep = "|",header=1)
    snowpack = dataOnDate[dataOnDate.Name == stationName].Amount.values[0]
    dateString = dataOnDate[dataOnDate.Name == stationName]['DateTime_Report(UTC)'].values[0][:-3]
    return snowpack,dateString


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


## Example:
# dir_path = '/Users/paulnicknish/Desktop/pinkhamNotchStuff/dailyTestData/*.txt'
# for file in glob.glob(dir_path, recursive=False):
#     print(snowpackOnDate('PINKHAM NOTCH',file))

currentSeasonSnowDepth = np.array([])
currentSeasonDates = np.array([])

stationsOfInterest = ['PINKHAM NOTCH']
currYear = '2024'

dir_path = '/PinkSnow/data/' + currYear + '/*12.txt' # path with the daily downloads of data, select the 12Z (morning EST)
for ifile,file in enumerate(glob.glob(dir_path, recursive=False)):
    currentSnowDepth,currentDateString = snowpackOnDate(stationsOfInterest[0],file)
    currentSeasonSnowDepth = np.append(currentSeasonSnowDepth,currentSnowDepth)
    currentSeasonDates = np.append(currentSeasonDates,dayOfYear(currentDateString))
    
# Save
pathToSave = '/PinkSnow/data/'
np.save(pathToSave+'currentSeasonSnowDepth.npy',currentSeasonSnowDepth)
np.save(pathToSave+'currentSeasonDates.npy',currentSeasonDates)
