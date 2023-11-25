""" GUI for inspecting data for each PyFlora Pot """

import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

from PyFlora_class import PyFloraPot
from Data_visualization import *


class InterfaceOpenPot:

    def __init__(self, root):
        self.toplevel_open_pot = tk.Toplevel(root)
        self.toplevel_open_pot.title("PyFlora Pots - " + PyFloraPot.SELECTED_POT)
        self.toplevel_open_pot.geometry('800x400')
        
        # retrieve pot information as dataframe self.df
        
        self.retrieve_pot_info()

        self.interface_plant_attributes()
        self.interface_image()
        self.interface_functions()
        if PyFloraPot.df['no_measurements'][0] > 0:
            self.complete_actions()
        #self.data_visualization()

    def retrieve_pot_info(self):
        """ Retrieve all data from the Database_PyFlora_Pots and return it as a dictionary"""
        df_success, df_error = PyFloraPot.get_dataframe_for_opened_pot(PyFloraPot, PyFloraPot.SELECTED_POT)
       
        if not df_success:
            print('Data retrieving unsucessful. Error: ', df_error)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' + str(df_error) + "\nPlease restart the application",
                                 parent=self.toplevel_open_pot)
            self.toplevel_open_pot.destroy()   
        else:
            print('Data retrieving sucessful.')
            self.no_measurements = PyFloraPot.df['no_measurements'][0]
            if self.no_measurements == 0:
                self.current_humidity = '-'
                self.current_ph = '-'
                self.current_salinity = '-'
                self.current_light = '-'
                self.current_temperature = '-'
            else:
                self.current_humidity = PyFloraPot.df[f'humidity{self.no_measurements}'][0]
                self.current_ph = PyFloraPot.df[f'ph{self.no_measurements}'][0]
                self.current_salinity = PyFloraPot.df[f'salinity{self.no_measurements}'][0]
                self.current_light = PyFloraPot.df[f'light{self.no_measurements}'][0]
                self.current_temperature = PyFloraPot.df[f'temperature{self.no_measurements}'][0]

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

    def update_current_measurements_labels(self):
        self.current_humidity_label.config(text=f"Current humidity:   {self.current_humidity}")
        self.current_ph_label.config(text=f"Current PH:   {self.current_ph}")
        self.current_salinity_label.config(text=f"Current salinity:   {self.current_salinity}")
        self.current_light_label.config(text=f"Current light exposure:   {self.current_light}")
        self.current_temperature_label.config(text=f"Current temperature:   {self.current_temperature}")
    
    def update_needed_actions(self):
        ''' Checks the latest measures for each pot attribute. If the deviation from optimal value is acceptable, 
            action label is set to checkmark, otherwise a cross'''
        
        # check humidity - accepted deviation +/- 15% 
        humidity_check = '\u2713' if abs(PyFloraPot.df['optimal_humidity'][0] - self.current_humidity) < 15 else '\u2717 Water!'
        self.humidity_action_label.config(text=humidity_check)

        # ph - accepted deviation +/- 1,5
        ph_check = '\u2713' if abs(PyFloraPot.df['optimal_ph'][0] - self.current_ph) < 1.75 else '\u2717 Add fertilizer!'
        self.ph_action_label.config(text=ph_check)

        # salinity - has to be below limit
        salinitiy_check = '\u2713' if PyFloraPot.df['max_salinity'][0] > self.current_salinity else '\u2717 Change soil!'
        self.salinity_action_label.config(text=salinitiy_check)
        
        # light - accepted deviation +/- 100 PAR
        light_check = '\u2713' if abs(PyFloraPot.df['optimal_light'][0] - self.current_light) < 150 else '\u2717 Adjust light!'
        self.light_action_label.config(text=light_check)

        # temperature - accepted deviation +/- 8 degrees
        temperature_check = '\u2713' if abs(PyFloraPot.df['optimal_temperature'][0] - self.current_temperature) < 8 else '\u2717 Adjust temperature!'
        self.temperature_action_label.config(text=temperature_check)

    def sync(self):
        syncing_success = PyFloraPot.sync(PyFloraPot, PyFloraPot.df['pot_name'][0], generated=True) # returns an error message if syncing unsucessful
        if not syncing_success:
            messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: '\
                          + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)
        self.retrieve_pot_info()
        self.update_current_measurements_labels()
        self.update_needed_actions()

    def complete_actions(self):
        optimizing_success = PyFloraPot.sync(PyFloraPot, PyFloraPot.df['pot_name'][0], generated=False) # returns an error message if syncing unsucessful
        if not optimizing_success:
            messagebox.showerror(title='Error while attempting to optimize pot values!',
                    message='Unsuccessful optimization of the pot: ' + str(optimizing_error)\
                          + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)
        self.retrieve_pot_info()
        self.update_current_measurements_labels()
        self.update_needed_actions()

    def interface_plant_attributes(self):

        # pot basic information
        pot_name_label = tk.Label(self.toplevel_open_pot, text=f"PyFlora Pot Name:   {PyFloraPot.df['pot_name'][0]}")
        pot_name_label.grid(row=1, column=2)

        plant_name_label = tk.Label(self.toplevel_open_pot, text=f"Plant name:   {PyFloraPot.df['plant_name'][0]}")
        plant_name_label.grid(row=2, column=2)

        # humidity
        optimal_humidity_label = tk.Label(self.toplevel_open_pot, text=f"Optimal humidity:   {PyFloraPot.df['optimal_humidity'][0]}")
        optimal_humidity_label.grid(row=10, column=1)

        self.current_humidity_label = tk.Label(self.toplevel_open_pot, text=f"Current humidity:   {self.current_humidity}")
        self.current_humidity_label.grid(row=10, column=2)

        self.humidity_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.humidity_action_label.grid(row=10, column=3)

        # PH
        optimal_ph_label = tk.Label(self.toplevel_open_pot, text=f"Optimal PH:   {PyFloraPot.df['optimal_ph'][0]}")
        optimal_ph_label.grid(row=11, column=1)
        
        self.current_ph_label = tk.Label(self.toplevel_open_pot, text=f"Current PH:   {self.current_ph}")
        self.current_ph_label.grid(row=11, column=2)

        self.ph_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.ph_action_label.grid(row=11, column=3)

        # salinity
        optimal_salinity_label = tk.Label(self.toplevel_open_pot, text=f"Salinity celiing:   {PyFloraPot.df['max_salinity'][0]}")
        optimal_salinity_label.grid(row=12, column=1)
        
        self.current_salinity_label = tk.Label(self.toplevel_open_pot, text=f"Current salinity:   {self.current_salinity}")
        self.current_salinity_label.grid(row=12, column=2)

        self.salinity_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.salinity_action_label.grid(row=12, column=3)

        # light
        optimal_light_label = tk.Label(self.toplevel_open_pot, text=f"Optimal light:   {PyFloraPot.df['optimal_light'][0]}")
        optimal_light_label.grid(row=13, column=1)
        
        self.current_light_label = tk.Label(self.toplevel_open_pot, text=f"Current light exposure:   {self.current_light}")
        self.current_light_label.grid(row=13, column=2)

        self.light_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.light_action_label.grid(row=13, column=3)

        # temperature
        optimal_temperature_label = tk.Label(self.toplevel_open_pot, text=f"Optimal temperature:   {PyFloraPot.df['optimal_temperature'][0]}")
        optimal_temperature_label.grid(row=14, column=1)

        self.current_temperature_label = tk.Label(self.toplevel_open_pot, text=f"Current temperature:   {self.current_temperature}")
        self.current_temperature_label.grid(row=14, column=2)

        self.temperature_action_label = tk.Label(self.toplevel_open_pot, text='-')
        self.temperature_action_label.grid(row=14, column=3)

    def interface_image(self):
        
        image_path = (f"Images\{PyFloraPot.df['plant_name'][0]}.jpg")
        original_image = Image.open(image_path)
        resized_image = original_image.resize((100, 100))

        self.photo = ImageTk.PhotoImage(resized_image)
        self.test_label = tk.Label(self.toplevel_open_pot, image=self.photo)
        self.test_label.grid(row=1, rowspan=3, column=1)

    def interface_functions(self):
        sync_button = tk.Button(self.toplevel_open_pot, text="Sync only this pot", command=self.sync)
        sync_button.grid(row=999, column=1)

        complete_actions_button = tk.Button(self.toplevel_open_pot, text="Complete recommended actions", command=self.complete_actions)
        complete_actions_button.grid(row=999, column=2)

        delete_button = tk.Button(self.toplevel_open_pot, text="Remove pot...", command=self.delete_pot)
        delete_button.grid(row=1000, column=2)

        back_button = tk.Button(self.toplevel_open_pot, text="Back",
                                command=self.toplevel_open_pot.destroy)
        back_button.grid(row=1000, column=0)