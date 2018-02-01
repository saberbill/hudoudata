# coding=utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from hudou.handler.datafetcher import DataFetcher


def fetchData():
    DataFetcher.readHudouOnlineData(DataFetcher)

def startCronJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchData, 'cron', second="*/60", minute="*", hour="*")
    scheduler.start()
