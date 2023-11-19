import tkinter as tk
import sqlite3
from tkinter import messagebox


class InterfaceManageLexicon:

    def __init__(self, root):
        self.toplevel_manage_lexicon = tk.Toplevel(root)
        self.toplevel_manage_lexicon.title("Manage PyFlora Lexicon")
        self.toplevel_manage_lexicon.geometry('800x400')

        self.interface_elements()      

    def validate_input(self):
        """Validates all entry values before adding to Lexicon."""
        validation = True

        # try changing all attribute values into integer. Only if that works, check range. 
        try:
            self.plant_name = self.plant_name_input.get()
            self.optimal_humidity = int(self.optimal_humidity_input.get().strip())
            self.optimal_ph = int(self.optimal_ph_input.get().strip())
            self.max_salinity = int(self.max_salinity_input.get().strip())
            self.optimal_light = int(self.optimal_light_input.get().strip())
            self.optimal_temperature = int(self.optimal_temperature_input.get().strip())

            # check a name is chosen 
            if self.plant_name == "":
                validation = False
                messagebox.showwarning(title='No name given!',
                                        message='Please input a name of the plant.', 
                                        parent=self.toplevel_manage_lexicon)
            # check humidity range
            if not self.optimal_humidity in range (0, 101):
                validation = False
                messagebox.showwarning(title='Humidity out of range',
                                    message='Humidity must be an integer between 0 and 100.',
                                    parent=self.toplevel_manage_lexicon)
            # check ph range
            if not self.optimal_ph in range (0, 15):
                validation = False
                messagebox.showwarning(title='PH out of range',
                                    message='PH must be an integer between 0 and 14.',
                                    parent=self.toplevel_manage_lexicon)        
            # check salinity
            if not self.max_salinity >= 0:
                validation = False
                messagebox.showwarning(title='Salinity ceiling out of range',
                                    message='Max salinity must be a positive integer.',
                                    parent=self.toplevel_manage_lexicon)        
            # check light range
            if not self.optimal_light >= 0:
                validation = False
                messagebox.showwarning(title='Light intensity out of range',
                                    message='Light intensity must be a postive integer.',
                                    parent=self.toplevel_manage_lexicon)       
            # check temperature
            if not self.optimal_temperature >= 0:
                validation = False
                messagebox.showwarning(title='Temperature out of range',
                                    message='Temperature must be a postive integer.',
                                    parent=self.toplevel_manage_lexicon)            
        except:
            validation = False
            messagebox.showwarning(title='Non-numerical characters inputed',
                                message="Only numerical characters are allowed in the \
                                    atrribute value fields. This includes symbols as: - , . !", 
                                parent=self.toplevel_manage_lexicon)    
        # return validation result
        return validation

    def add_plant(self):
        """Button function - adds a new plant to Database_plants_lexicon if validated."""
        # activate validation function
        validation = self.validate_input()
        # insert the new plant into Database_plants_lexicon
        if validation:
            DB_NAME = 'Database_plants_lexicon.db'

            QUERY_INSERT = '''
            INSERT INTO Database_plants_lexicon 
            (plant_name, optimal_humidity, 
            optimal_ph, max_salinity, optimal_light, optimal_temperature)
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            VALUES_LIST = [
                self.plant_name, self.optimal_humidity, self.optimal_ph, 
                self.max_salinity, self.optimal_light, self.optimal_temperature
                ]

            try:
                sqlite_connection = sqlite3.connect(DB_NAME)
                cursor = sqlite_connection.cursor()
                cursor.execute(QUERY_INSERT, VALUES_LIST)
                sqlite_connection.commit()
                print("New plant sucessfully added.")

            except sqlite3.Error as e:
                print("Execution unsuccessful. Error when creating the database: ", e)
                messagebox.showwarning(title='Adding the new plant unsuccessful!',
                                        message=f'Error when adding the new plant to the lexicon: {e}', 
                                        parent=self.toplevel_manage_lexicon)
                SystemExit(1)


            # Close the connection to the database
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("SQLite connection closed.")
    def interface_elements(self):
      # Define interface variables
      self.plant_name_input = tk.StringVar()
      self.optimal_humidity_input = tk.StringVar()
      self.optimal_ph_input = tk.StringVar()
      self.max_salinity_input = tk.StringVar()
      self.optimal_light_input = tk.StringVar()
      self.optimal_temperature_input = tk.StringVar()

      # plant name
      name_label = tk.Label(self.toplevel_manage_lexicon, text='Name: ')
      name_label.grid(row=1, column=1)

      name_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.plant_name_input)
      name_entry.grid(row=1, column=2)

      # humidity
      optimal_humidity_label = tk.Label(self.toplevel_manage_lexicon, text='Optimal humidity: ')
      optimal_humidity_label.grid(row=2, column=1)

      optimal_humidity_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.optimal_humidity_input)
      optimal_humidity_entry.grid(row=2, column=2)

      humidity_unit_label = tk.Label(self.toplevel_manage_lexicon, text='%')
      humidity_unit_label.grid(row=2, column=3)

      # ph
      optimal_ph_label = tk.Label(self.toplevel_manage_lexicon, text='Optimal PH: ')
      optimal_ph_label.grid(row=3, column=1)

      optimal_ph_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.optimal_ph_input)
      optimal_ph_entry.grid(row=3, column=2)

      ph_unit_label = tk.Label(self.toplevel_manage_lexicon, text='pH')
      ph_unit_label.grid(row=3, column=3)

      # salinity
      max_salinity_label = tk.Label(self.toplevel_manage_lexicon, text='Max salinity allowed: ')
      max_salinity_label.grid(row=4, column=1)

      max_salinity_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.max_salinity_input)
      max_salinity_entry.grid(row=4, column=2)

      salinity_unit_label = tk.Label(self.toplevel_manage_lexicon, text='dS/m')
      salinity_unit_label.grid(row=4, column=3)

      # light
      optimal_light_label = tk.Label(self.toplevel_manage_lexicon, text='Optimal light intensity: ')
      optimal_light_label.grid(row=5, column=1)

      optimal_light_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.optimal_light_input)
      optimal_light_entry.grid(row=5, column=2)

      light_unit_label = tk.Label(self.toplevel_manage_lexicon, text='µmol/m²/s')
      light_unit_label.grid(row=5, column=3)

      # temperature
      optimal_temperature_label = tk.Label(self.toplevel_manage_lexicon, text='Optimal temperature: ')
      optimal_temperature_label.grid(row=6, column=1)

      optimal_temperature_entry = tk.Entry(self.toplevel_manage_lexicon, textvariable=self.optimal_temperature_input)
      optimal_temperature_entry.grid(row=6, column=2)

      temperature_unit_label = tk.Label(self.toplevel_manage_lexicon, text='°C')
      temperature_unit_label.grid(row=6, column=3)

      # other
      add_plant_button = tk.Button(self.toplevel_manage_lexicon, text="Add plant", command=self.add_plant) 
      add_plant_button.grid(row=999, column=1)

      back_button = tk.Button(self.toplevel_manage_lexicon, text="Back", command=self.toplevel_manage_lexicon.destroy)
      back_button.grid(row=1000, column=1, columnspan=2)