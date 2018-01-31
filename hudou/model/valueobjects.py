# coding=utf-8

from django.db import models


class House(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=40)
    areaId = models.IntegerField(db_column='area_id')
    areaName = models.CharField(max_length=30,db_column='area_name')
    lid = models.CharField(max_length=40)
    title = models.CharField(max_length=128)
    price = models.FloatField()
    lang = models.FloatField()
    lat = models.FloatField()
    model = models.CharField(max_length=30)
    status = models.SmallIntegerField()
    lastUpdated = models.DateTimeField(db_column='last_updated')
    createTime=models.DateTimeField(db_column='create_time')

    def __unicode__(self):  # __str__ on Python 3
        return self

    class Meta:
        db_table = "house"



class HouseSold(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    houseId = models.IntegerField(db_column='house_id')
    price = models.FloatField()
    specialPrice = models.FloatField(db_column='special_price')
    status = models.SmallIntegerField()
    date = models.DateField()
    lastUpdated = models.DateTimeField(db_column='last_updated')

    def __unicode__(self):  # __str__ on Python 3
        return self.name

    class Meta:
        db_table = "house_sold"


class Area(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    lid = models.CharField(max_length=40)
    areaName = models.CharField(max_length=30, db_column='area_name')
    long = models.FloatField()
    lat = models.FloatField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name

    class Meta:
        db_table = "area"


class DailySummary(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    totalRooms = models.IntegerField(db_column='total_rooms')
    soldRooms = models.IntegerField(db_column='sold_rooms')
    turnover = models.FloatField()
    date = models.DateField()
    lastUpdated=models.DateTimeField(db_column='last_updated')

    def __unicode__(self):  # __str__ on Python 3
        return self

    class Meta:
        db_table = "daily_summary"