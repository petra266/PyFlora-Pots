"""Creating the PyFlora Pots database"""

import os
import sqlite3

os.chdir('PyFlora Pots')

DB_NAME = 'Database_PyFlora_Pots.db'

QUERY_CREATE = '''
CREATE TABLE IF NOT EXISTS Database_PyFlora_Pots (
    id INTEGER PRIMARY KEY,
    PyFlora_pot_name VARCHAR(20) NOT NULL UNIQUE,
    plant_name VARCHAR(50) NOT NULL UNIQUE,
    optimal_humidity INTEGER NOT NULL CHECK 
        (optimal_humidity >= 0 AND optimal_humidity <= 100),
    optimal_ph INTEGER NOT NULL CHECK 
        (optimal_ph >= 0 AND optimal_ph <= 14),
    max_salinity INTEGER NOT NULL CHECK (max_salinity >= 0),
    optimal_light INTEGER NOT NULL CHECK (optimal_light >= 0),
    optimal_temperature INTEGER NOT NULL
    );
'''

QUERY_INSERT = '''
INSERT INTO Database_PyFlora_Pots (PyFlora_pot_name,
    plant_name, optimal_humidity, optimal_ph,
    max_salinity, optimal_light, optimal_temperature)
VALUES ("Balcony", "Basil", 50, 7, 200, 500, 22)
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


# TO DELETE AT THE END
# Insert plants into the lexicon
try:
    cursor.execute(QUERY_INSERT)
    sqlite_connection.commit()
    print("Successfully inserted into the database.")
    cursor.close()

except sqlite3.Error as e:
    print("Error when inserting into the database: ", e)
    SystemExit(1)
# TO DELETE AT THE END


# Close the connection to the database
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("SQLite connection closed.")
