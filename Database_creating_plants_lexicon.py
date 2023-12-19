"""Creating the plants lexicon with 10 plants"""
import os
import sqlite3
import sys

def convert_image_to_blob(image_path):
    with open(image_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

# setup to keep images in a separate folder
IMAGES_FOLDER = 'Images'
if not os.path.exists(IMAGES_FOLDER):
    print('Error: The images folder does not exist. Table not created.')
    SystemExit(1)


DB_NAME = 'Database_plants_lexicon.db'

# create sql queries

QUERY_CREATE = '''
CREATE TABLE IF NOT EXISTS Database_plants_lexicon (
    id INTEGER PRIMARY KEY,
    plant_name VARCHAR(50) NOT NULL UNIQUE,
    optimal_humidity INTEGER NOT NULL CHECK 
        (optimal_humidity >= 0 AND optimal_humidity <= 100),
    optimal_ph INTEGER NOT NULL CHECK 
        (optimal_ph >= 0 AND optimal_ph <= 14),
    max_salinity INTEGER NOT NULL CHECK (max_salinity >= 0),
    optimal_light INTEGER NOT NULL CHECK (optimal_light >= 0),
    optimal_temperature INTEGER NOT NULL,
    photo BLOB
    );
'''

QUERY_INSERT = '''
INSERT INTO Database_plants_lexicon 
(plant_name, optimal_humidity, 
optimal_ph, max_salinity, optimal_light, optimal_temperature, photo)
VALUES (?, ?, ?, ?, ?, ?, ?)
'''

INSERT_DICT = [
    {'plant_name': 'Basil (Ocimum basilicum)',
     'optimal_humidity': 60,
     'optimal_ph': 6,
     'max_salinity': 2,
     'optimal_light': 350,
     'optimal_temperature': 24,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Basil (Ocimum basilicum).jpg'))
     },
    {'plant_name': 'Hibiscus (Hibiscus rosa-sinensis)',
     'optimal_humidity': 65,
     'optimal_ph': 6,
     'max_salinity': 2,
     'optimal_light': 350,
     'optimal_temperature': 24,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Hibiscus (Hibiscus rosa-sinensis).jpg'))
     },
    {'plant_name': 'Spider Plant (Chlorophytum comosum)',
     'optimal_humidity': 40,
     'optimal_ph': 6,
     'max_salinity': 1.5,
     'optimal_light': 200,
     'optimal_temperature': 18,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Spider Plant (Chlorophytum comosum).jpg'))
     },
    {'plant_name': 'Snake Plant (Sansevieria trifasciata)',
     'optimal_humidity': 40,
     'optimal_ph': 6.5,
     'max_salinity': 2,
     'optimal_light': 150,
     'optimal_temperature': 18,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Snake Plant (Sansevieria trifasciata).jpg'))
     },
    {'plant_name': 'Peace Lily (Spathiphyllum spp.)',
     'optimal_humidity': 40,
     'optimal_ph': 6.5,
     'max_salinity': 1.5,
     'optimal_light': 150,
     'optimal_temperature': 22,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Peace Lily (Spathiphyllum spp.).jpg'))
     },
    {'plant_name': 'Aloe Vera (Aloe barbadensis miller)',
     'optimal_humidity': 30,
     'optimal_ph': 6,
     'max_salinity': 1.5,
     'optimal_light': 200,
     'optimal_temperature': 22,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Aloe Vera (Aloe barbadensis miller).jpg'))
     },
    {'plant_name': 'ZZ Plant (Zamioculcas zamiifolia)',
     'optimal_humidity': 40,
     'optimal_ph': 6,
     'max_salinity': 1.5,
     'optimal_light': 150,
     'optimal_temperature': 18,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'ZZ Plant (Zamioculcas zamiifolia).jpg'))
     },
    {'plant_name': 'Fiddle Leaf Fig (Ficus lyrata)',
     'optimal_humidity': 50,
     'optimal_ph': 6,
     'max_salinity': 2,
     'optimal_light': 300,
     'optimal_temperature': 24,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Fiddle Leaf Fig (Ficus lyrata).jpg'))
     },
    {'plant_name': 'Jade Plant (Crassula ovata)',
     'optimal_humidity': 40,
     'optimal_ph': 6.5,
     'max_salinity': 1.5,
     'optimal_light': 200,
     'optimal_temperature': 20,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Jade Plant (Crassula ovata).jpg'))
     },
    {'plant_name': 'Boston Fern (Nephrolepis exaltata)',
     'optimal_humidity': 60,
     'optimal_ph': 5.5,
     'max_salinity': 1.5,
     'optimal_light': 200,
     'optimal_temperature': 18,
     'photo' : convert_image_to_blob(os.path.join(IMAGES_FOLDER, 'Boston Fern (Nephrolepis exaltata).jpg'))
     }
]


INSERT_LIST = []
for i in INSERT_DICT:
    plant = (i['plant_name'], i['optimal_humidity'], i['optimal_ph'],
             i['max_salinity'], i['optimal_light'], i['optimal_temperature'], i['photo'])
    INSERT_LIST.append(plant)

# Create the plants lexicon
try:
    sqlite_connection = sqlite3.connect(DB_NAME)
    cursor = sqlite_connection.cursor()
    cursor.execute(QUERY_CREATE)
    sqlite_connection.commit()
    print("Database successfully created.")

except sqlite3.Error as e:
    print("Execution unsuccessful. Error when creating the database: ", e)
    SystemExit(1)

# Insert plants into the lexicon

try:
    for plant in INSERT_LIST:
        cursor.execute(QUERY_INSERT, plant)
    sqlite_connection.commit()
    print("Successfully inserted into the database.")
    cursor.close()

    table_exists = 1

except sqlite3.Error as e:
    print("Error when inserting into the database: ", e)

    # Close the connection to the database
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("SQLite connection closed.")