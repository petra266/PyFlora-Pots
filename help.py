"""
broj = 1

test = broj % 2
print(test)
"""


import os
import sqlite3

os.chdir('PyFlora Pots')


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


PyFloraPot_list = update_pot_list()
print(PyFloraPot_list)
# print(PyFloraPot_list[0].pot_name)
print(PyFloraPot.PyFloraPots_count)
