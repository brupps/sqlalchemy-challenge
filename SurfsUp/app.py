# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# Create first route for precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
  
    # Calculate the date one year from the last date in data set.
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


# Create second route for stations
"""List of stations to review"""
@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to the DB
    session = Session(engine)

    # List the stations and their counts in descending order.
    station_list = session.query(Station.station).\
        order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_list))

    return jsonify(all_stations)


#Create third route for TOBs
"""List of TOBs"""

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session from Python to the DB
    session = Session(engine)

    # List the tobs results
    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()

    session.close()
   
    # Convert list of tuples into normal list
    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)






if __name__ == '__main__':
    app.run(debug=True)