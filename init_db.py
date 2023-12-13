import os
import psycopg2

# Database connection parameters
db_params = {
        "host": "localhost",
        "port": int(os.getenv("DB_PORT")),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }

def table_exists(table_name, cursor):
    # Check if the table exists in the database
    cursor.execute("SELECT EXISTS ("
                   "   SELECT 1 "
                   "   FROM   information_schema.tables "
                   "   WHERE  table_name = %s"
                   ");", (table_name,))
    return cursor.fetchone()[0]

def create_table(cursor):
    # Create the pi_plants table if it doesn't exist
    cursor.execute('CREATE TABLE IF NOT EXISTS pi_plants ('
                   '   id SERIAL PRIMARY KEY,'
                   '   plant_id VARCHAR(255) NOT NULL'
                   '   moisture TEXT NOT NULL DEFAULT \'\','
                   '   date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
                   ');')

# Main script
try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    table_name = "pi_plants"

    # Check if the table already exists
    if not table_exists(table_name, cur):
        create_table(cur)
        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists. Skipping table creation.")

    # Commit changes and close the cursor and connection
    conn.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    cur.close()
    conn.close()