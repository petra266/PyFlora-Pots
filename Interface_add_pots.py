""" GUI for adding new PyFlora Pots """

import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot


class InterfaceAddPots:

    def __init__(self, root):
        self.toplevel_add_pots = tk.Toplevel(root)
        self.toplevel_add_pots.title("PyFlora Pots - Let's plant!")
        self.toplevel_add_pots.geometry('1200x800')
        self.interface_elements()

    def get_all_known_plant_names(self):
        """Returns the list of all plant names available in the lexicon."""

        DB_NAME = 'Database_plants_lexicon.db'
        QUERY_GET_ALL_KNOWN_PLANT_NAMES = 'SELECT plant_name FROM Database_plants_lexicon'

        ALL_KNOWN_PLANT_NAMES = []

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()

                cursor.execute(QUERY_GET_ALL_KNOWN_PLANT_NAMES)
                data = cursor.fetchall()
                for plant_name in data:
                    ALL_KNOWN_PLANT_NAMES.append(plant_name[0])

                print("All plant names retrived.")
                return ALL_KNOWN_PLANT_NAMES

        except sqlite3.Error as e:
            print('Data retrieving unsucessful. Error: ', e)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' +
                                 str(e) + "\nPlease restart the application.",
                                 parent=self.toplevel_add_pots)
            self.toplevel_add_pots.destroy()

    def validate_choices(self):
        """Validates choices when creating a new PyFlora pot."""
        # validate the chosen pot_name is available
        validation = True
        ALL_POT_NAMES = list(PyFloraPot.df['pot_name'])

        if len(ALL_POT_NAMES) > 0:
            for i in range(0, len(ALL_POT_NAMES)):
                if self.new_pot.get() == ALL_POT_NAMES[i]:
                    validation = False
                    messagebox.showwarning(title='PyFlora pot already in use!',
                                        message='Please choose another name for the PyFlora pot.',
                                        parent=self.toplevel_add_pots)
                if self.new_pot.get() == "":
                    validation = False
                    messagebox.showwarning(title='No name given!',
                                        message='Please choose a name for the PyFlora pot.',
                                        parent=self.toplevel_add_pots)
        # check a plant is chosen from the menu
        if self.chosen_plant.get() == self.DEFAULT_PLANT:
            validation = False
            messagebox.showwarning(title='No plant chosen!',
                                   message='Please choose a plant from the plant menu.\n\nNote: If the plant you have in mind is not on the list, add it to the plant lexicon.',
                                   parent=self.toplevel_add_pots)
        # return validation result
        if validation == False:
            return False
        else:
            return True

    def add_new_pot(self):
        """Button function - adds a new PyFlora pot to Database_PlyFlora_Pots."""

        # activate validation function
        validation = self.validate_choices()

        # retrieve data on the selected plant from the lexicon
        if validation:
            DB_NAME = 'Database_plants_lexicon.db'
            QUERY_GET_CHOSEN_PLANT = 'SELECT * FROM Database_plants_lexicon where plant_name ='

            try:
                with sqlite3.connect(DB_NAME) as sql_connection:
                    cursor = sql_connection.cursor()

                    cursor.execute(QUERY_GET_CHOSEN_PLANT +
                                   '"{}"'.format(self.chosen_plant.get()))
                    data = cursor.fetchall()

            except sqlite3.Error as e:
                print('Data retrieving unsucessful. Error: ', e)
                messagebox.showerror(title='Error in retrieving data!',
                                     message='Data retrieving unsucessful. Error: ' +
                                     str(e) +
                                     "\n\nPlease restart the application.",
                                     parent=self.toplevel_add_pots)
                self.toplevel_add_pots.destroy()

            # insert the new pot into Database_PyFlora_Pots

            DB_NAME = 'Database_PyFlora_Pots.db'

            QUERY_INSERT_POT = '''
            INSERT INTO Database_PyFlora_Pots (pot_name,
                plant_name, optimal_humidity, optimal_ph,
                max_salinity, optimal_light, optimal_temperature, photo, no_measurements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            new_pot = (self.new_pot.get(
            ), data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], 0)

            try:
                with sqlite3.connect(DB_NAME) as sql_connection:
                    cursor = sql_connection.cursor()
                    query = QUERY_INSERT_POT
                    cursor.execute(query, new_pot)
                    sql_connection.commit()
                    print("Successfully inserted into the database.")

            except sqlite3.Error as e:
                print('Inserting new pot unsuccessful. Error: ', e)
                messagebox.showerror(title='Error while adding a new PyFlora Pot!',
                                     message='New PyFlora Pot not added due to error: ' +
                                     str(e) + "\n\nPlease try again or restart the application.",
                                     parent=self.toplevel_add_pots)
            self.toplevel_add_pots.destroy()

    def interface_elements(self):

        # Define interface variables

        self.new_pot = tk.StringVar()

        self.chosen_plant = tk.StringVar()
        self.DEFAULT_PLANT = "Choose a plant from the list:"
        self.chosen_plant.set(self.DEFAULT_PLANT)

        all_known_plant_names = self.get_all_known_plant_names()

        # Define interface elements

        pot_name_label = tk.Label(
            self.toplevel_add_pots, text="Give this pot a name:")
        pot_name_label.grid(row=1, column=1)

        entry_pot_name = tk.Entry(
            self.toplevel_add_pots, textvariable=self.new_pot)
        entry_pot_name.grid(row=1, column=2)

        plant_label = tk.Label(self.toplevel_add_pots,
                               text="Choose a plant to plant:")
        plant_label.grid(row=2, column=1)

        plant_menu = tk.OptionMenu(
            self.toplevel_add_pots, self.chosen_plant, *all_known_plant_names)
        plant_menu.grid(row=2, column=2)

        add_pot_button = tk.Button(
            self.toplevel_add_pots, text="Let's plant!!", command=self.add_new_pot)
        add_pot_button.grid(row=3, columnspan=3)

        back_button = tk.Button(self.toplevel_add_pots, text="Back",
                                command=self.toplevel_add_pots.destroy)
        back_button.grid(row=1000, columnspan=3)
