import tkinter as tk
import sqlite3
from tkinter import messagebox

class InterfaceUserAccount:

    def __init__(self, root):
        self.toplevel_user_account = tk.Toplevel(root)
        self.toplevel_user_account.title("User account details")
        self.toplevel_user_account.geometry('1200x800')

        # retrieve user inforamtion
        self.USER_INFO = self.retrieve_user_info()
    
        self.interface_elements()   
        self.password_visible = False             
    
    def interface_elements(self):
        
        # Define interface variables
        self.firstname = tk.StringVar()
        self.firstname.set(self.USER_INFO['firstname'])

        self.lastname = tk.StringVar()
        self.lastname.set(self.USER_INFO['lastname'])

        self.username = tk.StringVar()
        self.username.set(self.USER_INFO['username'])

        self.password = tk.StringVar()
        self.password.set('*' * len(self.USER_INFO['password']))

        self.show_password_text = tk.StringVar()
        self.show_password_text.set('Show password')

        # Define interface elements
        name_label = tk.Label(self.toplevel_user_account, text='Name: ')
        name_label.grid(row=1, column=1)

        firstname_entry = tk.Entry(self.toplevel_user_account, textvariable=self.firstname)
        firstname_entry.grid(row=1, column=2)

        lastname_entry = tk.Entry(self.toplevel_user_account, textvariable=self.lastname)
        lastname_entry.grid(row=1, column=3)

        username_label = tk.Label(self.toplevel_user_account, text='Username: ')
        username_label.grid(row=2, column=1)

        username_entry = tk.Entry(self.toplevel_user_account, textvariable=self.username)
        username_entry.grid(row=2, column=2)

        save_button = tk.Button(self.toplevel_user_account, text='Save user details', command=self.save_changes)
        save_button.grid(row=3, column=1, columnspan=2)

        password_label = tk.Label(self.toplevel_user_account, text='Password: ')
        password_label.grid(row=4, column=1)

        password_entry = tk.Entry(self.toplevel_user_account, textvariable=self.password)
        password_entry.grid(row=4, column=2)

        show_password_button = tk.Button(self.toplevel_user_account, textvariable=self.show_password_text, command=self.show_password)
        show_password_button.grid(row=4, column=3)

        change_password_button = tk.Button(self.toplevel_user_account, text='Change password', command=self.change_password)
        change_password_button.grid(row=5, column=1, columnspan=2)

    def retrieve_user_info(self):
        """ Retrieve user data from the Database_users and return it as a dictionary"""
        
        DB_NAME = 'Database_users.db'
        QUERY_GET_USER = 'SELECT * FROM Database_users'

        try:
            with sqlite3.connect(DB_NAME) as sql_connection:
                cursor = sql_connection.cursor()
                cursor.execute(QUERY_GET_USER)
                data = cursor.fetchall()[0]
                USER_INFO = {              
                    'firstname' : data[1],
                    'lastname': data[2],
                    'username': data[3],
                    'password': data[4],
                    }
                print("User information retrived.")
                return USER_INFO

        except sqlite3.Error as e:
            print('Data retrieving unsucessful. Error: ', e)
            messagebox.showerror(title='Error in retrieving data!',
                                 message='Data retrieving unsucessful. Error: ' + str(e) + "\nPlease restart the application.",
                                 parent=self.toplevel_user_account)
            self.toplevel_user_account.destroy()

    def validate_user_details(self):
        "Validate new user details"
        validation_details = True
        choices_label = ("Firstname", "Lastname", "Username")
        choices_value = (self.firstname.get(),self.lastname.get(), self.username.get())

        for i in range(0, len(choices_value)):
            # validate choices are in range 
            if len(choices_value[i]) > 50:
                validation_details = False
                messagebox.showwarning(title=choices_label[i] + 'out of range!',
                        message=choices_label[i] + ' you selected exceeds the limit of 50 characters.', 
                        parent=self.toplevel_user_account)
             # validate all choices are selected 
            elif len(choices_value[i]) == 0:
                validation_details = False
                messagebox.showwarning(title=choices_label[i] + 'not chosen!',
                        message=choices_label[i] + ' field is empty.', 
                        parent=self.toplevel_user_account)

        return validation_details

    def save_changes(self):
        """ Save changes to the user account """
        
        validation_details = self.validate_user_details()

        if validation_details:
            DB_NAME = 'Database_users.db'
            QUERY_UPDATE_USER = 'UPDATE Database_users SET firstname = "{}", lastname = "{}",  username = "{}" WHERE id = 1'.format(self.firstname.get(),self.lastname.get(), self.username.get())

            try:
                with sqlite3.connect(DB_NAME) as sql_connection:
                    cursor = sql_connection.cursor()
                    cursor.execute(QUERY_UPDATE_USER)
                    print("User information updated.")

            except sqlite3.Error as e:
                print('Data update unsucessful. Error: ', e)
                messagebox.showerror(title='Error in updating user data!',
                                    message='Data update unsucessful. Error: ' + str(e) + "\nPlease try again or restart the application.",
                                    parent=self.toplevel_user_account)
                self.toplevel_user_account.destroy()      

    def show_password(self):
        """ Show true value instead of * sign """
        
        if not self.password_visible:
            self.password.set(self.USER_INFO['password'])
            self.password_visible = True
            self.show_password_text.set('Hide password')

        else:
            if self.password.get() == self.USER_INFO['password']:
                self.password.set('*' * len(self.USER_INFO['password']))
            else:
                self.password.set('*' * len(self.USER_INFO['password']))
            self.password_visible = False
            self.show_password_text.set('Hide password')

    def validate_password(self):
        "Validate new password"
        validation_password = True
        new_password = self.password.get()
        if len(new_password) > 50:
            validation_password = False
            messagebox.showwarning(title='Password out of range!',
                    message='Password you selected exceeds the limit of 50 characters.', 
                    parent=self.toplevel_user_account)
        elif len(new_password) == 0:
            validation_password = False
            messagebox.showwarning(title='Password not chosen!',
                        message='Password field is empty.', 
                        parent=self.toplevel_user_account)   
        return validation_password       

    def change_password(self):
        validation_password = self.validate_password()
        #activate only if password validated and the old password is not shown in * signs
        if validation_password and self.password.get() != '*' * len(self.USER_INFO['password']):
            DB_NAME = 'Database_users.db'
            QUERY_UPDATE_PASSWORD = 'UPDATE Database_users SET password = "{}" WHERE id = 1'.format(self.password.get())

            try:
                with sqlite3.connect(DB_NAME) as sql_connection:
                    cursor = sql_connection.cursor()
                    cursor.execute(QUERY_UPDATE_PASSWORD)
                    print("Password updated.")

            except sqlite3.Error as e:
                print('Data update unsucessful. Error: ', e)
                messagebox.showerror(title='Error in updating password!',
                                    message='Data update unsucessful. Error: ' + str(e) + "\nPlease try again or restart the application.",
                                    parent=self.toplevel_user_account)
                self.toplevel_user_account.destroy()