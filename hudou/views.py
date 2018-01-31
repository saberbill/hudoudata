import os
import datetime
from django.http import JsonResponse
from hudou.model.valueobjects import House, HouseSold, Area, DailySummary
from hudou.handler.datafetcher import DataFetcher
from hudou.services.houseservices import HouseService
from hudou.services.apis import getDailySummary
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from hudou.util.utilities import todayWithTZ
from django.core import serializers

import json

from . import database
from .models import PageView

# Create your views here.

def index(request):
    #hostname = os.getenv('HOSTNAME', 'unknown')
    #PageView.objects.create(hostname=hostname)
    today = todayWithTZ()
    dailySummary = getDailySummary(today)[0]
    soldPercent = round(dailySummary.soldRooms/dailySummary.totalRooms, 2)
    return render(request, 'index.html',{
        'turnover': dailySummary.turnover,
        'totalRooms': dailySummary.totalRooms,
        'soldRooms': dailySummary.soldRooms,
        'soldPercent': format(soldPercent, '.00%'),
    })
    '''
    return render(request, 'hudou/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })
    '''

def getLatestSummary(request):
    days = request.GET.get('days')
    if(not days):
        days = '7'
    summaries = HouseService.listLatestDailySummary(int(days))
    #content = serializers.serialize("json", summaries)
    #print(content)
    dates = []
    soldRooms = []
    totalRooms = []
    turnovers = []
    for item in summaries[::-1]:
        dates.append(item.date)
        totalRooms.append(item.totalRooms)
        soldRooms.append(item.soldRooms)
        turnovers.append(item.turnover)
    data = {
        'count': len(summaries),
        'dates': dates,
        'totalRooms': totalRooms,
        'soldRooms': soldRooms,
        'turnovers': turnovers}

    return JsonResponse(data, content_type='application/json; charset=utf-8')

def getHouseArea(request):
    today = todayWithTZ().strftime("%Y-%m-%d")
    #houseSolds = HouseService.listHousesSoldByDate(today)
    #houses = HouseService.list(HouseService)
    #print(content)
    areas = []
    areaCounts = []
    totalAreas = HouseService.getOnlineHouses(today)
    for (k,v) in totalAreas.items():
        areas.append(k)
        areaCounts.append(v)
    data = {
        'count': len(totalAreas),
        'areas': areas,
        'areaCounts': areaCounts
    }
    return JsonResponse(data, content_type='application/json; charset=utf-8')

def health(request):
    return render(request,'index.html')
    #return HttpResponse(PageView.objects.count())

def getReportSummary(request):
    date = datetime.datetime.today()
    areas = Area.objects.only('id', 'area_name').all()
    houses = HouseService.listAllHouses(HouseService)
    houseSolds = HouseService.listHousesSoldByDate(date)

    total = 0
    sold = 0
    amount = 0.0
    soldHouseAreaCountMap = {}

    for housesold in houseSolds:
        total = total + 1
        houseDetail = House.objects.get(id=housesold.house_id)
        key = 'areaId-' + str(houseDetail.areaId)
        areaCountData = soldHouseAreaCountMap.get(key, None)
        if(not areaCountData):
            areaCountData = {'areaId': houseDetail.areaId,
                             'areaName': houseDetail.areaName,
                             'count': 1,
                             'soldCount': 0}
        else:
            areaCountData['count'] = areaCountData['count'] + 1
            soldHouseAreaCountMap[key] = areaCountData

        if (housesold.status == 1):
            sold = sold + 1
            if (housesold.specialPrice):
                price = housesold.specialPrice
            else:
                price = housesold.price * 0.88
            amount = amount + price

            areaCountData = soldHouseAreaCountMap.get(key, None)
            if (not areaCountData):
                areaCountData = {'areaId': houseDetail.areaId,
                                 'areaName': houseDetail.areaName,
                                 'count': 1,
                                 'soldCount': 1}
            else:
                areaCountData['soldCount'] = areaCountData['soldCount'] + 1
            soldHouseAreaCountMap[key] = areaCountData

    content = {'total': total, 'sold': sold, 'amount': round(amount, 2), 'soldPercent': round(sold/float(total), 2),
               'soldHouseAreas': soldHouseAreaCountMap}

    print(content)
    return JsonResponse(content, content_type='application/json; charset=utf-8')
