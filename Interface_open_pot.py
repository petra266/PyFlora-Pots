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
                POT_INFO = {              
                    'pot_name': data[1],
                    'plant_name': data[2],
                    'optimal_humidity': data[3],
                    'optimal_ph': data[4],
                    'max_salinity': data[5],
                    'optimal_light': data[6],
                    'optimal_temperature': data[7],
                    'no_measurements': data[8]
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

    def sync(self):
        syncing_error = PyFloraPot.sync(PyFloraPot, self.POT_INFO['pot_name']) # returns an error message if syncing unsucessful
        if syncing_error:
            messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: ' + str(syncing_error) + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)

    def interface_elements(self):
        pot_name_label = tk.Label(self.toplevel_open_pot, text="PyFlora Pot Name:   " + self.POT_INFO['pot_name'])
        pot_name_label.grid(row=1, column=1)

        plant_name_label = tk.Label(self.toplevel_open_pot, text="Plant name:   " + self.POT_INFO['plant_name'])
        plant_name_label.grid(row=2, column=1)

        sync_button = tk.Button(self.toplevel_open_pot, text="Sync only this pot", command=self.sync)
        sync_button.grid(row=3, column=1)

        delete_button = tk.Button(self.toplevel_open_pot, text="Remove pot...", command=self.delete_pot)
        delete_button.grid(row=1000, column=2)

        back_button = tk.Button(self.toplevel_open_pot, text="Back",
                                command=self.toplevel_open_pot.destroy)
        back_button.grid(row=1000, column=0)