import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json
from flask import Flask, jsonify
import pandas as pd



#C:\Users\casas\Desktop\Starter_Code\Starter_Code\Resources\hawaii.sqlite

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#Start at the homepage.
#List all the available routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    most_active_station = 'USC00519397'
    latest_date = session.query(func.max(measurement.date)).scalar()
    last_12_months = (dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)).date()

    prcp_results = session.query(measurement.date, measurement.prcp).filter(
    measurement.station == most_active_station,
    measurement.date >= last_12_months).all()

    prcp_dict = {str(date): prcp for date, prcp in prcp_results}

    prcp_json = json.dumps(prcp_dict, indent=4)
        
    return prcp_json

# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.        



@app.route("/api/v1.0/stations")
def stations():
    csv_file_path = 'Resources\hawaii_stations.csv'  
    df = pd.read_csv(csv_file_path)
    json_data = df.to_json(orient='records', date_format='iso')  

    json_file_path = 'archivo.json'  
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_data)
    return json_data





@app.route("/api/v1.0/tobs")
def tobs():
    
    most_active_station = 'USC00519397'

    latest_date = session.query(func.max(measurement.date)).scalar()
    latest_date_obj = dt.datetime.strptime(latest_date, "%Y-%m-%d")

    one_year_ago = latest_date_obj - dt.timedelta(days=365)

    temp_results = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == most_active_station,
        measurement.date >= one_year_ago.date(),
        measurement.date <= latest_date_obj.date()
    ).all()

    temp_data = [{"date": str(date), "temperature": tobs} for date, tobs in temp_results]

    temp_json = json.dumps(temp_data, indent=4)
    
    return temp_json
    
    
    
    
@app.route("/api/v1.0/")    
def v1():
    pass    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)