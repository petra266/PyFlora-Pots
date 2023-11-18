""" GUI for inspecting data for each PyFlora Pot """

import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot


class InterfaceOpenPot:

    def __init__(self, root):
        self.toplevel_open_pot = tk.Toplevel(root)
        self.toplevel_open_pot.title("PyFlora Pots - " + PyFloraPot.SELECTED_POT)
        self.toplevel_open_pot.geometry('1200x800')

        #retrieve pot information and save it into a class property
        self.POT_INFO = self.retrieve_pot_info()
    
        self.create_textvariables()
        self.interface_elements()

    def retrieve_pot_info(self):
        """ Retrieve all data from the Database_PyFlora_Pots and return it as a dictionary"""
        
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_POT = 'SELECT * FROM Database_PyFlora_Pots WHERE pot_name = '

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()
                cursor.execute(QUERY_GET_POT + '"{}"'.format(PyFloraPot.SELECTED_POT))
                data = cursor.fetchall()[0]
                # drop empty measure columns
                data = [i for i in data if i is not None]
                # assign values to dict
                POT_INFO = {              
                    'pot_name': data[1],
                    'plant_name': data[2],
                    'optimal_humidity': data[3],
                    'optimal_ph': data[4],
                    'max_salinity': data[5],
                    'optimal_light': data[6],
                    'optimal_temperature': data[7],
                    'no_measurements': data[8],
                    'current_humidity': data[-5],
                    'current_ph': data[-4],
                    'current_salinity': data[-3],
                    'current_light': data[-2],
                    'current_temperature': data[-1]
                    }
                print("PyFlora Pot information retrived.")
                return POT_INFO

        except sqlite3.Error as e:
            print('Data retrieving unsucessful. Error: ', e)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' + str(e) + "\nPlease restart the application",
                                 parent=self.toplevel_open_pot)
            self.toplevel_open_pot.destroy()       

    def delete_pot(self):
        """ Deletes the PyFlora Pot from the Database_PyFlora_Pots """
        
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_DELETE_POT = 'DELETE FROM Database_PyFlora_Pots WHERE pot_name = '

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()
                cursor.execute(QUERY_DELETE_POT + '"{}"'.format(PyFloraPot.SELECTED_POT))
                print("PyFlora Pot successfully deleted.")
                messagebox.showinfo(title='PyFlora Pot removed!',
                                 message='You have successfully removed PyFlora Pot: {}'.format(PyFloraPot.SELECTED_POT),
                                 parent=self.toplevel_open_pot)

        except sqlite3.Error as e:
            print('Data retrieving unsucessful. Error: ', e)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' + str(e) + "\nPlease restart the application",
                                 parent=self.toplevel_open_pot)
        self.toplevel_open_pot.destroy()       

    def update_current_values_shown(self):
        self.current_humidity.set(f"Current humidity:   {self.POT_INFO['current_humidity']}")
        self.current_ph.set(f"Current PH:   {self.POT_INFO['current_ph']}")
        self.current_salinity.set(f"Current salinity:   {self.POT_INFO['current_salinity']}")
        self.current_light.set(f"Current light exposure:   {self.POT_INFO['current_light']}")
        self.current_temperature.set(f"Current temperature:   {self.POT_INFO['current_temperature']}")
    
    def check_needed_actions(self):
        ''' Checks the latest measure for each pot attribute. If deviation from optimal value is acceptable, 
            action label is set to checkmark, otherwise a cross'''
        
        # check humidity - accepted deviation +/- 15% 
        self.humidity_check = '\u2717' if abs(self.POT_INFO['optimal_humidity'] - self.POT_INFO['current_humidity']) > 15 else '\u2713'
        #humidity_action_label.config(text=f"Current humidity:   {self.POT_INFO['current_humidity']} {humidity_check}")

        # ph - accepted deviation +/- 1,5
        self.ph_check = '\u2717' if abs(self.POT_INFO['optimal_ph'] - self.POT_INFO['current_ph']) > 1.5 else '\u2717'

        # salinity - has to be below limit
        self.salinitiy_check = '\u2717' if self.POT_INFO['max_salinity'] > self.POT_INFO['current_salinity'] else '\u2717'
        
        # light - accepted deviation +/- 100 PAR
        self.light_check = '\u2717' if abs(self.POT_INFO['optimal_light'] - self.POT_INFO['current_light']) > 100 else '\u2713'

        # temperature - accepted deviation +/- 8 degrees
        self.temperature_check = '\u2717' if abs(self.POT_INFO['optimal_temperature'] - self.POT_INFO['current_temperature']) > 8 else '\u2713'

    def sync(self):
        syncing_error = PyFloraPot.sync(PyFloraPot, self.POT_INFO['pot_name']) # returns an error message if syncing unsucessful
        if syncing_error:
            messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: ' + str(syncing_error) + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)
        self.retrieve_pot_info()
        self.update_current_values_shown()
        self.check_needed_actions()

    def create_textvariables(self):
       # create text variables to show pot status and actions needed
        self.current_humidity = tk.StringVar()
        self.humidity_action = tk.StringVar()
        
        self.current_ph = tk.StringVar()
        self.ph_action = tk.StringVar()
        
        self.current_salinity = tk.StringVar()
        self.salinity_action = tk.StringVar()

        self.current_light = tk.StringVar()
        self.light_action = tk.StringVar()

        self.current_temperature = tk.StringVar()
        self.temperature_action = tk.StringVar()

    def interface_elements(self):

        # pot basic information
        pot_name_label = tk.Label(self.toplevel_open_pot, text="PyFlora Pot Name:   " + self.POT_INFO['pot_name'])
        pot_name_label.grid(row=1, column=1)

        plant_name_label = tk.Label(self.toplevel_open_pot, text="Plant name:   " + self.POT_INFO['plant_name'])
        plant_name_label.grid(row=2, column=1)

        # humidity
        self.current_humidity_label = tk.Label(self.toplevel_open_pot, textvariable=self.current_humidity)
        self.current_humidity_label.grid(row=10, column=1)

        optimal_humidity_label = tk.Label(self.toplevel_open_pot, text=f"Optimal humidity:   {self.POT_INFO['optimal_humidity']}")
        optimal_humidity_label.grid(row=10, column=2)

        humidity_action_label = tk.Label(self.toplevel_open_pot, textvariable=self.humidity_action)
        humidity_action_label.grid(row=10, column=3)

        # PH
        self.current_ph_label = tk.Label(self.toplevel_open_pot, textvariable=self.current_humidity)
        self.current_ph_label.grid(row=11, column=1)

        optimal_ph_label = tk.Label(self.toplevel_open_pot, text=f"Optimal PH:   {self.POT_INFO['optimal_ph']}")
        optimal_ph_label.grid(row=11, column=2)

        ph_action_label = tk.Label(self.toplevel_open_pot, textvariable=self.ph_action)
        ph_action_label.grid(row=11, column=3)

        # salinity
        self.current_salinity_label = tk.Label(self.toplevel_open_pot, textvariable=self.current_salinity)
        self.current_salinity_label.grid(row=12, column=1)

        optimal_salinity_label = tk.Label(self.toplevel_open_pot, text=f"Salinity celiing:   {self.POT_INFO['max_salinity']}")
        optimal_salinity_label.grid(row=12, column=2)

        salinity_action_label = tk.Label(self.toplevel_open_pot, textvariable=self.salinity_action)
        salinity_action_label.grid(row=12, column=3)

        # light
        self.current_light_label = tk.Label(self.toplevel_open_pot, textvariable=self.current_light)
        self.current_light_label.grid(row=13, column=1)

        optimal_light_label = tk.Label(self.toplevel_open_pot, text=f"Optimal light:   {self.POT_INFO['optimal_light']}")
        optimal_light_label.grid(row=13, column=2)

        light_action_label = tk.Label(self.toplevel_open_pot, textvariable=self.light_action)
        light_action_label.grid(row=13, column=3)

        # temperature
        self.current_temperature_label = tk.Label(self.toplevel_open_pot, textvariable=self.current_temperature)
        self.current_temperature_label.grid(row=14, column=1)

        optimal_temperature_label = tk.Label(self.toplevel_open_pot, text=f"Optimal temperature:   {self.POT_INFO['optimal_temperature']}")
        optimal_temperature_label.grid(row=14, column=2)

        temperature_action_label = tk.Label(self.toplevel_open_pot, textvariable=self.temperature_action)
        temperature_action_label.grid(row=14, column=3)

        # other
        sync_button = tk.Button(self.toplevel_open_pot, text="Sync only this pot", command=self.sync)
        sync_button.grid(row=999, column=1)

        delete_button = tk.Button(self.toplevel_open_pot, text="Remove pot...", command=self.delete_pot)
        delete_button.grid(row=1000, column=2)

        back_button = tk.Button(self.toplevel_open_pot, text="Back",
                                command=self.toplevel_open_pot.destroy)
        back_button.grid(row=1000, column=0)