import sqlalchemy
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
    session.query(Measurement.date, Measurement.prcp).all()
    session.close()

if __name__ == '__main__':
    app.run(debug=True)