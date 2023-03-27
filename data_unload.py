import numpy as np
import pandas as pd
import os


# Получение данных в формате выгрузки Mpstat и их совмещение по месяцам с добавлением метки времени
def marker(row, colum, keywords):
    """" Base func for marking rows in frame by the presence of keywords"""
    val = 0
    for keyword in keywords:
        if type(row[colum]) is not str:
            val = 0
        else:
            if row[colum].find(keyword) == -1:
                val = 0
            else:
                val = 1
    return val


class Data_unload:
    def __init__(self):
        self.final_frame = None
        self.temp_frame = None
        self.file_list = []
        self.date_list = []
        self.set_dates = True

    def _create_lists(self, directory=None):
        """Finding of all .csv files in directory"""
        if directory is not None:
            for f in os.scandir(directory):
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    self.file_list.append(f.path)
                    if self.set_dates:
                        self.date_list.append(f.path[-15:-5])
        else:
            for f in os.scandir():
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    self.file_list.append(f.path)
                    if self.set_dates:
                        self.date_list.append(f.path[-15:-5])

    def _get_data(self, filename, date):
        """ Read file into temp frame, marking by data if necessary"""
        self.temp_frame = pd.read_csv(filename, delimiter=';')
        if self.set_dates:
            self.temp_frame['data'] = date
        # print(self.temp_frame.head(5))

    def _concentrate_data(self):
        """Concentrating data into one dataframe"""
        if self.final_frame is None:
            self.final_frame = self.temp_frame
        else:
            self.final_frame = pd.concat([self.temp_frame, self.final_frame], sort=False, axis=0)

    def _get_makers(self, colum, markers_file):
        """Marking data according to list of markers in .txt file"""
        markers = {}
        with open(markers_file, "r", encoding='utf8') as file:
            for line in file:
                temp_line = line.split(':')
                key = temp_line[0][0:-1] if temp_line[0][-1] == ' ' else temp_line[0]
                keywords_temp = temp_line[1].split(',')
                keywords = []
                for keyword in keywords_temp:
                    if keyword[0] == ' ' and keyword[-1] != '\n':
                        keyword = keyword[1:]
                    elif keyword[-1] == '\n' and keyword[0] == ' ':
                        keyword = keyword[1:-1]
                    keywords.append(keyword)
                markers[key] = keywords
        for key in markers:
            self.final_frame[key] = self.final_frame.apply(lambda row: marker(row=row, colum=colum, keywords=markers[key]), axis=1)

    def use_script(self, finalname='./final.xlsx', set_dates=True, markers_file=None, colum=None):
        """Func for executing a script for marking data, control parameters determine the method of marking"""
        self._create_lists()
        self.set_dates = set_dates

        for filename, date in zip(self.file_list, self.date_list):
            self._get_data(filename=filename, date=date)
            self._concentrate_data()
        if markers_file is not None:
            self._get_makers(colum=colum, markers_file=markers_file)
        self.final_frame.to_excel(finalname, sheet_name='list1', index=False)


test = Data_unload()
test.use_script()