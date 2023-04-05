import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from data_loading import Data_loading
# from combine_files import Combine_files
from find_keywords import Find_keywords


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.read_xlsx_var = tk.BooleanVar()
        self.read_xlsx_checkbox = tk.Checkbutton(self, text="Read XLSX files", variable=self.read_xlsx_var)
        self.read_xlsx_checkbox.grid(row=2, column=0, sticky=tk.W)

        self.find_keywords_var = tk.BooleanVar()
        self.find_keywords_checkbox = tk.Checkbutton(self, text="Find keywords", variable=self.find_keywords_var)
        self.find_keywords_checkbox.grid(row=2, column=1, sticky=tk.W)

        self.directory_label = tk.Label(self, text="Directory:")
        self.directory_label.grid(row=0, column=0, sticky=tk.W)
        self.directory_entry = tk.Entry(self)
        self.directory_entry.grid(row=0, column=1)
        self.directory_button = tk.Button(self, text="Browse...", command=self.browse_directory)
        self.directory_button.grid(row=0, column=2)

        self.selection_label = tk.Label(self, text="Selection:")
        self.selection_label.grid(row=3, column=0, sticky=tk.W)
        self.selection_entry = tk.Entry(self)
        self.selection_entry.grid(row=3, column=1)

        self.set_dates_var = tk.BooleanVar()
        self.set_dates_checkbox = tk.Checkbutton(self, text="Set dates", variable=self.set_dates_var)
        self.set_dates_checkbox.grid(row=4, column=0, sticky=tk.W)

        self.load_button = tk.Button(self, text="Load data", command=self.load_data)
        self.load_button.grid(row=5, column=1)

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(row=5, column=2)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def load_data(self):
        directory = self.directory_entry.get()
        read_xlsx = self.read_xlsx_var.get()
        find_keywords_var = self.find_keywords_var
        selection = self.selection_entry.get().split(",")
        if len(selection) != 2:
            selection = None
        else:
            selection = (selection[0], selection[1])
        set_dates = self.set_dates_var.get()

        dl = Data_loading()
        data = dl.get_data(directory=directory, read_xlsx=read_xlsx, selection=selection, set_dates=set_dates)


root = tk.Tk()
root.title("Data Processing App")
root.geometry("600x400")
root.resizable(False, False)
app = App(master=root)
app.mainloop()
