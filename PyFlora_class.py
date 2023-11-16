import tkinter as tk
import sqlite3
from tkinter import messagebox
import random
import requests
from bs4 import BeautifulSoup


class PyFloraPot:

    SELECTED_POT = ""
    count_pots = 0

    def __init__(self, pot_name, plant_name, no_measurements):
        self.pot_name = pot_name
        self.plant_name = plant_name
        self.no_measurements = no_measurements
        
        PyFloraPot.count_pots += 1
        
    def update_pot_list(self):
        
        PyFloraPot.count_pots = 0
        PyFloraPot.list_pots = []
        PyFloraPot.all_pot_names = []
        PyFloraPot.max_no_measurements = 0

        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_ALL_POTS = 'SELECT pot_name, plant_name, no_measurements FROM Database_PyFlora_Pots'

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()

                cursor.execute(QUERY_GET_ALL_POTS)
                data = cursor.fetchall()
                all_no_measurements = []
                for pot in data:
                    pot_class = PyFloraPot(pot[0], pot[1], pot[2])
                    PyFloraPot.list_pots.append(pot_class)
                    PyFloraPot.all_pot_names.append(pot[0])
                    all_no_measurements.append(pot[2])
                
                if PyFloraPot.count_pots > 0:
                    PyFloraPot.max_no_measurements = max(all_no_measurements)
                print("All PyFlora Pot names retrived.")
                return PyFloraPot.list_pots

        except sqlite3.Error as e:
            messagebox.showerror(title='Error in retrieving data',
                                 message='Data retrieving unsucessful. Error: ' + str(e))

    def webscrape_temperature(self, url):
        ''' Returns the value of temperature from the provided url '''
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        try:
            container = soup.find('div', class_='location-info block-01')
            temperature = container.find('li', class_='temp').find(
                'span', class_='val').text
            temperature = int(temperature[:-1])
            print('Temperature successfully webscraped.')
            return True, temperature
        except AttributeError as e:
            print(
                f'Unable to webscrape temperature due to error: {e}. Temperature will be randomly generated.')
            return False, temperature

    def generate_measurements(self):
        ''' Generate a value for each pot attribute measured '''

        # humidity in range 10 - 90, with 80% chance 50-70
        if random.random() < 0.8:
            measured_humidity = round(random.uniform(50, 70), 2)
        else:
            measured_humidity = round(random.uniform(10, 90), 2)
        
        # PH in range 0 - 14, with 80% chance 6.0 - 7.5
        if random.random() < 0.8:
            measured_ph = round(random.uniform(0, 14), 2)
        else:
            measured_ph = round(random.uniform(6, 7.5), 2)
    
        # salinity in range 0 - 6, with 80% chance 0 - 2
        if random.random() < 0.8:
            measured_salinitiy = round(random.uniform(0, 2), 2)
        else:
            measured_salinitiy = round(random.uniform(6, 6), 2)
       
        # light in range 0 - 400, with 80% chance 150 - 250
        if random.random() < 0.8:
            measured_light = round(random.uniform(0, 14), 2)
        else:
            measured_light = round(random.uniform(0, 400), 2)

        # temperature in range -20 - 50, with 80% chance 10-25
        temperature_web, retrieved_temperature = self.webscrape_temperature(PyFloraPot, 'https://www.vrijeme.net/hrvatska/zagreb')

        if temperature_web:
            measured_temperature = retrieved_temperature
        else:
            if random.random() < 0.8:
                measured_temperature = round(random.uniform(10, 25), 2)
            else:
                measured_temperature = round(random.uniform(-20, 50), 2)

        # return measured values
        all_measures = {
            'measured_humidity': measured_humidity,
            'measured_ph': measured_ph,
            'measured_salinitiy': measured_salinitiy,
            'measured_light': measured_light,
            'measured_temperature': measured_temperature
            }
        return all_measures

    def save_measurements(self, pots_to_sync):
        # create a new column in Database_PyFlora_Pots if no column for that number of measurement
        
        DB_NAME = 'Database_PyFlora_Pots.db'

        for pot in PyFloraPot.list_pots:
            if pot.pot_name in pots_to_sync:
                new_measurement_no = pot.no_measurements+1
                # get number of measurement for the selected pot 
                # compare it to the highest measurement to see whether new column is necessary
                if new_measurement_no > PyFloraPot.max_no_measurements:
                    QUERIES_ADD_COLUMNS = [
                        f'humidity{new_measurement_no} FLOAT',
                        f'ph{new_measurement_no} FLOAT',
                        f'salinity{new_measurement_no} FLOAT',
                        f'light{new_measurement_no} FLOAT',
                        f'temperature{new_measurement_no} FLOAT'
                    ]
                        #add new columns to the database
                    try:
                        with sqlite3.connect(DB_NAME) as sql_connection:
                            cursor = sql_connection.cursor()
                            for column in QUERIES_ADD_COLUMNS:
                                cursor.execute(f'ALTER TABLE Database_PyFlora_Pots ADD {column}')
                            sql_connection.commit()
                            print("Successfully created new columns in the database.")
                            
                            PyFloraPot.max_no_measurements += 1

                    except sqlite3.Error as e:
                        print('Creating new columns in the database unsuccessful. Error: ', e)
                        return e
                        
                # generate measurements 
                all_measurements = self.generate_measurements(PyFloraPot)
                
                # update database with new measurements

                QUERIES_UPDATE_MEASUREMENTS = [
                    f"humidity{new_measurement_no} = {all_measurements.get('measured_humidity')}",
                    f"ph{new_measurement_no} = {all_measurements.get('measured_ph')}",
                    f"salinity{new_measurement_no} = {all_measurements.get('measured_salinitiy')}",
                    f"light{new_measurement_no} = {all_measurements.get('measured_light')}",
                    f"temperature{new_measurement_no} = {all_measurements.get('measured_temperature')}",
                    f"no_measurements = {new_measurement_no}"
                ]

                try:
                    with sqlite3.connect(DB_NAME) as sql_connection:
                        cursor = sql_connection.cursor()
                        for column in QUERIES_UPDATE_MEASUREMENTS:
                            cursor.execute(f'UPDATE Database_PyFlora_Pots SET {column} WHERE pot_name = "{pot.pot_name}"')
                        sql_connection.commit()
                        print("Successfully inserted the new measurements into the database.")

                except sqlite3.Error as e:
                    print('Inserting new measurements into the database unsucessful. Error: ', e)
                    
    def sync(self, pots_to_sync):
        self.update_pot_list(PyFloraPot)
        self.save_measurements(PyFloraPot, pots_to_sync)

# PyFloraPot_list = PyFloraPot.update_pot_list(PyFloraPot)
# PyFloraPot.sync(PyFloraPot)