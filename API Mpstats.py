import requests
import json
import pandas as pd
from datetime import datetime

class requ_Mpstats:

    def __init__(self):
        self.url = 'https://mpstats.io/api/'
        self.request = 'wb/get/category'
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
        self.temp_frame=None

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

    def category_request(self, d1, d2, category_string='Зоотовары/Для собак', startRow=0, endRow=5000,save=True):
        category_string = category_string

        url = self.url + self.request
        params = {
            'd1': d1,
            'd2': d2,
            'path': category_string
        }
        data = {
            'startRow': startRow,
            'endRow': endRow,
            'filterModel': self.filter,
            'sortModel': self.sort
        }

        response = requests.post(url, headers=self.headers, params=params, data=json.dumps(data))
        if response.status_code == 200:
            data = json.loads(response.text)['data']
            self.temp_frame = pd.json_normalize(data)
            date_obj1 = datetime.strptime(d2, '%Y-%m-%d')
            new_d2 = date_obj1.strftime('%d.%m.%Y')
            self.temp_frame['date'] = new_d2
            # df.drop(axis=1, inplace=True,
            #         columns=['color', 'thumb', 'final_price_min', 'final_price_max', 'basic_sale', 'final_price',
            #                  'basic_price', 'promo_sale', 'client_price', 'revenue_potential', 'days_with_sales',
            #                  'average_if_in_stock', 'graph'])
            # print(response.text)
            if save:
                self.temp_frame.to_excel(category_string + ' ' + d1 + '-' + d2 + '.xlsx')
            # print(df)
        else:
            pass

    def get_cat_by_dates(self, category_string, start_date, end_date):
        self.dates = self._date_list(start_date=start_date, end_date=end_date)
        self.final_frame = None
        date_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date_start = date_obj1.strftime('%d.%m.%Y')
        date_obj1 = datetime.strptime(end_date, '%Y-%m-%d')
        new_date_end = date_obj1.strftime('%d.%m.%Y')
        save_date = new_date_start + '-'+ new_date_end
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
                self.final_frame = pd.concat([self.temp_frame, self.final_frame], sort=False, axis=0)
        self.final_frame.to_excel(category_string.split(sep='/')[-1] + ' ' + save_date + '.xlsx')




test = requ_Mpstats()
# test.category_request(d1='2023-03-01', d2='2023-02-01')
test.get_cat_by_dates(category_string='Зоотовары/Для кошек/Игрушки и когтеточки', start_date='2023-01-01', end_date='2023-03-01')
# url = 'http://mpstats.io/api/user/report_api_limit'
#
# headers = {
#     'X-Mpstats-TOKEN': '61615ecd6159c8.9570050408ccb7fbf4ab2f74d256e0850caf2666',
#     'Content-Type': 'application/json'
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.text)
