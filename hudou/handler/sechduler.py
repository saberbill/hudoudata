# coding=utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from hudou.handler.datafetcher import DataFetcher


def fetchData():
    DataFetcher.readHudouOnlineData(DataFetcher)

def startCronJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchData, 'cron', second="30", minute="*/30", hour="*")
    scheduler.start()
