### Make the plot of snow depth

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import copy
import glob
from datetime import date

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


### Load Data ###

# Available Stations
availableStations = ['HVCN3','HTLN3','GKBN3','CRNN3','KMWN','ZFHN3',
                     'CAWN3','NH-CR-26','ESDN3','GHMN3','NH-CR-41','TMWN3',
                     'NH-CR-11','NCON3','NH-CR-27','LLHN3','HUBN3','NH-CR-15',
                     'NH-CS-19','NH-CR-46','NH-BK-26','NH-CR-46','NH-GR-47','WENN3',
                     'NH-BK-9','MMNV1','MMSV1','NH-GR-11']

# Load data for the current year
currentSeasonSnowDepthDict_inCM = {}
for stat in availableStations:
    currentSeasonSnowDepthDict_inCM[stat] = np.array([])

currentSeasonDatesDict = {}
for stat in availableStations:
    currentSeasonDatesDict[stat] = np.array([])

dir_path = '/PinkSnow/data/2024/*.txt' # path with the daily downloads of data, select the 12Z (morning EST)

for ifile,file in enumerate(glob.glob(dir_path, recursive=True)):
    currentSeasonSnowDepthDict_inCM,currentSeasonDatesDict = snowpackOnDate(availableStations,file,
                                                                            currentSeasonSnowDepthDict_inCM,currentSeasonDatesDict)

# Make it so that currentSeasonDatesDict has Sept 1 as day 1
currentSeasonDatesDict = {i:currentSeasonDatesDict[i]+122 for i in currentSeasonDatesDict.keys()}
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
snowDepthClim_inCM = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_snowDepth_cm.npy')
datesClim = np.load('/PinkSnow/data/historical/pinkhamSnowpackClim1930-2023_endWinterYears_cm.npy')


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
    
    
### Station names for more readable plots
fullStationNames = {"HVCN3":"HARVARD CABIN",
"HTLN3":"HERMIT LAKE",
"GKBN3":"GRAY KNOB",
"CRNN3":"CARTER NOTCH",
"KMWN":"MOUNT WASHINGTON",
"ZFHN3":"ZEALAND FALLS HUT",
"CAWN3":"CRAWFORD NOTCH",
"NH-CR-26":"CENTER SANDWICH",
"ESDN3":"EAST SANDWICH",
"GHMN3":"PINKHAM NOTCH",
"NH-CR-41":"ALBANY",
"TMWN3":"TAMWORTH",
"NH-CR-11":"NORTH CONWAY 1.4 SSW, NH",
"NCON3":"NORTH CONWAY",
"NH-CR-27":"TAMWORTH 0.4 NNW, NH",
"LLHN3":"LONESOME LAKE HUT",
"HUBN3":"HUBBARD BROOK",
"NH-CR-15":"JACKSON",
"NH-CS-19":"CARROLL",
"NH-CR-46":"NORTH CONWAY 1.8 SSE, NH",
"NH-BK-26":"MEREDITH",
"NH-GR-47":"LITTLETON",
"WENN3":"WENTWORTH, NH",
"NH-BK-9":"MEREDITH 2.9 SSW, NH",
"NH-GR-11":"PLYMOUTH",
"MMSV1":"MT MANSFIELD BOT",
"MMNV1":"MT MANSFIELD TOP"
                   }


### Make the plot ###

fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(15, 5))

## Plot data from around New England Mountains ##

# Plot the current season

stationsOfInterest = ['NH-CR-15','LLHN3','MMNV1','CAWN3','GKBN3']

for i in stationsOfInterest:
    ax1.plot(currentSeasonDatesDict[i],currentSeasonSnowDepthDict_inIN[i],label='2023-2024 {}'.format(fullStationNames[i]),linewidth=2)

ax1.legend()

ax1.set_xticks([dayOfYear('2000-09-01')+122-365, dayOfYear('2000-10-01')+122-365,
            dayOfYear('2000-11-01')+122-365, dayOfYear('2000-12-01')+122-365,
            dayOfYear('2001-01-01')+122, dayOfYear('2001-02-01')+122,
            dayOfYear('2001-03-01')+122, dayOfYear('2001-04-01')+122,
            dayOfYear('2001-05-01')+122, dayOfYear('2000-06-01')+122,
            dayOfYear('2000-07-01')+122, dayOfYear('2000-08-01')+122],
           ['Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']);

ax1.set_ylabel('Inches of Snow')
ax1.set_ylim([0, 80])
ax1.set_title('New England Snowpack')

## Plot Pinkham Notch Data and climatology ##

# Put all of these years on a plot

datesForPlotting = np.arange(1,366)

# Shading for historical plot
n = len(snowDepthClim_inIN)
colors = plt.cm.Greys(np.linspace(0,1,n))

for i in range(len(snowDepthClim_inIN)):
    ax2.plot(datesForPlotting,snowDepthClim_inIN[i],c=colors[i],linewidth = .25)

# Plot the average
ax2.plot(range(1,366),averageSnowDepth_inIN,label='1930-2023 Pinkham Average',linewidth=2,color='dodgerblue')

# Plot the current season

stationsOfInterest = ['GHMN3']

for i in stationsOfInterest:
    ax2.plot(currentSeasonDatesDict[i],currentSeasonSnowDepthDict_inIN[i],label='2023-2024 {}'.format(fullStationNames[i]),linewidth=2,color='orange')

ax2.legend()

ax2.set_xticks([dayOfYear('2000-09-01')+122-365, dayOfYear('2000-10-01')+122-365,
            dayOfYear('2000-11-01')+122-365, dayOfYear('2000-12-01')+122-365,
            dayOfYear('2001-01-01')+122, dayOfYear('2001-02-01')+122,
            dayOfYear('2001-03-01')+122, dayOfYear('2001-04-01')+122,
            dayOfYear('2001-05-01')+122, dayOfYear('2000-06-01')+122,
            dayOfYear('2000-07-01')+122, dayOfYear('2000-08-01')+122],
           ['Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']);

ax2.set_ylabel('Inches of Snow')

ax2.set_title('Pinkham Notch Snowpack')
ax2.set_ylim([0, 80])

today = date.today()
d2 = today.strftime("%B %d, %Y")
fig.suptitle(d2);

plt.savefig('/PinkSnow/{}.png'.format(today.strftime("%b-%d-%Y"))
