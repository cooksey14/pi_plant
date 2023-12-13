# db_actions.py
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

def connect_to_database():
    # Your database connection parameters
    db_params = {
        "host": "localhost",
        "port": int(os.getenv("DB_PORT")),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }
    logging.info(f"DB_HOST: {db_params['host']}")
    logging.info(f"DB_PORT: {db_params['port']}")
    return psycopg2.connect(**db_params)

def insert_moisture_data(plant_id, moisture_level):
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # Insert data into the pi_plants table
        cur.execute(
            "INSERT INTO pi_plants (plant_id, moisture, date_added) VALUES (%s, %s, %s)",
            (plant_id, moisture_level, datetime.now())
        )

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully")

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error inserting moisture data: {e}")

    finally:
        cur.close()
        conn.close()

def get_moisture_data():
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT moisture, plant_id, date_added FROM pi_plants ORDER BY date_added DESC LIMIT 10")
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error retrieving moisture data: {e}")
        return None
    finally:
        cur.close()
        conn.close()
