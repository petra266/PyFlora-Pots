import tkinter as tk
import sqlite3
from tkinter import messagebox

from PyFlora_class import PyFloraPot
from Interface_add_pots import *


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

        print("PyFlora count: ", PyFloraPot.count_pots)
        print("PyFlora list in main: ", PyFloraPot_list)

        for i in range(0, PyFloraPot.count_pots):
            button = tk.Button(self.root, text=PyFloraPot_list[i].pot_name)
            button.pack()

        add_button = tk.Button(self.root, text="Add new pot",
                            command=self.launch_InterfaceAddPots)
        add_button.pack()

        exit_button = tk.Button(self.root, text="Quit",
                                command=self.root.destroy)
        exit_button.pack()



    def launch_InterfaceAddPots(self):
        interface_add_pots = InterfaceAddPots(self.root)
        self.root.wait_window(interface_add_pots.toplevel_add_pots)
        self.create_buttons()

InterfaceMain().root.mainloop()
