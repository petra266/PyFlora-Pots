import os
import tkinter as tk
import sqlite3

os.chdir('PyFlora Pots')

root = tk.Tk()
root.title("PyFlora Pots")


class PyFloraPot:

    PyFloraPots_count = 0

    def __init__(self, pot_name, plant_name):
        self.pot_name = pot_name
        self.plant_name = plant_name
        PyFloraPot.PyFloraPots_count += 1


def update_pot_list():
    DB_NAME = 'Database_PyFlora_Pots.db'
    QUERY_GET_ALL_POTS = 'SELECT PyFlora_pot_name, plant_name FROM Database_PyFlora_Pots'

    PyFloraPot_list = []

    try:
        with sqlite3.connect(DB_NAME) as sql_connection:
            cursor = sql_connection.cursor()

            cursor.execute(QUERY_GET_ALL_POTS)
            data = cursor.fetchall()
            for pot in data:
                pot_class = PyFloraPot(pot[0], pot[1])
                PyFloraPot_list.append(pot_class)

            print("All PyFlora Pot names retrived.")
            return PyFloraPot_list

    except sqlite3.Error as e:
        print('Data retrieving unsucessful. Error: ', e)


# nr_pots = len(PyFlora_pots_names)
row = 1
column = 1


def add_new_pot():
    if column % 2 == 0:
        column = 1
        row += 1
    else:
        column = 2

    button = tk.Button(root, text="New button")


exit_button = tk.Button(root, text="Quit", command=root.destroy)

root.mainloop()
