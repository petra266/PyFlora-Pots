"""Creating the user database with 1 user"""

import sqlite3
import sys

DB_NAME = 'Database_users.db'

QUERY_CREATE = '''
CREATE TABLE IF NOT EXISTS Database_users (
    id INTEGER PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);
'''
QUERY_INSERT = '''
INSERT INTO Database_users (firstname, lastname, username, password)
VALUES (?, ?, ?, ?)
'''

INSERT_LIST = [("Jane", "Doe", "admin", "pass123")]


# Create the user database
try:
    sqlite_connection = sqlite3.connect(DB_NAME)
    cursor = sqlite_connection.cursor()
    cursor.execute(QUERY_CREATE)
    sqlite_connection.commit()
    print("Database successfully created.")

except sqlite3.Error as e:
    print("Execution unsuccessful. Error when creating the database: ", e)
    sys.exit(1)


# Insert users into the database
try:
    for user in INSERT_LIST:
        cursor.execute(QUERY_INSERT, user)
    sqlite_connection.commit()
    print("Successfully inserted into the database.")
    cursor.close()

except sqlite3.Error as e:
    print("Error when inserting into the database: ", e)


# Close the connection to the database
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("SQLite connection closed.")
