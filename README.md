This tool provides an easy-to-use command line interface for producing shapefiles with transit headways and frequencies for user-selected time periods and routes. It relies heavily on the [gtfs_functions](https://github.com/Bondify/gtfs_functions) python library for the essential calculations. 

## First time setup and installation

For all below steps, you will need to install [Python3](https://www.python.org/downloads/) through the Anaconda distribution [(miniconda version)](https://docs.conda.io/en/latest/miniconda.html). 

### Install with Anaconda

1. Clone this repo (or just click the code > download zip button). This will be your working directory.

2. Open Anaconda Prompt (not the regular windows cmd prompt). Run `cd <path to working directory>`

3. Run `conda env create –f environment.yml` If you want to change the environment name, open the environment.yml file in a text editor and change name in the first line. 

## Running the tool

1. Place input GTFS zip files in the "feeds" folder inside the working directory. Do not unzip them. The folder must be called feeds (all lowercase). 

2. Open Anaconda Prompt. Cd to your working directory.

3. Run `conda activate <enviroment name>`

4. Run `python app.py`

5. Follow the messages displayed in the prompt (see "settings" and "configuration" below).

6. When finished, run `conda deactivate` to leave the environment. 

## Settings

**Route list:** comma-separated list of routes (corresponding to route short name in GTFS)
Time Interval: Integer in 24-hr clock. frequencies will only be calculated for the specified hours

**Day type:** Busiest Date will filter the feed to the single busiest service date. Weekend or weekday will select all trips of the corresponding type.

**Split results by hour?** If selected, will create a separate feature in the shapefile for each hour within the specified time interval. Otherwise, all trips in the time interval will be aggregated into one time bucket (appropriate for most use cases). 

## Optional Configuration

The tool can be configured using an optional file. Use the config.py file as an example. This file consists of a dictionary with the following key-value pairs:

- **Feed:** name of the GTFS zip file including extension
- **Day Type:** One of "weekday", "weekend", "All Days", "Busiest Day"
- **Routes:** List of routes entered as strings (e.g. ["101", "102", "156"]. These should correspond to the route_short_name field in GTFS.
- **Time Interval:** List containing 3 items. Integer for start and end hour (24-hr clock), and "yes" or "no" for splitting results by hour (e.g. [6,9, "yes"]). 
- **File name:** what to call the output file (without the extension)

Name the configuration file anything you want and place in the same folder. Run the tool with the name of the config file (excluding the .py extension) as a command line argument (e.g. python app.py config). 

## Results

The attributes below appear in the shapefile. 

- **s_st_name:** the first stop on the segment
- **e_st_name:** the last stop on the segment
- **route_name:** comma-separated list of routes running on this segment in the specified time period
- **hourly_frequency:** Buses per hour
- **trips_in_p:** Total bus trips in the specified time period
- **headway_mins:** Scheduled-based headway. Minutes between each bus, on average

## Feed Comparison
The compare.py file allows users to compare two similar GTFS feeds processed using the above steps to identify differences in frequency. 

### inputs

Two zipped shapefiles produced using the app.py file described above. 

### usage

Run `python compare.py <file 1 name> <file 2 name>` from the Anaconda prompt. File names should **not** include the .zip extension. 

### output

A folder called "feed_comparison" containing the loose files making up an ESRI shapefile with the feed comparison results. The "seg_type" attribute describes whether the segment is old, new, or the same in both feeds. Segments that are not the same will have null values for either the old or new attribute. 




