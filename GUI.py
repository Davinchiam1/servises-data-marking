import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
from data_loading import Data_loading
from data_processing import Data_unload
from find_keywords import Find_keywords
from API_Mpstats import requ_Mpstats
from tkcalendar import DateEntry


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.read_xlsx_var = tk.BooleanVar()
        self.read_xlsx_checkbox = tk.Checkbutton(self, text="Read XLSX files", variable=self.read_xlsx_var)
        self.read_xlsx_checkbox.grid(row=4, column=0, sticky=tk.W)

        self.find_keywords_var = tk.BooleanVar()
        self.find_keywords_checkbox = tk.Checkbutton(self, text="Find keywords", variable=self.find_keywords_var)
        self.find_keywords_checkbox.grid(row=4, column=1, sticky=tk.W)

        self.save_label = tk.Label(self, text="Save directory:")
        self.save_label.grid(row=0, column=0, sticky=tk.W)
        self.save_entry = tk.Entry(self)
        self.save_entry.grid(row=0, column=1)
        self.save_button = tk.Button(self, text="Browse...", command=self.browse_save_directory)
        self.save_button.grid(row=0, column=2)
        self.wb_oz_var = tk.StringVar()
        self.wb_oz_var.set("wb")
        self.rb01 = tk.Radiobutton(self, text="Wildberries", variable=self.wb_oz_var, value="wb")
        self.rb02 = tk.Radiobutton(self, text="Ozon", variable=self.wb_oz_var, value="oz")

        self.rb01.grid(row=0, column=3, sticky=tk.N)
        self.rb02.grid(row=0, column=4, sticky=tk.N)
        self.load_button = tk.Button(self, text="Load category", command=self.load_category)
        self.load_button.grid(row=1, column=2)

        self.date_entry_start = DateEntry(self, width=12, date_pattern='yyyy-MM-dd', background='darkblue',
                                          foreground='white', borderwidth=2, year=2021)
        self.date_entry_start.grid(row=1, column=3)

        self.date_entry_end = DateEntry(self, width=12, date_pattern='yyyy-MM-dd',background='darkblue',
                                        foreground='white', borderwidth=2, year=2023)
        self.date_entry_end.grid(row=1, column=4)

        self.directory_label = tk.Label(self, text="Directory:")
        self.directory_label.grid(row=2, column=0, sticky=tk.W)
        self.directory_entry = tk.Entry(self)
        self.directory_entry.grid(row=2, column=1)
        self.directory_button = tk.Button(self, text="Browse...", command=self.browse_directory)
        self.directory_button.grid(row=2, column=2)
        self.dir_file_var = tk.StringVar()
        self.dir_file_var.set("Dir")
        self.rb1 = tk.Radiobutton(self, text="Папка", variable=self.dir_file_var, value="Dir")
        self.rb2 = tk.Radiobutton(self, text="Файл", variable=self.dir_file_var, value="File")

        self.category_label = tk.Label(self, text="Category:")
        self.category_label.grid(row=1, column=0, sticky=tk.W)
        self.category_entry = tk.Entry(self)
        self.category_entry.grid(row=1, column=1)


        self.selection_label = tk.Label(self, text="Selection:")
        self.selection_label.grid(row=5, column=0, sticky=tk.W)
        self.selection_entry = tk.Entry(self)
        self.selection_entry.grid(row=5, column=1)

        self.language_label = tk.Label(self, text="Language:")
        self.language_label.grid(row=7, column=2, sticky=tk.W)
        self.language_entry = tk.Entry(self)
        self.language_entry.grid(row=7, column=3)

        self.Output_name = tk.Label(self, text="Output name:")
        self.Output_name.grid(row=5, column=2, sticky=tk.W)
        self.Output_name_entry = tk.Entry(self)
        self.Output_name_entry.grid(row=5, column=3)

        self.set_dates_var = tk.BooleanVar(value=True)
        self.set_dates_checkbox = tk.Checkbutton(self, text="Set dates", variable=self.set_dates_var)
        self.set_dates_checkbox.grid(row=4, column=2, sticky=tk.W)


        self.markers_label = tk.Label(self, text="Markers file:")
        self.markers_label.grid(row=6, column=0, sticky=tk.W)
        self.markers_entry = tk.Entry(self)
        self.markers_entry.grid(row=6, column=1)
        self.markers_button = tk.Button(self, text="Browse...", command=self.browse_markers)
        self.markers_button.grid(row=6, column=2)
        self.name_colum_label = tk.Label(self, text="Name colum:")
        self.name_colum_label.grid(row=7, column=0, sticky=tk.W)
        self.name_colum_entry = tk.Entry(self)
        self.name_colum_entry.grid(row=7, column=1)

        self.load_button = tk.Button(self, text="Load data", command=self.load_data)
        self.load_button.grid(row=8, column=1)

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(row=8, column=2)

        self.rb1.grid(row=4, column=3, sticky='n')
        self.rb2.grid(row=4, column=4, sticky='n')

    def load_category(self):
        save_directory = self.save_entry.get()
        category = self.category_entry.get()
        d1 = self.date_entry_start.get()
        d2 = self.date_entry_end.get()
        if self.wb_oz_var.get() == 'wb':
            api_connect = requ_Mpstats()
        else:
            api_connect=requ_Mpstats(request='oz')
        if category is not None:
            api_connect.get_cat_by_dates(category_string=category, start_date=d1, end_date=d2,save_directory=save_directory)


    def browse_save_directory(self):
        save_directory = filedialog.askdirectory()
        self.save_entry.delete(0, tk.END)
        self.save_entry.insert(0, save_directory)
    def browse_directory(self):
        if self.dir_file_var.get() == 'Dir':
            directory = filedialog.askdirectory()
        else:
            filetypes = [("CSV files", "*.csv"), ("XLSX files", "*.xlsx")]
            directory = filedialog.askopenfilenames(initialdir=".", filetypes=filetypes)
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def browse_markers(self):
        filetypes = [("Текстовые файлы", "*.txt"), ("XLSX files", "*.xlsx"), ("CSV files", "*.csv")]
        directory = filedialog.askopenfilenames(initialdir=".", filetypes=filetypes)
        self.markers_entry.delete(0, tk.END)
        self.markers_entry.insert(0, directory)
        pass
    def load_data(self):
        directory = self.directory_entry.get()
        read_xlsx = self.read_xlsx_var.get()
        find_keywords_var = self.find_keywords_var.get()
        selection = self.selection_entry.get().split(",")
        name_colum = self.name_colum_entry.get()
        if self.markers_entry.get() == '':
            markers = None
        else:
            markers = self.markers_entry.get()[1:-1]
            name_colum = self.name_colum_entry.get()
        filepath = None
        if len(selection) != 2:
            selection = None
        else:
            selection = (selection[0], selection[1])
        set_dates = self.set_dates_var.get()
        if self.dir_file_var.get() != 'Dir':
            filepath = directory[1:-1]
            directory = None
            finalname = os.path.dirname(filepath)
        else:
            finalname = directory
        if not os.path.exists(os.path.normpath((finalname+'\\result'))):
            os.makedirs(finalname+'\\result')
        dl = Data_loading()
        data = dl.get_data(directory=directory, read_xlsx=read_xlsx, selection=selection,
                           set_dates=set_dates, filepath=filepath)
        dp = Data_unload()
        dp.use_script(temp_frame=data, read_xlsx=read_xlsx, markers_file=markers, colum=name_colum,
                      set_dates=set_dates, filepath=filepath, finalname=os.path.normpath(finalname+'\\result\\final1.xlsx'))
        if find_keywords_var:
            language = self.language_entry.get()
            fk = Find_keywords(language=language)
            fk.use(name_colum=name_colum, need_normalization=False, n_grams=1,
                   temp_frame=data, otput_file=os.path.normpath(finalname+'\\result\\keywords.xlsx'))



root = tk.Tk()
root.title("Data Processing App")
root.geometry("550x200")
root.resizable(False, False)
root.columnconfigure(3, minsize=50, weight=1)
root.columnconfigure(1, minsize=50, weight=1)

app = App(master=root)
app.mainloop()
