import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


class InterfaceManageLexicon:

    def __init__(self, root):
        self.toplevel_manage_lexicon = tk.Toplevel(root)
        self.toplevel_manage_lexicon.title("Manage PyFlora Lexicon")
        self.toplevel_manage_lexicon.geometry('800x400')

        self.interface_attributes()     
        self.interface_image()
        self.interface_functions() 

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
        
        # save the plant image to the Images folder and get it's path
        if validation:
            self.photo_path = self.save_image()
            self.photo = self.convert_image_to_blob(self.photo_path)

        
        # insert the new plant into Database_plants_lexicon
        if validation:
            DB_NAME = 'Database_plants_lexicon.db'

            QUERY_INSERT = '''
            INSERT INTO Database_plants_lexicon 
            (plant_name, optimal_humidity, 
            optimal_ph, max_salinity, optimal_light, optimal_temperature, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''

            VALUES_LIST = [
                self.plant_name, self.optimal_humidity, self.optimal_ph, self.max_salinity, 
                self.optimal_light, self.optimal_temperature, self.photo
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
                                        message=f'Error when adding the new plant to the lexicon: {e}.\
                                                Try again or restart the application.', 
                                        parent=self.toplevel_manage_lexicon)
                self.toplevel_manage_lexicon.destroy()  

            # Close the connection to the database
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("SQLite connection closed.")

            for widget in self.toplevel_manage_lexicon.winfo_children():
                widget.destroy()
            self.interface_attributes()
            self.interface_image()
            self.interface_functions()
            
    def erase_plant(self):
        ''' Deletes selected plant from the lexicon and PyFlora pots if plant selected'''
        
        if self.plant_to_erase.get() != self.DEFAULT_PLANT:
           
           # delete from the lexicon
            DB_NAME = 'Database_plants_lexicon.db'
            QUERY_DELETE_PLANT = 'DELETE FROM Database_plants_lexicon WHERE plant_name = '

            try:
                with sqlite3.connect(DB_NAME) as sql_connection:
                    cursor = sql_connection.cursor()
                    cursor.execute(QUERY_DELETE_PLANT + '"{}"'.format(self.plant_to_erase.get()))
                    print("Plant successfully removed from the lexicon.")   

                # delete from PyFlora Pots all pots containing erased plant
                DB_NAME = 'Database_PyFlora_Pots.db'
                QUERY_DELETE_POT = 'DELETE FROM Database_PyFlora_Pots WHERE plant_name = '

                try:
                    with sqlite3.connect(DB_NAME) as sql_connection:
                        cursor = sql_connection.cursor()
                        cursor.execute(QUERY_DELETE_POT + '"{}"'.format(self.plant_to_erase.get()))
                        print("PyFlora Pots successfully deleted.")
                        messagebox.showinfo(title='Plant information erased!',
                                        message=f'You have successfully erased "{self.plant_to_erase.get()}"\
                                            from the PyFlora Lexicon. All PyFlora pots containing this plant have been unplanted.',
                                        parent=self.toplevel_manage_lexicon)  

                except sqlite3.Error as e:
                    print('Data retrieving unsucessful. Error: ', e)
                    messagebox.showerror(title='Error in retrieving data!',
                                        message='Data retrieving unsucessful. Error: ' + str(e) + "\nPlease restart the application",
                                        parent=self.toplevel_manage_lexicon) 
                

            except sqlite3.Error as e:
                print('Data retrieving unsucessful. Error: ', e)
                messagebox.showerror(title='Error in retrieving data!',
                                    message='Data retrieving unsucessful. Error: ' + str(e) + "\nPlease restart the application",
                                    parent=self.toplevel_manage_lexicon)
                self.toplevel_manage_lexicon.destroy()  
            
            for widget in self.toplevel_manage_lexicon.winfo_children():
                widget.destroy()

            self.interface_attributes()     
            self.interface_image()
            self.interface_functions()         

    def choose_image(self):
        
        self.image_path = filedialog.askopenfilename(parent=self.toplevel_manage_lexicon)
        original_image = Image.open(self.image_path)
        self.resized_image = original_image.resize((100, 100))
        original_image.close()

        self.show_image = ImageTk.PhotoImage(self.resized_image)
        self.test_label = tk.Label(self.toplevel_manage_lexicon, image=self.show_image)
        self.test_label.grid(row=7, rowspan=3, column=1)

    def save_image(self):
        ''' Saves the chosen image to Images folder '''

        image_to_save = Image.open(self.image_path)
        path_to_save = f'Images\{self.plant_name}.jpg'
        print(path_to_save)

        image_to_save.save(path_to_save)
        image_to_save.close()

        return path_to_save

    def convert_image_to_blob(self, image_path):
        with open(image_path, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def interface_attributes(self):
    
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
        optimal_ph_label = tk.Label(self.toplevel_manage_lexicon, text='Optimal pH: ')
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

    def interface_image(self):

        # add image
        choose_image_button = tk.Button(self.toplevel_manage_lexicon, text="Choose image", command=self.choose_image)
        choose_image_button.grid(row=7, column=2)
    
    def interface_functions(self):

        self.plant_to_erase = tk.StringVar()
        self.DEFAULT_PLANT = "Choose a plant to erase:"
        self.plant_to_erase.set(self.DEFAULT_PLANT)

        all_known_plant_names = self.get_all_known_plant_names()

        # add plant
        add_plant_button = tk.Button(self.toplevel_manage_lexicon, text="Add plant", command=self.add_plant) 
        add_plant_button.grid(row=20, column=2)

        # remove plant 
        remove_label = tk.Label(self.toplevel_manage_lexicon,
                               text="Choose a plant to erase: ")
        remove_label.grid(row=50, column=1)

        self.plant_menu = tk.OptionMenu(
            self.toplevel_manage_lexicon, self.plant_to_erase, *all_known_plant_names)
        self.plant_menu.grid(row=50, column=2)

        erase_plant_button = tk.Button(self.toplevel_manage_lexicon, text="Erase plant!", command=self.erase_plant) 
        erase_plant_button.grid(row=50, column=3)        

        back_button = tk.Button(self.toplevel_manage_lexicon, text="Back", command=self.toplevel_manage_lexicon.destroy)
        back_button.grid(row=1000, column=1, columnspan=2)