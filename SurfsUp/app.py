import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


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
    return f'''
        Available Routes:<br/>
        Precipitation: /api/v1.0/precipitation<br/>
        Stations: /api/v1.0/stations<br/>
        Temperature: /api/v1.0/tobs<br/>
        Temperature for a start date (input your date): /api/v1.0/temp/<start><br/>
        Temperature for a range (input your range): /api/v1.0/temp/<start>/<end><br/>
        '''

@app.route("/api/v1.0/precipitation")
def prcp():

    #return precipitation data for the past year
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23') \
                                                              .filter(Measurement.date<='2017-08-23') \
                                                              .all()
    
    #create dictionary of preciptation data
    prcp_dict={date:prcp for date, prcp in prcp_query}


    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    
    # create list of the stations
    station = session.query(Station.station).all()
    
    stations_list = list(np.ravel(station))

    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Get the dates and temperature observations of the most active station
    station_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-23') \
                                                              .filter(Measurement.date<='2017-08-23') \
                                                              .filter(Measurement.station=='USC00519281') \
                                                              .all()
    
    
    # Createa a dictionary of the dates and temperatures for the station
    station_info={date:tobs for date, tobs in station_data}

    # return a list of the temperature data for the most active station
    return jsonify(station_info)

@app.route("/api/v1.0/temp/<start>")   
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start=None, end=None):
    
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    
    
    if not end:
        range_data=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
        
        session.close()
        
        temps = list(np.ravel(range_data))
        
        return jsonify(temps) 
    
    end = dt.datetime.strptime(end, "%Y-%m-%d")   
    #Query the temperature information
    
    range_data2=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start) \
                                                                                                              .filter(Measurement.date<=end).all()
    temps2 = list(np.ravel(range_data2))

    
    return jsonify(temps2) 
        

if __name__ == '__main__':
    app.run(debug=True)



