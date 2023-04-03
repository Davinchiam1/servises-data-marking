import os

import pandas as pd


class Data_loading:
    def __init__(self):
        self.final_frame = None
        self.temp_frame = None
        self.file_list = []
        self.date_list = []
        self.set_dates = None
        self.read_xlsx = None

    def _create_lists(self, directory):
        """Finding of all .csv files in directory"""
        if directory is not None:
            for f in os.scandir(directory):
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    self.file_list.append(f.path)
                    if self.set_dates:
                        self.date_list.append(f.path[-15:-5])
                if self.read_xlsx and f.path.split('.')[-1].lower() == 'xlsx':
                    self.file_list.append(f.path)
        else:
            for f in os.scandir():
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    self.file_list.append(f.path)
                    if self.set_dates:
                        self.date_list.append(f.path[-15:-5])
                if self.read_xlsx and f.path.split('.')[-1].lower() == 'xlsx':
                    self.file_list.append(f.path)

    def _read_data(self, filepath, selection, date=None):
        if filepath.split('.')[-1].lower() == 'csv':
            self.temp_frame = pd.read_csv(filepath, delimiter=';')
        elif filepath.split('.')[-1].lower() == 'xlsx' and self.read_xlsx:
            self.temp_frame = pd.read_excel(filepath)
        if self.set_dates:
            self.temp_frame['date'] = date
        if selection is not None:
            self.temp_frame = self.temp_frame.loc[self.temp_frame[selection[0]] == selection[1]]

    def _concentrate_data(self):
        """Concentrating data into one dataframe"""
        if self.final_frame is None:
            self.final_frame = self.temp_frame
        else:
            self.final_frame = pd.concat([self.temp_frame, self.final_frame], sort=False, axis=0)

    def get_data(self, directory, read_xlsx=False, selection=None, set_dates=True, filepath=None):
        self.set_dates = set_dates
        self.read_xlsx = read_xlsx
        if filepath is None:
            self._create_lists(directory=directory)
        else:
            self.file_list.append(filepath)
        if set_dates:
            for filename, date in zip(self.file_list, self.date_list):
                self._read_data(filepath=filename, date=date, selection=selection)
                self._concentrate_data()
        else:
            for filename in self.file_list:
                self._read_data(filepath=filename, selection=selection)
                self._concentrate_data()
        return self.final_frame
