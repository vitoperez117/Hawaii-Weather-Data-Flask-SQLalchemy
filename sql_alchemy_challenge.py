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
x_axis = prcp_12month_df.index
y_axis = prcp_12month_df ['prcp']