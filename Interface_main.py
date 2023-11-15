import tkinter as tk

from PyFlora_class import PyFloraPot
from Interface_add_pots import *
from Interface_open_pot import *
from Interface_user_account import *

class InterfaceMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyFlora Pots")
        self.root.geometry('1200x800')

        self.create_buttons()

    def create_buttons(self):        

        # remove all buttons
        for button in self.root.winfo_children():
            if isinstance(button, tk.Button):
                button.destroy()

        # Header and options - top_space to be used for button.grid calculations
        HEADER = 5
        account_button = tk.Button(self.root, text="User account",
                            command=self.launch_InterfaceUserAccount)
        account_button.grid(row=0, column=2)

        # Defining and arranging buttons for each PyFlora pot
        PyFloraPot_list = PyFloraPot.update_pot_list(self)

        for i in range(0, PyFloraPot.count_pots):

            if i % 2 == 0:
                button_row = i + HEADER
                button_column = 1
            else: 
                button_row = i - 1 + HEADER
                button_column = 2

            pot_name = PyFloraPot_list[i].pot_name
            button = tk.Button(self.root, text=pot_name, command=lambda selected_name=pot_name: self.launch_InterfaceOpenPot(selected_name))
            button.grid(row=button_row, column=button_column)
        
        # Other buttons
        add_button = tk.Button(self.root, text="Add new pot",
                            command=self.launch_InterfaceAddPots)
        add_button.grid(row=button_row + 1 + HEADER, column=1, columnspan=2)

        sync_button = tk.Button(self.root, text="Sync", command=self.sync)
        sync_button.grid(row=button_row + 2 + HEADER, column=1, columnspan=2)

        logout_button = tk.Button(self.root, text="Log Out",
                                command=self.root.destroy)
        logout_button.grid(row=1000, column=1, columnspan=2)

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

    def sync(self):
        pots_to_sync = PyFloraPot.all_pot_names
        PyFloraPot.sync(PyFloraPot, pots_to_sync)
        '''messagebox.showerror(title='Error while attempting to sync!',
                    message='PyFlora Pot syncing unsuccessful: ' + str(e) + "\n\nPlease try again or restart the application.",
                    parent=self.toplevel_open_pot)'''
InterfaceMain().root.mainloop()