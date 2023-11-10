import os
import tkinter as tk
import sqlite3
from tkinter import messagebox


os.chdir('PyFlora Pots')


class InterfaceAddPots:

    def __init__(self, root):
        self.toplevel_add_pots = tk.Toplevel(root)
        self.toplevel_add_pots.title("PyFlora Pots - Let's plant!")
        self.toplevel_add_pots.geometry('1200x800')

        exit_button = tk.Button(self.toplevel_add_pots, text="Quit",
                                command=self.toplevel_add_pots.destroy)
        exit_button.pack()
