import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

######falsk setup###
app =Flask(__name__)

@app.route("/")
def home():
    return(
    f"Welcome and here's the list to explore<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end>"
    )

year_ago=dt.date(2017, 8, 23)-dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
data=session.query(Measurement.date, Measurement.prcp).filter(func.strftime(Measurement.date) >= year_ago).all()
data

@app.route("/api/v1.0/precipitation")
def date():
    date_info=[]
    for d in data:
        date_dict={}
        date_dict["date"]=data[0]
        date_dict["prcp"]=data[1]
        date_info.append(date_dict)
    return jsonify(date_info)

@app.route("/api/v1.0/stations")
def station(): 
    results=session.query(Station).all()
    all_station=[]
    for station in results:
        station_dict={}
        station_dict["station"]=station.station
        station_dict["name"]=station.name
        all_station.append(station_dict)
    return jsonify(all_station)


year_ago=dt.date(2017, 8, 23)-dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
tobs=session.query(Measurement.date, Measurement.tobs).filter(func.strftime(Measurement.date) >= year_ago).all()
tobs

@app.route("/api/v1.0/tobs")
def temp():
    temp_info=[]
    for t in tobs:
        temp_dict={}
        temp_dict["date"]=tobs[0]
        temp_dict["tobs"]=tobs[1]
        temp_info.append(temp_dict)
    return jsonify(temp_info)

@app.route("/api/v1.0/<start>")
def input(start):
    start_date=dt.datetime.strptime(start,'%Y-%m-%d')
    last_year=start_date-dt.timedelta(days=365)
    result=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(func.strftime(Measurement.date) >= last_year).filter(func.strftime(Measurement.date) <= dt.date(2017, 8, 23)).all()
    result_list=list(np.ravel(result))
    return jsonify(result_list)

@app.route("/api/v1.0/<start>/<end>")
def input2(start,end):
    start_date=dt.datetime.strptime(start,'%Y-%m-%d')
    end_date=dt.datetime.strptime(end,'%Y-%m-%d')
    last_year=start-dt.timedelta(days=365)
    result=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(func.strftime(Measurement.date) >= last_year).filter(func.strftime(Measurement.date) <= end_date).all()
    result_list=list(np.ravel(result))
    return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)