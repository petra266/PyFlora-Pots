import os
import tkinter as tk
import sqlite3
from tkinter import messagebox


class PyFloraPot:

    count_pots = 0

    def __init__(self, pot_name, plant_name):
        self.pot_name = pot_name
        self.plant_name = plant_name
        PyFloraPot.count_pots += 1
        PyFloraPot.list_pots = []

    def update_pot_list(self):
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_ALL_POTS = 'SELECT PyFlora_pot_name, plant_name FROM Database_PyFlora_Pots'

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()

                cursor.execute(QUERY_GET_ALL_POTS)
                data = cursor.fetchall()
                for pot in data:
                    pot_class = PyFloraPot(pot[0], pot[1])
                    PyFloraPot.list_pots.append(pot_class)

                print("All PyFlora Pot names retrived.")
                return PyFloraPot.list_pots

        except sqlite3.Error as e:
            messagebox.showerror(title='Error in retrieving data',
                                 message='Data retrieving unsucessful. Error: ' + str(e))
