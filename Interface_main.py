import os
import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot
from Interface_add_pots import InterfaceAddPots

# os.chdir('PyFlora Pots')

"""
class PyFloraPot:

    count_pots = 0

    def __init__(self, pot_name, plant_name):
        self.pot_name = pot_name
        self.plant_name = plant_name
        PyFloraPot.count_pots += 1

    def update_pot_list(self):
        DB_NAME = 'Database_PyFlora_Pots.db'
        QUERY_GET_ALL_POTS = 'SELECT PyFlora_pot_name, plant_name FROM Database_PyFlora_Pots'

        list_pots = []

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()

                cursor.execute(QUERY_GET_ALL_POTS)
                data = cursor.fetchall()
                for pot in data:
                    pot_class = PyFloraPot(pot[0], pot[1])
                    list_pots.append(pot_class)

                print("All PyFlora Pot names retrived.")
                return list_pots

        except sqlite3.Error as e:
            messagebox.showerror(title='Error in retrieving data',
                                 message='Data retrieving unsucessful. Error: ' + str(e))

"""


class InterfaceMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyFlora Pots")
        self.root.geometry('1200x800')

        PyFloraPot_list = PyFloraPot.update_pot_list(self)

        for i in range(0, PyFloraPot.count_pots):
            button = tk.Button(self.root, text=PyFloraPot_list[i].pot_name)
            button.pack()

        add_button = tk.Button(self.root, text="Add new pot",
                               command=self.launch_InterfaceAddPots)
        add_button.pack()

        exit_button = tk.Button(self.root, text="Quit",
                                command=self.root.destroy)
        exit_button.pack()

    def launch_InterfaceAddPots(self):
        InterfaceAddPots(self.root).toplevel_add_pots.mainloop()


InterfaceMain().root.mainloop()
