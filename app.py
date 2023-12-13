from flask import Flask, jsonify, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from app.db_actions import insert_moisture_data, get_moisture_data
from app.moisture import run_soil_moisture_reader
import pytz

app = Flask(__name__)

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Use the API endpoint to insert data into the database
def insert_data_into_db():
    response = app.test_client().post('/insert_moisture_data')
    return response.json()

# Function to insert data into the database
def read_and_insert_data():
    # Read soil moisture data
    moisture_level = run_soil_moisture_reader()

    # Insert data into the pi_plants table
    insert_moisture_data('pineapple', moisture_level)

# Schedule the job to run once a day
scheduler = BackgroundScheduler()

timezone = pytz.timezone('America/Chicago')
scheduler = BackgroundScheduler(timezone=timezone)


# Add the job to run once a day
scheduler.add_job(
    read_and_insert_data,
    trigger='cron',
    hour=12,
    minute=0,
    id='read_and_insert_data'
)

# Start the scheduler
scheduler.start()

# API endpoint to manually trigger the data insertion
@app.route('/insert_moisture_data', methods=['GET', 'POST'])
def insert_moisture_data_route():
    if request.method == 'POST':
        # Read data from the form
        plant_id = request.form.get('plant_id')
        moisture_level = request.form.get('moisture_level')

        # Insert data into the pi_plants table
        insert_moisture_data(plant_id, moisture_level)

        return jsonify({"status": "success", "message": "Data inserted successfully"})
    else:
        # Render the HTML form
        return render_template('index.html')


# API endpoint to retrieve moisture data from the pi_plants table
@app.route('/get_moisture_data', methods=['GET'])
def get_moisture_data_route():
    moisture_data = get_moisture_data()
    return jsonify({"status": "success", "moisture_data": moisture_data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
