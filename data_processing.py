import numpy as np
import pandas as pd
import os
from data_loading import Data_loading


# Получение данных в формате выгрузки Mpstat и их совмещение по месяцам с добавлением метки времени
def marker(colum, keywords, row=''):
    """" Base func for marking rows in frame by the presence of keywords"""
    val = 0
    # row = row.lower()
    for keyword in keywords:
        if type(row[colum]) is not str:
            val = 0
        else:
            if row[colum].lower().find(keyword) == -1:
                val = 0
            else:
                val = 1
                break
    return val


def single_marker(colum, key, keywords, row=''):
    """" Base func for marking rows in frame by the presence of keywords"""
    val = 0
    # row = row.lower()
    for keyword in keywords:
        if type(row[colum]) is not str:
            val = 'Неразмечено'
        else:
            if row[colum].lower().find(keyword) == -1:
                continue
            else:
                val = key
                break
    if val is None:
        val = 'Неразмечено'
    return val


class Data_unload:
    def __init__(self):
        self.final_frame = None

    def _filter(self):
        pass

    def _get_makers(self, colum, markers_file, single=False):
        """Marking data according to list of markers in .txt file"""
        markers = {}
        with open(markers_file, "r", encoding='utf8') as file:
            for line in file:
                if line is not None:
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
        if single:
            for key in markers:
                self.final_frame['marks'] = self.final_frame.apply(
                    lambda row: single_marker(row=row, colum=colum, keywords=markers[key], key=key), axis=1)
        else:
            for key in markers:
                self.final_frame[key] = self.final_frame.apply(
                    lambda row: marker(row=row, colum=colum, keywords=markers[key]), axis=1)

    def _to_zero(self):
        self.final_frame = None

    def use_script(self, read_xlsx=False, directory=None, finalname='./final.xlsx', set_dates=True, markers_file=None,
                   colum=None, temp_frame=None, filepath=None):
        """Func for executing a script for marking data, control parameters determine the method of marking"""
        if __name__ == "__main__":
            dl = Data_loading()
            self.final_frame = dl.get_data(read_xlsx=read_xlsx, directory=directory, set_dates=set_dates,
                                           filepath=filepath)
        else:
            self.final_frame = temp_frame
        if markers_file is not None:
            self._get_makers(colum=colum, markers_file=markers_file)
        if self.final_frame.shape[0]>250000:
            self.final_frame.to_csv(finalname+'.csv',index=False, sep=';',encoding='utf-8-sig')
        else:
            self.final_frame.to_excel(finalname+'.xlsx', sheet_name='list1', index=False)
        self._to_zero()

# test = Data_unload()
# test.use_script(directory='C:\\Users\\aos.user5\\Desktop\\сыворотки для ресниц\\ozon\\по периодам',
#                 finalname='C:\\Users\\aos.user5\\Desktop\\сыворотки для ресниц\\ozon\\по периодам\\final.xlsx')
# test.use_script(directory='C:\\Users\\aos.user5\\Desktop\\сыворотки для ресниц\\wb\\по периодам\\масла',
#                 finalname='C:\\Users\\aos.user5\\Desktop\\сыворотки для ресниц\\wb\\по периодам\\масла\\final.xlsx')

# test.use_script(directory='C:\\Users\\aos.user5\\Desktop\\Масло для лица\\ozon\\по периодам',
#                 finalname='C:\\Users\\aos.user5\\Desktop\\Масло для лица\\ozon\\по периодам\\final.xlsx')
