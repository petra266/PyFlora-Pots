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

        PyFloraPot_list = PyFloraPot.update_pot_list(self)

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
        InterfaceAddPots(self.root).toplevel_add_pots.mainloop()


InterfaceMain().root.mainloop()
