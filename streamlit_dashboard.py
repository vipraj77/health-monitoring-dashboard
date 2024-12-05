import streamlit as st
from pymongo import MongoClient
import time

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['health_db']
collection = db['sensor_data']

st.title('Real-Time Health Monitoring Dashboard')

# Display data from MongoDB
while True:
    # Fetch the most recent data from MongoDB
    data = collection.find().sort([('_id', -1)]).limit(1)  # Get latest entry
    for entry in data:
        st.write(f"Heart Rate: {entry['heart_rate']} BPM")
        st.write(f"Glucose Level: {entry['glucose_level']} mg/dL")
        st.write(f"Blood Pressure: {entry['blood_pressure']}")
        st.write(f"Oxygen Level: {entry['oxygen_level']} %")
    
    # Refresh every 1 second
    time.sleep(1)
