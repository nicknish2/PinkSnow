# PinkSnow

Tracking daily snowpack depth at
[Pinkham Notch](https://appalachiantrail.com/20130607/amcs-pinkham-notch-visitor-center/)
and other stations in the white mountains. We currently track several stations in the
White Mountains plus Mt Mansfield in Vermont.

Authors: Paul Nicknish [@nicknish2](https://github.com/nicknish2) and Milan Klöwer ([@milankl](https://github.com/milankl)), MIT.

## Data

The data is from NOAA's
[National Operational Hydrological Remote Sensing Center](https://www.nohrsc.noaa.gov/)
as published [here](https://www.nohrsc.noaa.gov/nsa/discussions_text/Northeast/snowdepth/).
Recent years are copied into this repository.
Data is found as `.txt` files in [data/2024](https://github.com/nicknish2/PinkSnow/tree/main/data/2024)
for the year 2024. Historical data is in
[data/historical](https://github.com/nicknish2/PinkSnow/tree/main/data/historical)
and used to plot the climatology.

## Visualization

Data is visualized in [`plot/images`](https://github.com/nicknish2/PinkSnow/tree/main/plot/images).

## Available Stations

In the [National Operational Hydrological Remote Sensing Center](https://www.nohrsc.noaa.gov/)
the following stations in the White Mountains and in around Mt Mansfield in Vermont are available
among a wider network of stations across the North East US. Each station has an identifier
and the stations we select are a subset of those

### Stations

|Station_Id|Name|Latitude|Longitude|Elevation|Zip_Code|
|-|-|-|-|-|-|
|MMNV1|MT. MANSFIELD|44.52480|-72.81540|1190 meters|05672|
|MMSV1|MOUNT MANSFIELD|44.53330|-72.83330|697 meters|05489|
|ZFHN3|ZEALAND FALLS HUT|44.19590|-71.49440|805 meters|03574|
|LLHN3|LONESOME LAKE HUT|44.13820|-71.70310|846 meters|03251|
|GKBN3|GRAY KNOB|44.33260|-71.30930|1329 meters|00181|
|CRNN3|CARTER NOTCH|44.25940|-71.19550|1008 meters|00168|
|MWN|MOUNT WASHINGTON|44.26670|-71.30000|1715 meters|00176|
|MMSV1|MOUNT MANSFIELD|44.53330|-72.83330|697 meters|05489|
|KMWN|MOUNT WASHINGTON|44.26666|-71.30000|1715 meters|00176|
|KMWN|MOUNT WASHINGTON|44.26666|-71.30000|1715 meters|00176|
|HTLN3|HERMIT LAKE SNOWPLOT|44.26130|-71.28330|1151 meters|00176|
|NH-CS-19|CARROLL 4.6 NE, NH|44.33765|-71.46461|525 meters|03598|
|GHMN3|PINKHAM NOTCH|44.25800|-71.25250|620 meters|00177|
|CAWN3|CRAWFORD NOTCH|44.21960|-71.41270|581 meters|03598|
|HUBN3|HUBBARD BROOK|43.93330|-71.71670|489 meters|03223|
|NH-CR-41|ALBANY 2.8 SW, NH|43.92648|-71.21556|204 meters|03818|
|NH-GR-47|LITTLETON 7.3 W, NH|44.31847|-71.91086|341 meters|03561|
|NH-CR-15|JACKSON 3.7 NW, NH|44.19069|-71.22598|363 meters|03846|
|NH-CR-11|NORTH CONWAY 1.4 SSW, NH|44.03556|-71.14010|164 meters|03860|
|TMWN3|TAMWORTH 4|43.86390|-71.26610|164 meters|03886|
|TMWN3|TAMWORTH 4|43.86390|-71.26610|164 meters|03886|
|NH-CR-46|NORTH CONWAY 1.8 SSE, NH|44.02955|-71.11664|170 meters|03860|
|NH-CR-27|TAMWORTH 0.4 NNW, NH|43.86449|-71.26610|164 meters|03886|
|NH-CR-26|CENTER SANDWICH 4.9 E, NH|43.80976|-71.34150|229 meters|03227|
|NH-BK-9|MEREDITH 2.9 SSW, NH|43.62245|-71.53510|210 meters|03253|
|NH-BK-26|MEREDITH 3.3 NNE, NH|43.69844|-71.46930|276 meters|03226|
|NCON3|NORTH CONWAY|44.05620|-71.12970|163 meters|03860|
|ESDN3|EAST SANDWICH|43.80990|-71.34250|224 meters|03227|

### New Hampshire

![image](https://github.com/nicknish2/PinkSnow/assets/25530332/4aed8569-3e25-4013-9a70-bb751a80706c)

(Created using Matplotlib, Cartopy and OpenStreetMaps)

### Vermont

![image](https://github.com/nicknish2/PinkSnow/assets/25530332/d0793c4a-e39f-4c5a-95c5-eaf9d1b7dc69)

(Created using Matplotlib, Cartopy and OpenStreetMaps)
