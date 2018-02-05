# coding=utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from hudou.handler.datafetcher import DataFetcher
from hudou.services.houseservices import HouseService

import threading

def fetchData():
    DataFetcher.readHudouOnlineData(DataFetcher)

def startFetchDataCronJob():
    t = threading.Thread(target=fetchData)
    t.start()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchData, 'interval', minutes=10)
    scheduler.start()

def clearOldData():
    HouseService.deleteOldHouseSold(7)
    HouseService.deleteOldAccessHistory(7)

def startClearOldHouseSoldDataCronJob():
    #t = threading.Thread(target=clearOldData)
    #t.start()
    scheduler = BackgroundScheduler()
    scheduler.add_job(clearOldData, 'cron', second='0', minute='0', hour='2')
    scheduler.start()