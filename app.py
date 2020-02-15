from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


@app.route("/")
def home():
    return """<html>
                <h3><b>Welcome To Hawaii Temperatures!<b></h3>
                    <br>
                    <img src="https://media4.s-nbcnews.com/j/newscms/2019_52/3164476/191228-eddie-aikau-big-wave-invitational-al-1702_8658ae7119e73d40cdf62f7b7ad64b50.fit-760w.jpg"class="center">
                    <br>
                        Please use this link to find the last 12 months of rain totals:
                            <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
                    <br>
                        Rlease use this link to find station data: 
                            <a href="/api/v1.0/stations">/api/v1.0/stations</a>
                    <br>
                        Please use this link to find temperature observations for the last 12 months:
                            <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
                    <br>
                        Please use this link to find temperature observations for a date frame:
                            <a href="/api/v1.0/2015-08-05">/api/v1.0/2015-08-05</a>
                    <br> Please use this link to find temperature observations for a given period:
                            <a href="/api/v1.0/2015-08-05/2015-08-10">/api/v1.0/2015-08-05/2015-08-10</a>
                    <br>

                
            </html>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():

    df_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    measurment_df = (
        session.query(Measurement.date, Measurement.prcp,)
        .filter(Measurement.date >= df_12_months)
        .all()
    )
    # precip = {date: prcp for date, prcp in measurment_df}
    precip = dict(measurment_df)
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temps():
    station_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_last12 = (
        session.query(Measurement.date, Measurement.station, Measurement.tobs)
        .filter(Measurement.date >= station_12_months)
        .all()
    )

    return jsonify(station_last12)


@app.route("/api/v1.0/<start>")
def tobs_start(start):

    temps = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )

    tobs_yr = []
    for temp in temps:
        temps_dict = {}

        temps_dict["Min"] = temp[0]
        temps_dict["Avg"] = temp[1]
        temps_dict["Max"] = temp[2]
        tobs_yr.append(temps_dict)
    return jsonify(tobs_yr)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start,end):
    
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        
        tobs_yr = []
        for temp in temps:
            temps_dict={}
            
            temps_dict["Min"]=temp[0]
            temps_dict["Avg"]=temp[1]
            temps_dict["Max"]=temp[2]
            tobs_yr.append(temps_dict)
        return jsonify(tobs_yr)


if __name__ == "__main__":
    app.run(debug=True)
