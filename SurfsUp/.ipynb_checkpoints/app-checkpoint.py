import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables

Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return f'''
        Available Routes:<br/>
        Precipitation: /api/v1.0/precipitation<br/>
        Stations: /api/v1.0/stations<br/>
        Temperature: /api/v1.0/tobs<br/>
        /api/v1.0/<start><br/>
        /api/v1.0/<start>/<end><br/>
        '''

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #return precipitation data for the past year
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23') \
                                                              .filter(Measurement.date<='2017-08-23') \
                                                              .all()
    
    #create dictionary of preciptation data
    prcp_dict={date:prcp for date, prcp in prcp_query}
    
    #close your session
    session.close()

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    # create list of the stations
    station = session.query(Station.station).all()
    
    stations_list = list(np.ravel(station))

    # close your session
    session.close()
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    # Get the dates and temperature observations of the most active station
    station_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-23') \
                                                              .filter(Measurement.date<='2017-08-23') \
                                                              .filter(Measurement.station=='USC00519281') \
                                                              .all()
    
    
    # Createa a dictionary of the dates and temperatures for the station
    station_info={date:tobs for date, tobs in station_data}

    # return a list of the temperature data for the most active station
    return jsonify(station_info)



if __name__ == '__main__':
    app.run(debug=True)



