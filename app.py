# 1. import dependancies
from flask import Flask
from flask import jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct



#-----------------------------------------------------



# 2. Database 
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station




# 3. Create an app, using pass __name__
app = Flask(__name__)




# 4. Define what to do when a user hits the different routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )



# app route Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all passenger names"""
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    weather_data = []

    for date, prcp in results:
        weather_dict = {}
        weather_dict['date'] = date
        weather_dict['prcp'] = prcp
        weather_data.append(weather_dict)

    return jsonify(weather_data)




# app route Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of additional passenger data including the name, age, and gender"""
    results = session.query(Station.station).all()

    session.close()

    stations = []
    for result in results:
        stations.append(result[0])

    return jsonify(stations)    





# app route TOBS
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a JSON list of Temperature Observations for the year prior"""
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_prior).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date.desc()).all()

    session.close()

    return jsonify(station_results)





# app route start and end
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    """Return a JSON list of TMIN, TAVG, and TMAX"""
    min_temp = func.min(Measurement.tobs)
    avg_temp = func.avg(Measurement.tobs)
    max_temp = func.max(Measurement.tobs)
    temp_results = session.query(min_temp, avg_temp, max_temp).\
    filter(Measurement.date >= start).all()

    session.close()

    return jsonify(temp_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    """Return a JSON list of TMIN, TAVG, and TMAX"""
    min_temp = func.min(Measurement.tobs)
    avg_temp = func.avg(Measurement.tobs)
    max_temp = func.max(Measurement.tobs)
    temp_results = session.query(min_temp, avg_temp, max_temp).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    session.close()
    
    return jsonify(temp_results)       





# 6. Run the app

if __name__ == "__main__":
    app.run(debug=True)
