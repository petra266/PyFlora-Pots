""" GUI for inspecting data for each PyFlora Pot """

import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot


class InterfaceOpenPot:

    def __init__(self, root):
        self.toplevel_open_pot = tk.Toplevel(root)
        self.toplevel_open_pot.title("PyFlora Pots - " + PyFloraPot.SELECTED_POT)
        self.toplevel_open_pot.geometry('800x400')

        #retrieve pot information and save it into a class property
        self.POT_INFO = self.retrieve_pot_info()
    
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

    def update_current_measures_labels(self):
        self.current_humidity_label.config(text=f"Current humidity:   {self.POT_INFO['current_humidity']}")
        self.current_ph_label.config(text=f"Current PH:   {self.POT_INFO['current_ph']}")
        self.current_salinity_label.config(text=f"Current salinity:   {self.POT_INFO['current_salinity']}")
        self.current_light_label.config(text=f"Current light exposure:   {self.POT_INFO['current_light']}")
        self.current_temperature_label.config(text=f"Current temperature:   {self.POT_INFO['current_temperature']}")
    
    def update_needed_actions(self):
        ''' Checks the latest measures for each pot attribute. If the deviation from optimal value is acceptable, 
            action label is set to checkmark, otherwise a cross'''
        
        # check humidity - accepted deviation +/- 15% 
        humidity_check = '\u2713' if abs(self.POT_INFO['optimal_humidity'] - self.POT_INFO['current_humidity']) < 15 else '\u2717 Water!'
        self.humidity_action_label.config(text=humidity_check)

        # ph - accepted deviation +/- 1,5
        ph_check = '\u2713' if abs(self.POT_INFO['optimal_ph'] - self.POT_INFO['current_ph']) < 1.75 else '\u2717 Add fertilizer!'
        self.ph_action_label.config(text=ph_check)

        # salinity - has to be below limit
        salinitiy_check = '\u2713' if self.POT_INFO['max_salinity'] > self.POT_INFO['current_salinity'] else '\u2717 Change soil!'
        self.salinity_action_label.config(text=salinitiy_check)
        
        # light - accepted deviation +/- 100 PAR
        light_check = '\u2713' if abs(self.POT_INFO['optimal_light'] - self.POT_INFO['current_light']) < 150 else '\u2717 Adjust light!'
        self.light_action_label.config(text=light_check)

        # temperature - accepted deviation +/- 8 degrees
        temperature_check = '\u2713' if abs(self.POT_INFO['optimal_temperature'] - self.POT_INFO['current_temperature']) < 8 else '\u2717 Adjust temperature!'
        self.temperature_action_label.config(text=temperature_check)

    def sync(self):
        syncing_error = PyFloraPot.sync(PyFloraPot, self.POT_INFO['pot_name'], generated=True) # returns an error message if syncing unsucessful
        if syncing_error:
            messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: ' + str(syncing_error)\
                          + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)
        self.POT_INFO = self.retrieve_pot_info()
        self.update_current_measures_labels()
        self.update_needed_actions()

    def complete_actions(self):
        optimizing_error = PyFloraPot.sync(PyFloraPot, self.POT_INFO['pot_name'], generated=False) # returns an error message if syncing unsucessful
        if optimizing_error:
            messagebox.showerror(title='Error while attempting to optimize pot values!',
                    message='Unsuccessful optimization of the pot: ' + str(optimizing_error)\
                          + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)
        self.POT_INFO = self.retrieve_pot_info()
        self.update_current_measures_labels()
        self.update_needed_actions()

    def interface_elements(self):

        # pot basic information
        pot_name_label = tk.Label(self.toplevel_open_pot, text="PyFlora Pot Name:   " + self.POT_INFO['pot_name'])
        pot_name_label.grid(row=1, column=1)

        plant_name_label = tk.Label(self.toplevel_open_pot, text="Plant name:   " + self.POT_INFO['plant_name'])
        plant_name_label.grid(row=2, column=1)

        # humidity
        optimal_humidity_label = tk.Label(self.toplevel_open_pot, text=f"Optimal humidity:   {self.POT_INFO['optimal_humidity']}")
        optimal_humidity_label.grid(row=10, column=1)

        self.current_humidity_label = tk.Label(self.toplevel_open_pot, text=f"Current humidity:   {self.POT_INFO['current_humidity']}")
        self.current_humidity_label.grid(row=10, column=2)

        self.humidity_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.humidity_action_label.grid(row=10, column=3)

        # PH
        optimal_ph_label = tk.Label(self.toplevel_open_pot, text=f"Optimal PH:   {self.POT_INFO['optimal_ph']}")
        optimal_ph_label.grid(row=11, column=1)
        
        self.current_ph_label = tk.Label(self.toplevel_open_pot, text=f"Current PH:   {self.POT_INFO['current_ph']}")
        self.current_ph_label.grid(row=11, column=2)

        self.ph_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.ph_action_label.grid(row=11, column=3)

        # salinity
        optimal_salinity_label = tk.Label(self.toplevel_open_pot, text=f"Salinity celiing:   {self.POT_INFO['max_salinity']}")
        optimal_salinity_label.grid(row=12, column=1)
        
        self.current_salinity_label = tk.Label(self.toplevel_open_pot, text=f"Current salinity:   {self.POT_INFO['current_salinity']}")
        self.current_salinity_label.grid(row=12, column=2)

        self.salinity_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.salinity_action_label.grid(row=12, column=3)

        # light
        optimal_light_label = tk.Label(self.toplevel_open_pot, text=f"Optimal light:   {self.POT_INFO['optimal_light']}")
        optimal_light_label.grid(row=13, column=1)
        
        self.current_light_label = tk.Label(self.toplevel_open_pot, text=f"Current light exposure:   {self.POT_INFO['current_light']}")
        self.current_light_label.grid(row=13, column=2)

        self.light_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.light_action_label.grid(row=13, column=3)

        # temperature
        optimal_temperature_label = tk.Label(self.toplevel_open_pot, text=f"Optimal temperature:   {self.POT_INFO['optimal_temperature']}")
        optimal_temperature_label.grid(row=14, column=1)

        self.current_temperature_label = tk.Label(self.toplevel_open_pot, text=f"Current temperature:   {self.POT_INFO['current_temperature']}")
        self.current_temperature_label.grid(row=14, column=2)

        self.temperature_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.temperature_action_label.grid(row=14, column=3)

        # other
        sync_button = tk.Button(self.toplevel_open_pot, text="Sync only this pot", command=self.sync)
        sync_button.grid(row=999, column=1)

        complete_actions_button = tk.Button(self.toplevel_open_pot, text="Complete recommended actions", command=self.complete_actions)
        complete_actions_button.grid(row=999, column=2)

        delete_button = tk.Button(self.toplevel_open_pot, text="Remove pot...", command=self.delete_pot)
        delete_button.grid(row=1000, column=2)

        back_button = tk.Button(self.toplevel_open_pot, text="Back",
                                command=self.toplevel_open_pot.destroy)
        back_button.grid(row=1000, column=0)