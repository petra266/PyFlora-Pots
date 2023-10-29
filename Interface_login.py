import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, time


os.chdir('PyFlora Pots')

DB_NAME = 'Database_users.db'
QUERY_GET_PASSWORD = 'SELECT password, firstname FROM Database_users WHERE username ='
NOON = time(12, 0)
EVENING = time(18, 0)

root = tk.Tk()
root.title('PyFlora Pots: Login')
base_font = ('Helvetica', 16)
username = tk.StringVar()
password = tk.StringVar()


def login(event=None):
    now = datetime.now()
    now_time = time(now.hour, now.minute)
    success = False
    name = None
    try:
        sqlite_connection = sqlite3.connect(DB_NAME)
        cursor = sqlite_connection.cursor()
        query = QUERY_GET_PASSWORD + '"{}"'.format(username.get())
        cursor.execute(query)
        records = cursor.fetchall()
        if records:
            password_input = records[0][0]
            name = records[0][1]
            if password_input == password.get():
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


username_label = tk.Label(root, text='Username: ', font=base_font)
username_label.grid(row=0, column=0)

username_entry = tk.Entry(root, textvariable=username, font=base_font)
username_entry.grid(row=0, column=1)

password_label = tk.Label(root, text='Password: ', font=base_font)
password_label.grid(row=1, column=0)

password_entry = tk.Entry(root, textvariable=password,
                          font=base_font, show='*')
password_entry.grid(row=1, column=1)

start_button = tk.Button(root, text='Login', command=login, font=base_font)
start_button.grid(row=2, columnspan=2)

exit_button = tk.Button(
    root, text='Exit', command=root.destroy, font=base_font)
exit_button.grid(row=3, columnspan=2)

root.bind('<Return>', login)

root.mainloop()
