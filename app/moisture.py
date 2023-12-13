#moisture.py
import time
import Adafruit_ADS1x15
from app.mocks import ADS1115Mock
from app.db_actions import insert_moisture_data

# Function to determine whether to use actual hardware or a mock
def get_adc():
    running_on_local_machine = True  # Replace with your actual check
    if running_on_local_machine:
        return ADS1115Mock()
    else:
        return Adafruit_ADS1x15.ADS1115(busnum=1)

# Create an ADS1115 ADC object
adc = get_adc()

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Single threshold for wet/dry classification (adjust as needed)
THRESHOLD = 2000

# Function to determine the wet-dry level based on the soil moisture percentage
def wet_dry_level(soil_moisture):
    if soil_moisture < THRESHOLD:
        return "DRY"
    else:
        return "WET"

# Function to read data from the soil moisture sensor and insert it into the database
def read_and_insert_data():
    # Read the raw analog value from channel A3
    raw_value = adc.read_adc(3, gain=GAIN)

    # Determine the wet-dry level based on the raw ADC value
    level = wet_dry_level(raw_value)

    # Print the results
    print("Raw Value: {} \t Wet-Dry Level: {}".format(raw_value, level))

    # Insert data into the pi_plants table
    insert_moisture_data('your_plant_id', level)

# Main loop to read the analog value from the soil moisture sensor
def run_soil_moisture_reader():
    try:
        while True:
            # Read and insert data into the database
            read_and_insert_data()

            # Add a delay between readings (adjust as needed)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting the program.")
