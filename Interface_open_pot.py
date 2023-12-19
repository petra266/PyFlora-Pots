""" GUI for inspecting data for each PyFlora Pot """

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from tkinter import messagebox
from PIL import Image, ImageTk
import os

import sqlite3

import pandas as pd
import matplotlib.pyplot as plt

from PyFlora_class import PyFloraPot

class InterfaceOpenPot:

    def __init__(self, root):
        self.toplevel_open_pot = tk.Toplevel(root)
        self.toplevel_open_pot.title("PyFlora Pots - " + PyFloraPot.SELECTED_POT)
        self.toplevel_open_pot.geometry('1400x800')
        
        self.retrieve_pot_info()

        self.interface_plant_attributes()
        self.interface_image()
        self.interface_functions()
        if PyFloraPot.df['no_measurements'][0] > 0:
            self.update_needed_actions()
            self.visualization_plots()

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
        self.current_ph_label.config(text=f"Current pH:   {self.current_ph}")
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
        self.visualization_plots()

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
        self.visualization_plots()

    def visualization_get_axes(self):
        # create lists of all columns measuring the same attribute
        all_datetime_columns = []
        all_no_measurements = []
        all_humidity_columns = []
        all_ph_columns = []
        all_salinity_columns = []
        all_light_columns = []
        all_temperature_columns = []

        for column in PyFloraPot.df.columns:
            if column.startswith('no_measurement'):
                all_no_measurements.append(column)
            elif column.startswith('humidity'):
                all_humidity_columns.append(column)
            elif column.startswith('ph') and not column.startswith('photo'):
                all_ph_columns.append(column)
            elif column.startswith('salinity'):
                all_salinity_columns.append(column)
            elif column.startswith('light'):
                all_light_columns.append(column)
            elif column.startswith('temperature'):
                all_temperature_columns.append(column)

        # change all datetime measures into a datetime type
        for i in all_datetime_columns:
            PyFloraPot.df[i] = pd.to_datetime(PyFloraPot.df[i])

        # create list of values for all attributes

        humidity_series = PyFloraPot.df[all_humidity_columns]
        humidity_values = humidity_series.values.flatten().tolist()
        humidity_values = [value for value in humidity_values if value is not None]

        ph_series = PyFloraPot.df[all_ph_columns]
        ph_values = ph_series.values.flatten().tolist()
        ph_values = [value for value in ph_values if value is not None]

        salinity_series = PyFloraPot.df[all_salinity_columns]
        salinity_values = salinity_series.values.flatten().tolist()
        salinity_values = [value for value in salinity_values if value is not None]

        light_series = PyFloraPot.df[all_light_columns]
        light_values = light_series.values.flatten().tolist()
        light_values = [value for value in light_values if value is not None]

        temperature_series = PyFloraPot.df[all_temperature_columns]
        temperature_values = temperature_series.values.flatten().tolist()
        temperature_values = [value for value in temperature_values if value is not None]

        # get total number of measurements
        all_no_measurements = [i for i in range(1, len(humidity_values) + 1)]

        all_axes = {
            'all_no_measurements' : all_no_measurements,
            'humidity_values' : humidity_values,
            'ph_values' : ph_values,
            'salinity_values' : salinity_values,
            'light_values' : light_values,
            'temperature_values' : temperature_values
        }

        return all_axes

    def visualization_plots(self):
        self.all_axes = self.visualization_get_axes()

        # remove all plots
        for plot in self.toplevel_open_pot.winfo_children():
            if isinstance(plot, FigureCanvasTkAgg):
                plot.destroy()

        # temperature plot
        self.plot1, self.ax1 = plt.subplots(figsize=(0.2, 0.1))

        self.canvas1 = FigureCanvasTkAgg(self.plot1, master=self.toplevel_open_pot)
        self.canvas1.get_tk_widget().grid(row=1001, column=1, ipadx=170, ipady=140)

        self.ax1.plot(self.all_axes['all_no_measurements'], self.all_axes['temperature_values'], label='Temperature')

        self.ax1.set_xlabel('Number of measurement', fontsize=7.5)
        self.ax1.set_ylabel('Temperature in °C', fontsize=7.5)

        self.ax1.set_title('Temperature Measurements', fontsize=8)
        self.ax1.tick_params(axis='both', which='both', labelsize=6)
        self.ax1.xaxis.set_major_locator(MaxNLocator(integer=True)) 
        self.canvas1.draw()

        # humidity plot
        self.plot2, self.ax2 = plt.subplots(figsize=(0.2, 0.1))

        self.canvas2 = FigureCanvasTkAgg(self.plot2, master=self.toplevel_open_pot)
        self.canvas2.get_tk_widget().grid(row=1001, column=2, ipadx=170, ipady=140)

        self.ax2.bar(self.all_axes['all_no_measurements'], self.all_axes['humidity_values'], label='Humidity')

        self.ax2.set_xlabel('Number of measurement', fontsize=7.5)
        self.ax2.set_ylabel('Humidity in %', fontsize=7.5)

        self.ax2.set_title('Humidity Measurements', fontsize=8)
        self.ax2.tick_params(axis='both', which='both', labelsize=6)
        self.ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.canvas2.draw()


        # salinity plot
        self.plot3, self.ax3 = plt.subplots(figsize=(0.2, 0.1))

        self.canvas3 = FigureCanvasTkAgg(self.plot3, master=self.toplevel_open_pot)
        self.canvas3.get_tk_widget().grid(row=1001, column=3, ipadx=170, ipady=140)

        salinitiy_over_ceiling = 0
        salinity_within_ceiling = 0

        for i in self.all_axes['salinity_values']:
            if i > PyFloraPot.df['max_salinity'][0]:
                salinitiy_over_ceiling += 1
            else:
                salinity_within_ceiling += 1

        salinity_values_groups  = [salinity_within_ceiling, salinitiy_over_ceiling]
        self.ax3.pie(salinity_values_groups)

        self.ax3.pie(salinity_values_groups, 
                     labels=['Salinity \nwithin Ceiling', 'Salinity \nover Ceiling'], 
                     colors=['green', 'darkred'], textprops={'fontsize': 7},
                     autopct='%1.1f%%', startangle=90)

        self.ax3.set_title('Salinity Measurements', fontsize=8)
        self.canvas3.draw()

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
        optimal_ph_label = tk.Label(self.toplevel_open_pot, text=f"Optimal pH:   {PyFloraPot.df['optimal_ph'][0]}")
        optimal_ph_label.grid(row=11, column=1)
        
        self.current_ph_label = tk.Label(self.toplevel_open_pot, text=f"Current pH:   {self.current_ph}")
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
        sync_button.grid(row=999, column=1, columnspan=2, padx=15, pady=15, ipadx=5, ipady=5)

        complete_actions_button = tk.Button(self.toplevel_open_pot, text="Complete recommended actions", command=self.complete_actions)
        complete_actions_button.grid(row=999, column=3, columnspan=2, padx=15, pady=15, ipadx=5, ipady=5)

        delete_button = tk.Button(self.toplevel_open_pot, text="Remove pot...", command=self.delete_pot)
        delete_button.grid(row=0, column=3, columnspan=2, pady=(0,30))

        back_button = tk.Button(self.toplevel_open_pot, text="Back",
                                command=self.toplevel_open_pot.destroy)
        back_button.grid(row=0, column=0, pady=(0,30))