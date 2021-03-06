import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect existing database to new model
Base = automap_base()
#Reflect Tables
Base.prepare(engine,reflect=True)

#Save tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session from Python to DB
session = Session(engine)

# /
# Home page.
# List all routes that are available.

#12 month timeframe
start_date = '2016-08-23'
end_date = '2017-01-01'
start_end = Measurement.date.between('2016-08-23','2017-08-23')

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    Available routes
    <br>
    <br>/
    <br>/api/v1.0/precipitation
    <br>/api/v1.0/stations
    <br>/api/v1.0/tobs
    <br>/api/v1.0/start
    <br>/api/v1.0/start/end
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp in prcp:
        date_prcp = {}
        date_prcp["date"] = date
        date_prcp["prcp"] = prcp
        all_prcp.append(date_prcp)

    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def stations():
    stations = [i for i in session.query(Station.station).distinct()]
    session.close()

    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def temp():
    temp_12month = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(start_end).\
        order_by(Measurement.date).all()

    session.close()
    
    temp_12month_ls = []
    for date, station, tobs in temp_12month:
        temp_12month_dict = {}
        temp_12month_dict["date"] = date
        temp_12month_dict["station"] = station
        temp_12month_dict["tobs"] = tobs
        temp_12month_ls.append(temp_12month_dict)

    return jsonify(temp_12month_ls)


@app.route('/api/v1.0/start')
def temp_time():
    temp_start = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).group_by(Measurement.date).all()
    
    session.close()

    temp_start_ls = []
    for date, min_temp, max_temp, avg_temp in temp_start:
        temp_start_dict = {}
        temp_start_dict["date"] = date
        temp_start_dict["min_temp"] = min_temp
        temp_start_dict["max_temp"] = max_temp
        temp_start_dict["avg_temp"] = avg_temp
        temp_start_ls.append(temp_start_dict)

    return jsonify(temp_start_ls)


@app.route('/api/v1.0/start/end')
def temp_time_start_end():
    temp_start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).\
                group_by(Measurement.date).all()

    session.close()

    temp_start_end_ls = []
    for date, min_temp, max_temp, avg_temp in temp_start_end:
        temp_start_end_dict = {}
        temp_start_end_dict["date"] = date
        temp_start_end_dict["min_temp"] = min_temp
        temp_start_end_dict["max_temp"] = max_temp
        temp_start_end_dict["avg_temp"] = avg_temp
        temp_start_end_ls.append(temp_start_end_dict)

    return jsonify(temp_start_end_ls)
    
if __name__ == '__main__':
    app.run(debug=True)