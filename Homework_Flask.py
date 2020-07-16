import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()
Base = automap_base()

#################################################
# Preparing the Database and Tables and Session
#################################################
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome_page():
    """List all available api routes."""
    return (
        f"Available Routes are as follows:<br/>"
        f"Precipitation:        	/api/v1.0/precipitation<br/>"
        f"Station Info:        		/api/v1.0/stations<br/>"
        f"Temp Observations:   		/api/v1.0/tobs<br/>"
        f"Avg Temps Starting on:	/api/v1.0/<start><br/>"
        f"Avg Temps Between:		/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_page():
	session = Session(engine)

	results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
	prcp_dict = {}
	for x in results:
		prcp_dict[x[0]] = x[1]
	return jsonify(prcp_dict)

	session.close()

@app.route("/api/v1.0/stations")
def stations_page():
	session = Session(engine)

	station_info = session.query(Station.station, Station.name).all()
	return jsonify(station_info)

	session.close()

@app.route("/api/v1.0/tobs")
def tobs_page():
	session = Session(engine)
	
	temp_count = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).\
    	order_by(func.count(Measurement.tobs).desc()).all()
	most_tobs = temp_count[0][0]
	temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').filter(Measurement.station == most_tobs).all()
	return jsonify(temp_results)

	session.close()


@app.route("/api/v1.0/<start>")
def tobs_start_page(start):
	session = Session(engine)

	temp_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
	return jsonify(temp_result)

	session.close()

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end_page(start, end):
	session = Session(engine)

	temp_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	return jsonify(temp_result)

	session.close()

#################################################
# Flask Closure
#################################################
if __name__ == '__main__':
    app.run(debug=True)
