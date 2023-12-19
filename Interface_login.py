import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, time



class InterfaceLogin:
    def __init__(self):
        self.root_login = tk.Tk()
        self.root_login.title('PyFlora Pots Login')
        self.root_login.geometry('250x200')

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.interface()

    def login(self, event=None):
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

        else:
            message = 'Login credentials are incorrect.'
            messagebox.showerror(title='Unsuccesssful login', message=message)

    def interface(self):
        username_label = tk.Label(self.root_login, text='Username: ')
        username_label.grid(row=0, column=0, pady=(10,30))

        username_entry = tk.Entry(self.root_login, textvariable=self.username)
        username_entry.grid(row=0, column=1, pady=(10,30))

        password_label = tk.Label(self.root_login, text='Password: ')
        password_label.grid(row=1, column=0, pady=(0,15))

        password_entry = tk.Entry(self.root_login, textvariable=self.password,
                                show='*')
        password_entry.grid(row=1, column=1, pady=(0,15))

        start_button = tk.Button(self.root_login, text='Login', command=self.login)
        start_button.grid(row=2, columnspan=3, pady=5, ipadx=5, ipady=5)

        exit_button = tk.Button(
            self.root_login, text='Exit', command=self.root_login.destroy)
        exit_button.grid(row=3, columnspan=3, pady=5, ipadx=5, ipady=5)

        self.root_login.bind('<Return>', self.login)

InterfaceLogin().root_login.mainloop()
