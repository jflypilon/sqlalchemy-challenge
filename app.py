# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

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
        f"Available Routes:<br/><br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"NOTE: If no end-date is provided, the trip api calculates stats through 08/23/17<br>" 
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return json with the date as the key and the value as the precipitation"""
    # Query all jsonified precipitation data for the last year in the database
    start_date = '2016-08-23'
    Annual = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()
    
    all_dates = []
    all_precip = []
    for date, dailytotal in Annual :
        all_dates.append(date)
        all_precip.append(dailytotal)
        
    precip_dict = dict(zip(all_dates, all_precip))

    return jsonify(precip_dict)    
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return jsonified data of all the stations in the database"""
    # Query all jsonified precipitation data for the last year in the database
    Active = session.query(Measurement.station).\
        group_by(Measurement.station).all()
    session.close()
    
    stations_list = list(np.ravel(Active))
    
    return jsonify(stations_list)
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return jsonified data for the most active station (USC00519281)"""
    """Only returns jsonified data for the last year of data"""
    # Query all jsonified temperature data for the last year in the database
    start_date = '2016-08-23'
    
    Obs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date, Measurement.station == 'USC00519281').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()

    obs_dates = []
    obs_temps = []
    for date, observation in Obs :
        obs_dates.append(date)
        obs_temps.append(observation)
        
    temp_dict = dict(zip(obs_dates, obs_temps))

    return jsonify(temp_dict)   

@app.route("/api/v1.0/trip/<start_date>")
def TripA(start_date, end_date = '2017-08-23'):
    session = Session(engine)
    
    Most = session.query(func.min(Measurement.tobs), 
                     func.max(Measurement.tobs),
                     func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    
    Tripstat = []
    for min, avg, max in Most:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Avg"] = avg
        trip_dict["Max"] = max
        Tripstat.append(trip_dict)
        

@app.route("/api/v1.0/trip/<start_date>/<end_date>")
def TripB(start_date, end_date = '2017-08-23'):
    session = Session(engine)
    
    Most = session.query(func.min(Measurement.tobs), 
                     func.max(Measurement.tobs),
                     func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    
    Tripstat = []
    for min, avg, max in Most:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Avg"] = avg
        trip_dict["Max"] = max
        Tripstat.append(trip_dict)
    
if __name__ == '__main__':
    app.run(debug=True)




































