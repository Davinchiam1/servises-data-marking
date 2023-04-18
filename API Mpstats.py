import time

import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm

class requ_Mpstats:

    def __init__(self, request='wb/get/category'):
        self.url = 'https://mpstats.io/api/'
        self.request = request
        with open('token.txt', "r", encoding='utf8') as f:
            token = f.readline()
            print(token)
        self.headers = {
            'X-Mpstats-TOKEN': token,
            'Content-Type': 'application/json'
        }
        self.filter = {'sales': {'filterType': 'number', 'type': 'greaterThanOrEqual', 'filter': 5, 'filterTo': None}}

        self.sort = [{'colId': 'revenue', 'sort': 'desc'}]
        self.dates = []
        self.temp_frame = pd.DataFrame()

    def _date_list(self, start_date='2021-03-01', end_date='2023-03-01'):
        from datetime import datetime, timedelta
        dates = []
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        while current_date <= end_date:
            first_day = datetime(current_date.year, current_date.month, 1)
            last_day = datetime(current_date.year, current_date.month, 1) + timedelta(days=32)
            last_day = last_day.replace(day=1) - timedelta(days=1)
            dates.append((first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))
            current_date = last_day + timedelta(days=1)
        return dates

    def category_request(self, d1, d2, category_string='Зоотовары/Для собак', startRow=0, endRow=5000,
                         save=True):
        category_string = category_string

        url = self.url + self.request
        params = {
            'd1': d1,
            'd2': d2,
            'path': category_string
        }
        time.sleep(1)
        data = {
            'startRow': startRow,
            'endRow': endRow,
            'filterModel': self.filter,
            'sortModel': self.sort
        }
        response = requests.post(url, headers=self.headers, params=params, data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            data = json.loads(response.text)['data']
        if endRow < json.loads(response.text)['total']:
            temp_frame = pd.json_normalize(data)
            self.temp_frame = pd.concat([temp_frame, self.temp_frame], ignore_index=True)
            self.category_request(d1=d1, d2=d2, category_string=category_string, save=save, startRow=startRow + 5000,
                                  endRow=endRow + 5000)
        else:
            temp_frame = pd.json_normalize(data)
            self.temp_frame = pd.concat([temp_frame, self.temp_frame], ignore_index=True)

        date_obj1 = datetime.strptime(d2, '%Y-%m-%d')
        new_d2 = date_obj1.strftime('%d.%m.%Y')
        self.temp_frame['date'] = new_d2


        if save:
            self.temp_frame.to_excel(category_string + ' ' + d1 + '-' + d2 + '.xlsx')
            # print(df)


    def get_cat_by_dates(self, category_string, start_date, end_date):
        self.dates = self._date_list(start_date=start_date, end_date=end_date)
        self.final_frame = None
        date_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date_start = date_obj1.strftime('%d.%m.%Y')
        date_obj1 = datetime.strptime(end_date, '%Y-%m-%d')
        new_date_end = date_obj1.strftime('%d.%m.%Y')
        save_date = new_date_start + '-' + new_date_end
        i = 1
        for date in self.dates:

            self.category_request(d1=date[0], d2=date[1], category_string=category_string, save=False)
            if self.final_frame is None:
                self.final_frame = self.temp_frame
                self.colunm_list = [column for column in self.final_frame]
            else:
                temp_colums = [column for column in self.temp_frame]
                for final_colum, temp_colum in zip(self.colunm_list, temp_colums):
                    if final_colum != temp_colum:
                        self.temp_frame.rename(columns={temp_colum: final_colum}, inplace=True)
                self.temp_frame = self.temp_frame.loc[:, ~self.temp_frame.columns.duplicated(keep='last')]
                self.final_frame.reset_index(drop=True, inplace=True)
                self.final_frame = pd.concat([self.temp_frame, self.final_frame], sort=False, axis=0, ignore_index=True)
                print('#' + str(i) + ' Done!')
                i = i + 1
                self.temp_frame = None
        self.final_frame.to_excel(category_string.split(sep='/')[-2]+' ' + category_string.split(sep='/')[-1]
                                  + ' ' + save_date + '.xlsx')


# test = requ_Mpstats()
test = requ_Mpstats(request='oz/get/category')
# test.category_request(d1='2023-03-01', d2='2023-02-01')
test.get_cat_by_dates(category_string='Товары для животных/Для кошек/Лежаки и кровати', start_date='2021-04-01',
                      end_date='2023-03-01')
# url = 'http://mpstats.io/api/user/report_api_limit'
# Зоотовары/Для собак/Вольеры и клетки
# Зоотовары/Для собак/Корм и лакомства
# cat_list = ['Товары для животных/Для собак/Амуниция','Товары для животных/Для собак/Груминг',
#             'Товары для животных/Для собак/Вольеры и будки', 'Товары для животных/Для собак/Игрушки',
#             'Товары для животных/Для собак/Аксессуары для перевозки', 'Товары для животных/Для собак/Посуда для собак',
#             'Товары для животных/Для собак/Средства для ухода', 'Товары для животных/Для собак/Дрессировка собак',
#             'Товары для животных/Для собак/Матрасы и лежаки', 'Товары для животных/Для собак/Переноски']
# for cat in tqdm(cat_list):
#     test.get_cat_by_dates(category_string=cat, start_date='2021-04-01', end_date='2023-03-01')
