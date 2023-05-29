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
        self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def get_region(self):
        massive = self.pt.interest_over_time()
        massive.to_excel('US_trends.xlsx')

    def get_global(self):
        self.pt.build_payload(self.kw_list, timeframe=self.timeframe, gprop='')
        by_country = self.pt.interest_by_region("COUNTRY", inc_low_vol=True, inc_geo_code=True)
        by_country.to_excel('intr_by_country.xlsx')
        self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def get_by_country(self):
        by_city = self.pt.interest_by_region("CITY", inc_low_vol=True, inc_geo_code=True)
        by_region = self.pt.interest_by_region("REGION", inc_low_vol=True, inc_geo_code=True)
        by_dma = self.pt.interest_by_region("", inc_low_vol=True, inc_geo_code=True)
        with pd.ExcelWriter('trends_by_county.xlsx', engine='xlsxwriter') as writer:
            by_region.to_excel(writer, sheet_name='Region', index=True)
            by_city.to_excel(writer, sheet_name='City', index=True)
            by_dma.to_excel(writer, sheet_name='DMA', index=True)

    def related_topics(self, ):
        for kw in self.kw_list:
            kw_list = []
            kw_list.append(kw)
            self.pt.build_payload(kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            rt = self.pt.related_topics()
            with pd.ExcelWriter('Related topics ' + kw + '.xlsx', engine='xlsxwriter') as writer:
                for key in rt[kw].keys():
                    rt[kw][key].to_excel(writer, sheet_name=key, index=True)

        self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def related_searches(self):
        for kw in self.kw_list:
            kw_list = []
            kw_list.append(kw)
            self.pt.build_payload(kw_list, timeframe=self.timeframe, geo=self.region, gprop='')
            rt = self.pt.related_queries()
            with pd.ExcelWriter('Related searches ' + kw + '.xlsx', engine='xlsxwriter') as writer:
                for key in rt[kw].keys():
                    rt[kw][key].to_excel(writer, sheet_name=key, index=True)

        self.pt.build_payload(self.kw_list, timeframe=self.timeframe, geo=self.region, gprop='')

    def suggested_topics(self):
        for kw in self.kw_list:
            topics=self.pt.suggestions(kw)
            print(topics)



test = Common_trends(kw_list=['iphone', 'ios'])
# test.get_region()
# test.related_topics()
test.suggested_topics()