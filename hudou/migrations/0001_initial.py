# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('hostname', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        '''
            migrations.CreateModel(
                name='Area',
                fields=[
                    ('id', models.AutoField(primary_key=True, serialize=False)),
                    ('lid', models.CharField(max_length=40)),
                    ('areaName', models.CharField(db_column='area_name', max_length=30)),
                    ('long', models.FloatField()),
                    ('lat', models.FloatField()),
                ],
                options={
                    'db_table': 'area',
                },
            ),
            migrations.CreateModel(
                name='DailySummary',
                fields=[
                    ('id', models.AutoField(primary_key=True, serialize=False)),
                    ('totalRooms', models.IntegerField(db_column='total_rooms')),
                    ('soldRooms', models.IntegerField(db_column='sold_rooms')),
                    ('turnover', models.FloatField()),
                    ('date', models.DateField()),
                    ('lastUpdated', models.DateTimeField(db_column='last_updated')),
                ],
                options={
                    'db_table': 'daily_summary',
                },
            ),
            migrations.CreateModel(
                name='House',
                fields=[
                    ('id', models.AutoField(primary_key=True, serialize=False)),
                    ('uuid', models.CharField(max_length=40)),
                    ('areaId', models.IntegerField(db_column='area_id')),
                    ('areaName', models.CharField(db_column='area_name', max_length=30)),
                    ('lid', models.CharField(max_length=40)),
                    ('title', models.CharField(max_length=128)),
                    ('price', models.FloatField()),
                    ('lang', models.FloatField()),
                    ('lat', models.FloatField()),
                    ('model', models.CharField(max_length=30)),
                    ('status', models.SmallIntegerField()),
                    ('lastUpdated', models.DateTimeField(db_column='last_updated')),
                    ('createTime', models.DateTimeField(db_column='create_time')),
                ],
                options={
                    'db_table': 'house',
                },
            ),
            migrations.CreateModel(
                name='HouseSold',
                fields=[
                    ('id', models.AutoField(primary_key=True, serialize=False)),
                    ('houseId', models.IntegerField(db_column='house_id')),
                    ('price', models.FloatField()),
                    ('specialPrice', models.FloatField(db_column='special_price')),
                    ('status', models.SmallIntegerField()),
                    ('date', models.DateField()),
                    ('lastUpdated', models.DateTimeField(db_column='last_updated')),
                ],
                options={
                    'db_table': 'house_sold',
                },
            ),
            '''
    ]


from hudou.handler.sechduler import startFetchDataCronJob
startFetchDataCronJob()

#from hudou.handler.datafetcher import DataFetcher
#DataFetcher.readHudouOnlineData(DataFetcher)

#from hudou.services.houseservices import HouseService
#HouseService.handleHistory(HouseService)