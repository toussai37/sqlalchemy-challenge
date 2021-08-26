import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

twelve_months_ago = '2016-08-23'


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    

    session = Session(engine)

    precipitation_results = session.query(measurement.date, measurement.prcp).group_by(measurement.date).all()
    
    session.close()


    all_results = []
    
    for date, prcp in precipitation_results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_results.append(measurement_dict)


    return jsonify(all_results)



@app.route("/api/v1.0/stations")
def stations():
    
    
    session = Session(engine)

    results = session.query(station.station).all()

    session.close()

 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2016-08-23').filter(measurement.station == 'USC00519281').all()

    session.close()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
def start(start):
    
    session = Session(engine)
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()

    all_results = list(np.ravel(results))
    
    return jsonify(all_results)



if __name__ == "__main__":
    app.run(debug=True)
