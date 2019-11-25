#Import libraries
#%matplotlib inline #For jupyter notebook
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt    

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect existing database to new model
Base = automap_base()
#Reflect Tables
Base.prepare(engine,reflect=True)

#View all classes
Base.classes.keys()

#Save tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session from Python to DB
session = Session(engine)

#Get column names
engine.execute("SELECT * from measurement").keys()
#Or, use
#Base.metadata.tables.values()

### PRECIPITATION DATA ###

#Find Most Recent Date
session.query(Measurement.date).order_by(Measurement.date.desc()).all()

# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from the last data point in the database
# Find end date
session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# Subtract 1 year from end date
td = dt.timedelta(days = 365)
end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
start_date = dt.date(2017, 8, 23) - td

start_end = Measurement.date.between('2016-08-23','2017-08-23')

# Perform a query to retrieve the data and precipitation scores
prcp_12month = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
filter(start_end).\
order_by(Measurement.station).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_12month_df = pd.DataFrame(prcp_12month)    
prcp_12month_df = prcp_12month_df.set_index('date')

# Sort the dataframe by date
prcp_12month_df = prcp_12month_df.sort_values(by = 'date')

# Use Pandas Plotting with Matplotlib to plot the data
prcp_plot = prcp_12month_df.plot(subplots = True, figsize = (12,8), use_index = True)
prcp_plot

# Using Matplotlib to plot data
x_axis = prcp_12month_df.index
y_axis = prcp_12month_df ['prcp']

fig, ax = plt.subplots(figsize = (12,8))

ax.plot(x_axis, y_axis)

plt.xlabel("Days")
plt.ylabel("Precipitation")
plt.title("Precipitation levels over 1 year")
plt.savefig("Precipitation levels over 1 year.png")
plt.show()

# Use Pandas to calculate the summary statistics for the precipitation data
prcp_12month_df.describe()


### STATION DATA ###

# Design a query to show how many stations are available in this dataset
engine.execute("SELECT * from station").keys()
stations = [i for i in session.query(Station.station).distinct()]
#stations

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
a = session.query(Station.station, func.count(Measurement.station)).\
filter(Measurement.station == Station.station).\
group_by(Measurement.station).\
order_by(func.count(Measurement.station).desc()).all()

most_active = a[0][0]

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of most active station
session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
filter(Measurement.station == most_active).all()

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
start = start_date.strftime('%Y-%m-%d')
end = end_date[0]
def calc_temps(start_date, end_date):
    
    return session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps(start, end))

# Design a query to retrieve the last 12 months of temperature observation data (tobs).
# Filter by the station with the highest number of observations.
# Plot the results as a histogram with bins=12.
x = session.query(Measurement.tobs).\
filter(Measurement.date >= start).\
filter(Measurement.date <= end).\
filter(Measurement.station == most_active).all()

temp_12_months = np.asarray(x)
plt.hist(temp_12_months, bins = 12)
plt.ylabel("Frequency")
plt.xlabel("Temperature (F)")
plt.title("Frequencies of Temperature Values Observed over 12 months")