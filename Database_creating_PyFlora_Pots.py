"""Creating the PyFlora Pots database"""

import os
import sqlite3

DB_NAME = 'Database_PyFlora_Pots.db'

# Create sql queries

QUERY_CREATE = '''
CREATE TABLE IF NOT EXISTS Database_PyFlora_Pots (
    id INTEGER PRIMARY KEY,
    pot_name VARCHAR(20) NOT NULL UNIQUE,
    plant_name VARCHAR(50) NOT NULL,
    optimal_humidity INTEGER NOT NULL CHECK 
        (optimal_humidity >= 0 AND optimal_humidity <= 100),
    optimal_ph INTEGER NOT NULL CHECK 
        (optimal_ph >= 0 AND optimal_ph <= 14),
    max_salinity INTEGER NOT NULL CHECK (max_salinity >= 0),
    optimal_light INTEGER NOT NULL CHECK (optimal_light >= 0),
    optimal_temperature INTEGER NOT NULL,
    photo BLOB UNIQUE,
    no_measurements INTEGER NOT NULL
    );
'''

# Create the empty PyPots database
try:
    sqlite_connection = sqlite3.connect(DB_NAME)
    cursor = sqlite_connection.cursor()
    cursor.execute(QUERY_CREATE)
    sqlite_connection.commit()
    print("Database successfully created.")

except sqlite3.Error as e:
    print("Execution unsuccessful. Error when creating the database: ", e)
    SystemExit(1)


# Close the connection to the database
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("SQLite connection closed.")
