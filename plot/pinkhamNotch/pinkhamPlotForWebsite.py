### Make the plot of snow depth

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import copy
import glob
from datetime import date

### Define Functions ###

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
def snowpackOnDate(stationNames,dataPath,snowDepthDict,datesDict):
    dataOnDate = pd.read_csv(dataPath, sep = "|",header=1)
    
    for name in stationNames:
        # Station is in the text file
        if sum(dataOnDate.Station_Id == name) > 0:
            snowpack = dataOnDate[dataOnDate.Station_Id == name].Amount.values[0]
            dateString = dataOnDate[dataOnDate.Station_Id == name]['DateTime_Report(UTC)'].values[0][:-3]
            snowDepthDict[name] =  np.append(snowDepthDict[name],snowpack)
            datesDict[name] =  np.append(datesDict[name],dayOfYear(dateString))
        # Station is not in the text file
    return snowDepthDict,datesDict

def historicSeasonStrings(seasonStrings,snowDepth):
    currString = ''
    for i in range(len(seasonStrings)):
        if i<len(seasonStrings)-1:
            currString = currString + '{}: {} \n'.format(seasonStrings[i],round(snowDepth[i],1))
        else:
            currString = currString + '{}: {}'.format(seasonStrings[i],round(snowDepth[i],1))
    return currString


### Load Data ###
currentYear = 2024

# Available Stations
#availableStations = ['HVCN3','HTLN3','GKBN3','CRNN3','KMWN','ZFHN3',
#                     'CAWN3','NH-CR-26','ESDN3','GHMN3','NH-CR-41','TMWN3',
#                     'NH-CR-11','NCON3','NH-CR-27','LLHN3','HUBN3','NH-CR-15',
#                     'NH-CS-19','NH-CR-46','NH-BK-26','NH-CR-46','NH-GR-47','WENN3',
#                     'NH-BK-9','MMNV1','MMSV1','NH-GR-11']

# Load Pinkham Notch Data
availableStations = ['GHMN3']

# Load data for the current year
currentSeasonSnowDepthDict_inCM = {}
for stat in availableStations:
    currentSeasonSnowDepthDict_inCM[stat] = np.array([])

currentSeasonDatesDict = {}
for stat in availableStations:
    currentSeasonDatesDict[stat] = np.array([])

dir_path = '/Users/paulnicknish/Desktop/pinkhamNotchStuff/gitHubTesting/PinkSnow-main/data/2024/*.txt' # path with the daily downloads of data, select the 12Z (morning EST)

for ifile,file in enumerate(glob.glob(dir_path, recursive=True)):
    currentSeasonSnowDepthDict_inCM,currentSeasonDatesDict = snowpackOnDate(availableStations,file,
                                                                            currentSeasonSnowDepthDict_inCM,currentSeasonDatesDict)

# Make it so that currentSeasonDatesDict has Sept 1 as day 1
adjustToSept1 = 121 # want sept 1 to be day 1
currentSeasonDatesDict = {i:currentSeasonDatesDict[i]+adjustToSept1 for i in currentSeasonDatesDict.keys()}
for name in availableStations: 
    currVal = currentSeasonDatesDict[name]
    currVal[currVal>365] = currVal[currVal>365]-365
    currentSeasonDatesDict[name] = currVal
    
# Add NANs where station data is missing
# this can make the plots hard to read
addNANs = False
if addNANs:
    for stat in availableStations:
        for d in range(1,366):
            if d in currentSeasonDatesDict[stat]:
                pass
            else:
                currentSeasonDatesDict[stat] = np.append(currentSeasonDatesDict[stat],d)
                currentSeasonSnowDepthDict_inCM[stat] = np.append(currentSeasonSnowDepthDict_inCM[stat],np.nan)
    
# Load Historical Pinkham Notch Data
lastYearInClimatology = currentYear-1
snowDepthClim_inCM = np.load('/Users/paulnicknish/Desktop/pinkhamNotchStuff/gitHubTesting/PinkSnow-main/data/historical/pinkhamSnowpackClim1930-{}_snowDepth_cm.npy'.format(lastYearInClimatology))
datesClim = np.load('/Users/paulnicknish/Desktop/pinkhamNotchStuff/gitHubTesting/PinkSnow-main/data/historical/pinkhamSnowpackClim1930-{}_endWinterYears_cm.npy'.format(lastYearInClimatology))


# Convert to Inches
snowDepthClim_inIN = snowDepthClim_inCM/2.54
currentSeasonSnowDepthDict_inIN = {i:currentSeasonSnowDepthDict_inCM[i]/2.54 for i in currentSeasonSnowDepthDict_inCM.keys()}

# Calculate Average
averageSnowDepth_inIN = np.nanmean(snowDepthClim_inIN,axis=0)

# Sort the current season data according to the dates
for name in availableStations:
    sortInds = np.argsort(currentSeasonDatesDict[name])
    currentSeasonDatesDict[name] = currentSeasonDatesDict[name][sortInds]
    currentSeasonSnowDepthDict_inIN[name] = currentSeasonSnowDepthDict_inIN[name][sortInds]
    
    
    
### Make the plot ###

fig, (ax1) = plt.subplots(1, 1,figsize=(8, 5),dpi=300)

dayOfYear_startFromJan1 = date.today().timetuple().tm_yday
if dayOfYear_startFromJan1 > 245:
    dayOfYear_startFromSept1 = dayOfYear_startFromJan1 + adjustToSept1 - 365
else:
    dayOfYear_startFromSept1 = dayOfYear_startFromJan1 + adjustToSept1


## Plot Pinkham Notch Data and climatology ##

# Put all of these years on a plot
datesForPlotting = np.arange(1,366) # day 1 is Sept 1

# Shading for historical plot
n = len(snowDepthClim_inIN)
colors = plt.cm.Greys(np.linspace(0,1,n))

# Plot the climatology
for i in range(len(snowDepthClim_inIN)):
    ax1.plot(datesForPlotting,snowDepthClim_inIN[i],c=colors[i],linewidth = .25,alpha = .3,zorder=0)

# Plot the average
ax1.plot(datesForPlotting,averageSnowDepth_inIN,label='1930-{} Climatology'.format(lastYearInClimatology),linewidth=2,color='k',zorder=1)
# Get the average snow depth on today's date
averageSnowDepthToday = averageSnowDepth_inIN[dayOfYear_startFromSept1-1] # minus 1 because day 1 is index 0

# Plot the current season in Pinkham Notch
pinkhamNotchCode = 'GHMN3'
ax1.plot(currentSeasonDatesDict[pinkhamNotchCode],currentSeasonSnowDepthDict_inIN[pinkhamNotchCode],label='{}-{}'.format(lastYearInClimatology,lastYearInClimatology+1),linewidth=2,color='red',zorder=10)
# get the current seasonal snowpack on this date
currentSeasonSnowDepthToday = currentSeasonSnowDepthDict_inIN[pinkhamNotchCode][currentSeasonDatesDict[pinkhamNotchCode]==dayOfYear_startFromSept1]
if len(currentSeasonSnowDepthToday)==0:
    currentSeasonSnowDepthToday = 0.0
else:
    currentSeasonSnowDepthToday = currentSeasonSnowDepthToday[0]

# Highlight the last N years
highlightLastNYears = 3
seasonsToShow = ['{}-{}'.format(lastYearInClimatology-i, lastYearInClimatology-i+1) for i in range(1,highlightLastNYears+1)]
datesUpToToday = np.arange(1,dayOfYear_startFromSept1 + 1)
trackHistoricSnowDepthOnCurrDay = []
for i in range(highlightLastNYears):
    ax1.plot(datesUpToToday,snowDepthClim_inIN[-1-i][:len(datesUpToToday)],linewidth = 1.25,label=seasonsToShow[i])
    
    # Get the snow pack on this day in the last N years
    snowDepthInYear = snowDepthClim_inIN[-1-i]
    snowDepthOnCurrentDay = snowDepthInYear[len(datesUpToToday)]
    trackHistoricSnowDepthOnCurrDay = trackHistoricSnowDepthOnCurrDay + [snowDepthOnCurrentDay]
    
    
# Format Figure
ax1.legend()
ax1.set_xticks([dayOfYear('2000-09-01')+adjustToSept1-365, dayOfYear('2000-10-01')+adjustToSept1-365,
            dayOfYear('2000-11-01')+adjustToSept1-365, dayOfYear('2000-12-01')+adjustToSept1-365,
            dayOfYear('2001-01-01')+adjustToSept1, dayOfYear('2001-02-01')+adjustToSept1,
            dayOfYear('2001-03-01')+adjustToSept1, dayOfYear('2001-04-01')+adjustToSept1,
            dayOfYear('2001-05-01')+adjustToSept1, dayOfYear('2000-06-01')+adjustToSept1,
            dayOfYear('2000-07-01')+adjustToSept1, dayOfYear('2000-08-01')+adjustToSept1],
           ['Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']);

ax1.set_ylabel('Inches of Snow')

ax1.set_title('Pinkham Notch Snowpack (in)')
ax1.set_ylim([0, 80])

today = date.today()
d2 = today.strftime("%B %d, %Y")
fig.suptitle(d2);

# Make Text box

stringForTextBox = 'On this date:'+ '\nAverage Snowpack: {} \nCurrent Season: {} \n'.format(round(averageSnowDepthToday,1),round(currentSeasonSnowDepthToday,1)) + historicSeasonStrings(seasonsToShow,trackHistoricSnowDepthOnCurrDay);

ax1.text(0.05, 0.95, stringForTextBox, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top');

plt.savefig('pinkhamNotchSnowpack{}.png'.format(today.strftime("%b-%d-%Y"))