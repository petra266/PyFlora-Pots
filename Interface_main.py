import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot
from Interface_add_pots import *
from Interface_open_pot import *

class InterfaceMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyFlora Pots")
        self.root.geometry('1200x800')

        self.create_buttons()

    def create_buttons(self):        

        for button in self.root.winfo_children():
            if isinstance(button, tk.Button):
                button.destroy()

        PyFloraPot_list = PyFloraPot.update_pot_list(self)

        for i in range(0, PyFloraPot.count_pots):

            if i % 2 == 0:
                button_row = i
                button_column = 1
            else: 
                button_row = i - 1
                button_column = 2

            pot_name = PyFloraPot_list[i].pot_name
            button = tk.Button(self.root, text=pot_name, command=lambda selected_name=pot_name: self.launch_InterfaceOpenPot(selected_name))
            button.grid(row=button_row, column=button_column)

        add_button = tk.Button(self.root, text="Add new pot",
                            command=self.launch_InterfaceAddPots)
        add_button.grid(row=button_row + 1, column=1, columnspan=2)

        exit_button = tk.Button(self.root, text="Quit",
                                command=self.root.destroy)
        exit_button.grid(row=button_row + 2, column=1, columnspan=2)

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

InterfaceMain().root.mainloop()