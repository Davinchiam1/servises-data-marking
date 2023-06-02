import pandas as pd
from pytrends.request import TrendReq

requests_args = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36'
    }
}


# pt = TrendReq(hl="en-US", tz=360)
# kw_list = ["патчи для глаз"]
# pt.build_payload(kw_list, timeframe='today 5-y', geo='RU', gprop='')
# massive = pt.interest_over_time()
# print(massive.tail(20))


class Common_trends:
    def __init__(self, kw_list=[], timeframe='today 5-y', region='US'):
        self.pt = TrendReq(hl="en-US", tz=360)
        self.kw_list = kw_list
        self.timeframe = timeframe
        self.region = region

    def get_region(self):
        if len(self.kw_list) > 5:
            blocks = [self.kw_list[i:i + 5] for i in range(0, len(self.kw_list), 5)]
            for i in range(len(blocks)):
                self.pt.build_payload(blocks[i], timeframe=self.timeframe, geo=self.region, gprop='')
                temp = self.pt.interest_over_time()
                massive=pd.merge(massive, temp, left_index=True, right_index=True)
        else:
            self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            massive = self.pt.interest_over_time()
        massive.to_excel('US_trends.xlsx')


    def get_global(self):
        if len(self.kw_list) > 5:
            blocks = [self.kw_list[i:i + 5] for i in range(0, len(self.kw_list), 5)]
            for i in range(len(blocks)):
                self.pt.build_payload(blocks[i], timeframe=self.timeframe, gprop='')
                temp = self.pt.interest_by_region("COUNTRY", inc_low_vol=True, inc_geo_code=True)
                by_country = pd.merge(by_country, temp, left_index=True, right_index=True)
        else:
            self.pt.build_payload(self.kw_list, timeframe=self.timeframe, gprop='')
            by_country = self.pt.interest_by_region("COUNTRY", inc_low_vol=True, inc_geo_code=True)
        by_country.to_excel('intr_by_country.xlsx')


    def get_by_country(self):
        if len(self.kw_list) > 5:
            blocks = [self.kw_list[i:i + 5] for i in range(0, len(self.kw_list), 5)]
            for i in range(len(blocks)):
                self.pt.build_payload(blocks[i], timeframe=self.timeframe, geo=self.region, gprop='')
                temp_city = self.pt.interest_by_region("CITY", inc_low_vol=True, inc_geo_code=True)
                temp_region = self.pt.interest_by_region("REGION", inc_low_vol=True, inc_geo_code=True)
                temp_dma = self.pt.interest_by_region("DMA", inc_low_vol=True, inc_geo_code=True)
                by_city = pd.merge(by_city, temp_city, left_index=True, right_index=True)
                by_region = pd.merge(by_region, temp_region, left_index=True, right_index=True)
                by_dma = pd.merge(by_dma, temp_dma, left_index=True, right_index=True)
        else:
            self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            by_city = self.pt.interest_by_region("CITY", inc_low_vol=True, inc_geo_code=True)
            by_region = self.pt.interest_by_region("REGION", inc_low_vol=True, inc_geo_code=True)
            by_dma = self.pt.interest_by_region("DMA", inc_low_vol=True, inc_geo_code=True)
        with pd.ExcelWriter('trends_by_county.xlsx', engine='xlsxwriter') as writer:
            by_region.to_excel(writer, sheet_name='Region', index=True)
            by_city.to_excel(writer, sheet_name='City', index=True)
            by_dma.to_excel(writer, sheet_name='DMA', index=True)

    def related_topics(self, ):
        rising=pd.DataFrame()
        top=pd.DataFrame()
        for kw in self.kw_list:
            kw_list = []
            kw_list.append(kw)
            self.pt.build_payload(kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            rt = self.pt.related_topics()
            rt[kw]['rising']['key']=kw
            rising=pd.concat([rising, rt[kw]['rising']], ignore_index=True)
            rt[kw]['top']['key'] = kw
            top = pd.concat([rising, rt[kw]['rising']], ignore_index=True)
        with pd.ExcelWriter('Related topics.xlsx', engine='xlsxwriter') as writer:
            rising.to_excel(writer, sheet_name='rising', index=True)
            top.to_excel(writer, sheet_name='top', index=True)

        # self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def related_searches(self):
        for kw in self.kw_list:
            kw_list = []
            kw_list.append(kw)
            self.pt.build_payload(kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            rt = self.pt.related_queries()
            with pd.ExcelWriter('Related searches ' + kw + '.xlsx', engine='xlsxwriter') as writer:
                for key in rt[kw].keys():
                    rt[kw][key].to_excel(writer, sheet_name=key, index=True)

        # self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def suggested_topics(self):
        sugg = pd.DataFrame()
        for kw in self.kw_list:
            topics = self.pt.suggestions(kw)
            temp = pd.DataFrame(topics)
            temp['key']=kw
            sugg=pd.concat([sugg,temp], ignore_index=True)
            print(sugg)



test = Common_trends(kw_list=['iphone', 'ios'])
# test.get_region()
test.related_searches()
# test.suggested_topics()