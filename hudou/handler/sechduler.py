# coding=utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from hudou.handler.datafetcher import DataFetcher


def fetchData():
    DataFetcher.readHudouOnlineData(DataFetcher)

def startFetchDataCronJob():
    fetchData()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchData, 'interval', minutes=10)
    scheduler.start()
