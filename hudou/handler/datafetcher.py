# coding=utf-8

import json
import requests
from hudou.services.houseservices import HouseService
from django.utils import timezone
from hudou.util.utilities import Utilities, todayWithChineseTZ

PAGE_SIZE = 70
URL = 'http://mp.hudoufun.cn/tenement/js/listview_h5.ashx?' \
      'op=1' \
      '&r=0.6620256237220019' \
      '&table=tenement_rooms1' \
      '&city=%E6%88%90%E9%83%BD&lng=0' \
      '&lat=0' \
      '&filter=' \
      '&order2=auto' \
      '&PADDING=0' \
      '&refable=false' \
      '&page=js%2Flistview_h5.ashx' \
      '&search=' \
      '&order=' \
      '&totalnum=-1' \
      '&random=0.3783954663667828'

class DataFetcher:
    def fetch(url):
        requests.session()
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        return resp.text

    def getData(pageIndex, pageSize):
        url = URL + '&pageindex=' + str(pageIndex) + '&pageSize=' + str(pageSize)
        content = DataFetcher.fetch(url)
        result = json.loads(content)
        return result

    def readHudouOnlineData(self):
        pageIndex = 0
        hasPage = True

        print('Fetching data...')
        while (hasPage):
            data = self.getData(pageIndex, PAGE_SIZE)
            HouseService.saveAllHouses(data['data'])
            pageIndex = pageIndex + 1
            hasPage = True if (pageIndex < int(data['pagenum'])) else False

        # generate daily summary
        today = todayWithChineseTZ()
        HouseService.generateDailySummary(today)
        print('Data fetching completed.')

#DataFetcher.readHudouOnlineData(DataFetcher)