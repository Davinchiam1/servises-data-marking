import os.path
import time
import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def progress_bar(func):
    def wrapper(*args, **kwargs):
        with tqdm(total=100) as pbar:
            for i in range(100):
                pbar.update(1)
                result = func(*args, **kwargs)
        return result

    return wrapper


class requ_Mpstats:
    """Main class for loading data from Mpstats api"""
    def __init__(self, request='wb'):
        self.url = 'https://mpstats.io/api/'
        self.request = request
        with open('token.txt', "r", encoding='utf8') as f:
            token = f.readline()
            print(token)
        self.headers = {
            'X-Mpstats-TOKEN': token,
            'Content-Type': 'application/json'
        }
        self.filter = {'sales': {'filterType': 'number', 'type': 'greaterThanOrEqual', 'filter': 10, 'filterTo': None}}

        self.sort = [{'colId': 'revenue', 'sort': 'desc'}]
        self.dates = []
        self.temp_frame = pd.DataFrame()

    def _date_list(self, start_date='2021-03-01', end_date='2023-03-01'):
        """Create list of pairs of dates from start to end with one month step"""
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

    def _get_sku_info(self, sku):
        """Loading info sor up to 200 SKu"""
        url = self.url + self.request + "/get/items/batch"
        # str(sku)
        params = {'ids': sku}
        response = requests.post(url=url, headers=self.headers, data=json.dumps(params))
        print(response.status_code)
        json_data = response.json()
        df = pd.json_normalize(json_data)
        df['photos'] = df['photos'][0][0]['f']
        return df

    def _get_sku_sales(self, sku, d1, d2):
        """Load sales by sku from d1 to d2"""
        url = self.url + self.request + "/get/item/" + str(sku) + '/sales'
        params = {
            'd1': d1,
            'd2': d2
        }
        response = requests.get(url=url, headers=self.headers, params=params)
        print(response.status_code)
        json_data = response.json()
        df = pd.json_normalize(json_data)
        return df

    # @progress_bar
    def category_request(self, d1, d2, category_string='Зоотовары/Для собак', startRow=0, endRow=5000,
                         save=True):
        """Load SKU in category from d1 to d2 starting from row start to end, and saved them in file if selected"""
        category_string = category_string

        url = self.url + self.request + "/get/category"
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


    def get_cat_by_dates(self, category_string, start_date, end_date, save_directory=None):
        """Loading selected category from starn to end date with step month.Results are contcat into 1 file and saved
         in save dir. If loaded file is larger than 250000 save format is csv, else -- xlsx. If file is larger than
         1000000 rows -- it splits in two"""
        self.dates = self._date_list(start_date=start_date, end_date=end_date)
        self.final_frame = None
        date_obj1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date_start = date_obj1.strftime('%d.%m.%Y')
        date_obj1 = datetime.strptime(end_date, '%Y-%m-%d')
        new_date_end = date_obj1.strftime('%d.%m.%Y')
        save_date = new_date_start + '-' + new_date_end
        i = 1
        if category_string.find('/')>0:
            category = category_string.split(sep='/')[-2] + ' ' + category_string.split(sep='/')[-1]
        else:
            category = category_string
        if save_directory is not None:
            save_path = save_directory + '/' + category + ' ' + save_date
        else:
            save_path = category + ' ' + save_date
        for date in self.dates:

            self.category_request(d1=date[0], d2=date[1], category_string=category_string, save=False)
            if self.final_frame is None:
                if self.temp_frame.shape[0] != 0:
                    self.final_frame = self.temp_frame
                    print('#' + str(i) + ' Done!')
                    self.colunm_list = [column for column in self.final_frame]
                else:
                    i = i + 1
                    print('No data from' + date[0] + ' ' + date[1])
            else:
                temp_colums = [column for column in self.temp_frame]
                # for final_colum, temp_colum in zip(self.colunm_list, temp_colums):
                #     if final_colum != temp_colum:
                #         self.temp_frame.rename(columns={temp_colum: final_colum}, inplace=True)
                self.temp_frame = self.temp_frame.loc[:, ~self.temp_frame.columns.duplicated(keep='last')]
                self.final_frame.reset_index(drop=True, inplace=True)
                self.final_frame = pd.concat([self.temp_frame, self.final_frame], sort=False, axis=0, ignore_index=True)
                print('#' + str(i) + ' Done!')
                i = i + 1
                self.temp_frame = None
                if self.final_frame.shape[0] > 250000:
                    format ='.csv'
                else:
                    format = '.xlsx'
                if self.final_frame.shape[0] > 1000000:
                    self.final_frame.to_csv(save_path+'_1' + format, sep=';', encoding='utf-8-sig')
                    self.final_frame = None
        if format == '.csv':
            self.final_frame.to_csv(save_path + format, sep=';',encoding='utf-8-sig')
        else:
            self.final_frame.to_excel(save_path + format)
        print('Finished')

    # @progress_bar
    def load_by_SKU(self, save_directory, start_date, end_date, sku_list, load_info=False, load_sales=False,
                    db_connect=False):
        if os.path.isfile(sku_list):
            if os.path.splitext(sku_list)[1] == '.csv':
                sku_frame = pd.read_csv(sku_list, delimiter=';')
            elif os.path.splitext(sku_list)[1] == '.xlsx':
                sku_frame = pd.read_excel(sku_list)
            sku_list = list(sku_frame['SKU'])
        else:
            sku_item = sku_list
            sku_list = []
            sku_list.append(sku_item)

        if load_info:
            index = 0
            step = 199
            info_frame = pd.DataFrame()
            while index < len(sku_list):
                temp_list = sku_list[index:index + step]
                temp = self._get_sku_info(temp_list)
                info_frame = pd.concat([info_frame, temp], ignore_index=True)
                index = index + step + 1
                if (index + step + 1) > len(sku_list):
                    step = len(sku_list) - index
            if db_connect:
                return info_frame
            else:
                info_frame.to_excel(save_directory + '/SKU\'s info.xlsx')

        if load_sales:
            save_directory = save_directory + '\\sales'
            if not os.path.exists(os.path.normpath(save_directory)):
                os.makedirs(save_directory)
            for sku in sku_list:
                sales_info = self._get_sku_sales(sku=sku, d1=start_date, d2=end_date)
                sales_info.to_excel(save_directory + '/' + str(sku) + '_sale.xlsx')

# test = requ_Mpstats()
# test = requ_Mpstats(request='wb/get/subject')
# print(test._get_sku_sales(sku=51450143,d1='2023-03-01',d2='2023-03-30'))
# test.category_request(d1='2023-03-01', d2='2023-02-01')
# test.get_cat_by_dates(category_string='Товары для животных/Миски для животных', start_date='2021-04-01', end_date='2023-03-01')
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

