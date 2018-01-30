# coding=utf-8

from django.db import models


class House(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=40)
    area_id = models.IntegerField()
    area_name = models.CharField(max_length=30)
    lid = models.CharField(max_length=40)
    title = models.CharField(max_length=128)
    price = models.FloatField()
    lang = models.FloatField()
    lat = models.FloatField()
    model = models.CharField(max_length=30)
    status = models.SmallIntegerField()
    last_updated = models.DateTimeField()
    create_time=models.DateTimeField()

    def __unicode__(self):  # __str__ on Python 3
        return self


class HouseSold(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    house_id = models.IntegerField()
    price = models.FloatField()
    special_price = models.FloatField()
    status = models.SmallIntegerField()
    date = models.DateField()
    last_updated = models.DateTimeField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name


class Area(models.Model):
    #id = models.IntegerField()
    id = models.AutoField(primary_key=True)
    lid = models.CharField(max_length=40)
    area_name = models.CharField(max_length=30)
    long = models.FloatField()
    lat = models.FloatField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name
