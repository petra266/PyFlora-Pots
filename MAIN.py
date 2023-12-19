import tkinter as tk
from datetime import datetime, time

import Database_creating_plants_lexicon
import Database_creating_users
import Database_creating_PyFlora_Pots

from PyFlora_class import PyFloraPot

from Interface_add_pots import *
from Interface_open_pot import *
from Interface_user_account import *
from Interface_manage_lexicon import *

class InterfaceLogin:
    def __init__(self):
        self.root_login = tk.Tk()
        self.root_login.title('PyFlora Pots Login')
        self.root_login.geometry('250x150')

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.interface()

    def login(self):
        DB_NAME = 'Database_users.db'
        QUERY_GET_PASSWORD = 'SELECT password, firstname FROM Database_users WHERE username ='
        NOON = time(12, 0)
        EVENING = time(18, 0)
        
        now = datetime.now()
        now_time = time(now.hour, now.minute)
        success = False
        name = None
        try:
            sqlite_connection = sqlite3.connect(DB_NAME)
            cursor = sqlite_connection.cursor()
            query = QUERY_GET_PASSWORD + '"{}"'.format(self.username.get())
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                password_input = records[0][0]
                name = records[0][1]
                if password_input == self.password.get():
                    success = True
                else:
                    succes = False
            else:
                success = False
            cursor.close()
        except sqlite3.Error as e:
            print(e)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

        if success:
            if now_time < NOON:
                greeting = 'Good morning'
            elif now_time < EVENING:
                greeting = 'Good day'
            else:
                greeting = 'Good evening'
            message = '{}, {}!'.format(greeting, name)
            messagebox.showinfo(title='Welcome to PyFlora Pots!', message=message)
            self.root_login.destroy()
            InterfaceMain().root.mainloop()

        else:
            message = 'Login credentials are incorrect.'
            messagebox.showerror(title='Unsuccesssful login', message=message)

    def interface(self):
        username_label = tk.Label(self.root_login, text='Username: ')
        username_label.grid(row=0, column=0, padx=(30,0), pady=(10,30))

        username_entry = tk.Entry(self.root_login, textvariable=self.username)
        username_entry.grid(row=0, column=1, pady=(10,30))

        password_label = tk.Label(self.root_login, text='Password: ')
        password_label.grid(row=1, column=0, padx=(30,0), pady=(0,15))

        password_entry = tk.Entry(self.root_login, textvariable=self.password,
                                show='*')
        password_entry.grid(row=1, column=1, pady=(0,15))

        start_button = tk.Button(self.root_login, text='Login', command=self.login)
        start_button.grid(row=2, columnspan=3, pady=5, ipadx=5, ipady=5)

        exit_button = tk.Button(
            self.root_login, text='Exit', command=self.root_login.destroy)
        exit_button.grid(row=3, columnspan=3, pady=5, ipadx=5, ipady=5)

        self.root_login.bind('<Return>', self.login)

class InterfaceMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('PyFlora Pots')
        self.root.geometry('510x650')

        self.create_buttons()

    def retrieve_data(self):
        df_success, df_error = PyFloraPot.get_dataframe_for_all_pots(PyFloraPot)

        if not df_success:
            print('Data retrieving unsucessful. Error: ', df_error)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' + str(df_error) + "\nPlease restart the application",
                                 parent=self.root)
    
    def create_buttons(self):        

        self.retrieve_data()

        # remove buttons and labels
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Button, tk.Label)):
                widget.destroy()

        # Header and settings - top_space, header to be used for button.grid calculations
        HEADER = 5
        
        logout_button = tk.Button(self.root, text="Log Out",
                                command=self.logout)
        logout_button.grid(row=0, column=1, pady=(0, 30), ipadx=5, ipady=5)

        lexicon_button = tk.Button(self.root, text='Manage Lexicon',
                            command=self.launch_InterfaceManageLexicon)
        lexicon_button.grid(row=0, column=3, pady=(0, 30), ipadx=5, ipady=5)

        account_button = tk.Button(self.root, text="User Account",
                            command=self.launch_InterfaceUserAccount)
        account_button.grid(row=0, column=4, pady=(0, 30), ipadx=5, ipady=5)

        # Defining and arranging buttons for each PyFlora pot
        
        image_list = []

        if len(PyFloraPot.df.index) > 0:
            for i in range(0, len(PyFloraPot.df.index)):

                if i % 2 == 0:
                    button_row = i + 1 + HEADER
                    button_column = 1
                else: 
                    button_row = i + HEADER
                    button_column = 3

                pot_name = PyFloraPot.df.loc[i, 'pot_name']
                current_measurement = PyFloraPot.df.loc[i, 'no_measurements']
                attention_needed = ''
                                
                if current_measurement > 0 :
                    
                    # check humidity - accepted deviation +/- 15% 
                    if abs(PyFloraPot.df.loc[i, 'optimal_humidity'] - PyFloraPot.df.loc[i, f'humidity{current_measurement}']) >= 15:
                        attention_needed = 'Attention needed!'

                    # ph - accepted deviation +/- 1,5
                    if abs(PyFloraPot.df.loc[i, 'optimal_ph'] - PyFloraPot.df.loc[i, f'ph{current_measurement}']) >= 1.75:
                        attention_needed = 'Attention needed!'

                    # salinity - has to be below limit
                    if (PyFloraPot.df.loc[i, 'max_salinity'] < PyFloraPot.df.loc[i, f'salinity{current_measurement}']):
                        attention_needed = 'Attention needed!'
                    
                    # light - accepted deviation +/- 100 PAR
                    if abs(PyFloraPot.df.loc[i, 'optimal_light'] - PyFloraPot.df.loc[i, f'light{current_measurement}']) > 150:
                        attention_needed = 'Attention needed!'

                    # temperature - accepted deviation +/- 8 degrees
                    if abs(PyFloraPot.df.loc[i, 'optimal_temperature'] - PyFloraPot.df.loc[i, f'temperature{current_measurement}']) > 8:
                        attention_needed = 'Attention needed!'


                # show image
                image_path = (f"Images\{PyFloraPot.df.loc[i, 'plant_name']}.jpg")
                original_image = Image.open(image_path)
                resized_image = original_image.resize((100, 100))

                image_list.append(ImageTk.PhotoImage(resized_image))
                photo_label = tk.Label(self.root, image=image_list[-1])
                photo_label.image = image_list[-1]
                photo_label.grid(row=button_row, rowspan=2, column=button_column, padx=(15, 0), ipadx=10, ipady=10)

                # show button
                button = tk.Button(self.root, text=pot_name, command=lambda selected_name=pot_name: self.launch_InterfaceOpenPot(selected_name))
                button.grid(row=button_row, column=button_column + 1, ipadx=10, ipady=10)

                # show action
                attention_label = tk.Label(self.root, text=attention_needed)
                attention_label.grid(row=button_row + 1, column=button_column + 1)
            
        elif len(PyFloraPot.df.index) == 0:
            button_row = 1
            button_column = 1
        
        # Other buttons
        add_button = tk.Button(self.root, text="Add new pot",
                            command=self.launch_InterfaceAddPots)
        add_button.grid(row=button_row + 1 + HEADER, column=1, columnspan=2, pady=30, ipadx=10, ipady=10)

        sync_button = tk.Button(self.root, text="Sync all pots", command=self.sync)
        sync_button.grid(row=button_row + 2 + HEADER, column=1, columnspan=4, pady=30, ipadx=10, ipady=10)

    def logout(self):
        self.root.destroy()
        InterfaceLogin().root_login.mainloop()

    def launch_InterfaceUserAccount(self):
        InterfaceUserAccount(self.root)
    
    def launch_InterfaceAddPots(self):
        interface_add_pots = InterfaceAddPots(self.root)
        self.root.wait_window(interface_add_pots.toplevel_add_pots)
        self.create_buttons()

    def launch_InterfaceOpenPot(self, selected_name):
        # note the selected pot in the PyFloraPot class
        PyFloraPot.SELECTED_POT = selected_name
        
        interface_open_pot = InterfaceOpenPot(self.root)
        self.root.wait_window(interface_open_pot.toplevel_open_pot)
        self.create_buttons()

    def launch_InterfaceManageLexicon(self):
        interface_manage_lexicon = InterfaceManageLexicon(self.root)
        self.root.wait_window(interface_manage_lexicon.toplevel_manage_lexicon)
        self.create_buttons()

    def sync(self):
        all_pot_names = list(PyFloraPot.df['pot_name'])
        syncing_success, syncing_error = PyFloraPot.sync(PyFloraPot, all_pot_names, generated=True) # returns an error message if syncing unsucessful
        if not syncing_success:
            messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: ' + str(syncing_error) + "\n\nPlease try again or restart the application.",
                    parent=self.root)
        self.retrieve_data()
        self.create_buttons()

#InterfaceMain().root.mainloop()
InterfaceLogin().root_login.mainloop()