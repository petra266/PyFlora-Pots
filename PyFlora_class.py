import tkinter as tk
import sqlite3
from tkinter import messagebox
import random
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd


class PyFloraPot:

    SELECTED_POT = ""
    count_pots = 0

    def __init__(
            self, pot_name, plant_name, no_measurements, 
            optimal_humidity, optimal_ph, max_salinity, 
            optimal_light, optimal_temperature, photo
            ):
        
        self.pot_name = pot_name
        self.plant_name = plant_name
        self.no_measurements = no_measurements

        self.optimal_humidity = optimal_humidity
        self.optimal_ph = optimal_ph
        self.max_salinity = max_salinity
        self.optimal_light = optimal_light
        self.optimal_temperature = optimal_temperature

        self.photo = photo
        
        PyFloraPot.max_no_measurements = 0
        PyFloraPot.count_pots += 1
    
    def get_dataframe_for_all_pots(self):
        '''retrieves data from the database for all pots 
        and returns it as a dataframe or error'''
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_ALL_POTS = f'SELECT * FROM Database_PyFlora_Pots'
        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                PyFloraPot.df = pd.read_sql(QUERY_GET_ALL_POTS, con=sql_connection)
                PyFloraPot.max_no_measurements = PyFloraPot.df['no_measurements'].max()
                return True, None
            
        except sqlite3.Error as e:
            return False, e    
        
    def get_dataframe_for_opened_pot(self, pot_name):
        '''retrieves data from the database for selected pot 
        and returns it as a dataframe or error'''
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_OPENED_POT = f'SELECT * FROM Database_PyFlora_Pots WHERE pot_name="{pot_name}"'
        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                PyFloraPot.df = pd.read_sql(QUERY_GET_OPENED_POT, con=sql_connection)
                PyFloraPot.max_no_measurements = PyFloraPot.df['no_measurements'].max()
                return True, None

        except sqlite3.Error as e:
            return False, e

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
        # timestamp of measurement
        measured_datetime = datetime.datetime.now()

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
            measured_salinity = round(random.uniform(0, 2), 2)
        else:
            measured_salinity = round(random.uniform(6, 6), 2)
       
        # light in range  - 400, with 80% chance 150 - 250
        if random.random() < 0.8:
            measured_light = round(random.uniform(150, 250), 2)
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
        all_measures = {'measured_datetime' : measured_datetime,
            'measured_humidity': measured_humidity,
            'measured_ph': measured_ph,
            'measured_salinity': measured_salinity,
            'measured_light': measured_light,
            'measured_temperature': measured_temperature
            }
        return all_measures

    def query_generated_measurements(self, new_measurement_no):
        # generate new measurements
        all_measurements = self.generate_measurements(PyFloraPot)

        #format datetime
        formatted_datetime= all_measurements.get('measured_datetime').strftime('%Y-%m-%d %H:%M:%S')

        # update database with new measurements
        QUERIES_UPDATE_MEASUREMENTS = [
            f"datetime{new_measurement_no} = '{formatted_datetime}'",
            f"humidity{new_measurement_no} = {all_measurements.get('measured_humidity')}",
            f"ph{new_measurement_no} = {all_measurements.get('measured_ph')}",
            f"salinity{new_measurement_no} = {all_measurements.get('measured_salinity')}",
            f"light{new_measurement_no} = {all_measurements.get('measured_light')}",
            f"temperature{new_measurement_no} = {all_measurements.get('measured_temperature')}",
            f"no_measurements = {new_measurement_no}"
        ]
        return QUERIES_UPDATE_MEASUREMENTS

    def query_optimized_measurements(self, new_measurement_no, pots_to_sync):
        measured_datetime = datetime.datetime.now()
        formatted_datetime = measured_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        for pot in PyFloraPot.list_pots:
            if pot in pots_to_sync:
            # update database with new measurements
                QUERIES_OPTIMIZE_MEASUREMENTS = [
                f"datetime{new_measurement_no} = '{formatted_datetime}'",
                f"humidity{new_measurement_no} = {PyFloraPot.df.loc[PyFloraPot.df['pot_name'] == pot, 'optimal_humidity'].values[0]}",
                f"ph{new_measurement_no} = {PyFloraPot.df.loc[PyFloraPot.df['pot_name'] == pot, 'optimal_ph'].values[0]}",
                f"salinity{new_measurement_no} = 0",
                f"light{new_measurement_no} = {PyFloraPot.df.loc[PyFloraPot.df['pot_name'] == pot, 'optimal_light'].values[0]}",
                f"temperature{new_measurement_no} = {PyFloraPot.df.loc[PyFloraPot.df['pot_name'] == pot, 'optimal_temperature'].values[0]}",
                f"no_measurements = {new_measurement_no}"
            ]
        return QUERIES_OPTIMIZE_MEASUREMENTS

    def create_new_measurement_columns(self, database_name, new_measurement_no):
        ''' Creates a new column in Database_PyFlora_Pots if no column for that number of measurement '''

        QUERIES_ADD_COLUMNS = [
            f'datetime{new_measurement_no} VARCHAR(100)',
            f'humidity{new_measurement_no} FLOAT',
            f'ph{new_measurement_no} FLOAT',
            f'salinity{new_measurement_no} FLOAT',
            f'light{new_measurement_no} FLOAT',
            f'temperature{new_measurement_no} FLOAT'
        ]
            #add new columns to the database
        try:
            with sqlite3.connect(database_name) as sql_connection:
                cursor = sql_connection.cursor()
                for column in QUERIES_ADD_COLUMNS:
                    cursor.execute(f'ALTER TABLE Database_PyFlora_Pots ADD {column}')
                sql_connection.commit()
                print("Successfully created new columns in the database.")
                
            PyFloraPot.max_no_measurements += 1

        except sqlite3.Error as e:
            print('Creating new columns in the database unsuccessful. Error: ', e)
    
    def save_measurements(self, pots_to_sync, generated):
        success = True

        self.get_dataframe_for_all_pots(PyFloraPot)
        
        PyFloraPot.list_pots = list(PyFloraPot.df['pot_name'])
        print('PRINTING 1:   ', PyFloraPot.list_pots)

        DB_NAME = 'Database_PyFlora_Pots.db'      
        for pot in PyFloraPot.list_pots:
            if pot in pots_to_sync:
                # get number of measurement for the selected pot 
                # compare it to the highest measurement to see whether new column is necessary
                new_measurement_no = PyFloraPot.df.loc[PyFloraPot.df['pot_name'] == pot, 'no_measurements'].values[0] + 1
                print('PRINTING NEW MEASUREMENT:    ', new_measurement_no)
                if new_measurement_no > PyFloraPot.max_no_measurements:
                    self.create_new_measurement_columns(PyFloraPot, DB_NAME, new_measurement_no)
                
                # create query to generate values or input optimal values, depending on the function call (generated True/False)
                if generated:
                    QUERY_UPDATE_MEASUREMENTS = self.query_generated_measurements(PyFloraPot, new_measurement_no)
                else:
                    QUERY_UPDATE_MEASUREMENTS = self.query_optimized_measurements(PyFloraPot, new_measurement_no, pots_to_sync)
                
                # save data
                try:
                    with sqlite3.connect(DB_NAME) as sql_connection:
                        cursor = sql_connection.cursor()
                        for column in QUERY_UPDATE_MEASUREMENTS:
                            cursor.execute(f'UPDATE Database_PyFlora_Pots SET {column} WHERE pot_name = "{pot}"')
                        sql_connection.commit()
                        print("Successfully inserted the new measurements into the database.")

                except sqlite3.Error as e:
                    print('Inserting new measurements into the database unsucessful. Error: ', e)
                    success = False
        if success:
            return True, None
        else:
            return False, e
                                            
    def sync(self, pots_to_sync, generated):

        self.df = self.get_dataframe_for_all_pots(PyFloraPot)
        syncing_success, syncing_error = self.save_measurements(PyFloraPot, pots_to_sync, generated)
        
        return syncing_success, syncing_error