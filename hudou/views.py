
from hudou.handler.sechduler import startFetchDataCronJob, startClearOldHouseSoldDataCronJob
startFetchDataCronJob()
startClearOldHouseSoldDataCronJob()

from django.http import JsonResponse
from hudou.model.valueobjects import House, Area
from hudou.services.houseservices import HouseService
from django.shortcuts import render
from hudou.util.utilities import todayWithChineseTZ, nowWithChineseTZ, toChineseTZ


# Create your views here.

def index(request):
    today = todayWithChineseTZ()
    dailySummary = HouseService.listDailySummary(today)[0]
    soldPercent = round(dailySummary.soldRooms/dailySummary.totalRooms, 2)
    lastUpdated = toChineseTZ(dailySummary.lastUpdated)
    lastUpdated = lastUpdated.strftime("%Y-%m-%d %H:%M:%S")

    return render(request, 'index.html',{
        'turnover': round(dailySummary.turnover, 2),
        'totalRooms': dailySummary.totalRooms,
        'soldRooms': dailySummary.soldRooms,
        'soldPercent': format(soldPercent, '.00%'),
        'lastUpdated': lastUpdated,
    })

def getLatestSummary(request):
    days = request.GET.get('days')
    if(not days):
        days = '7'
    summaries = HouseService.listLatestDailySummary(int(days))

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
    today = todayWithChineseTZ().strftime("%Y-%m-%d")
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

def getAccessHistory(request):
    today = todayWithChineseTZ().strftime("%Y-%m-%d")
    data = {'data': HouseService.getAccessHistory(today + ' 00:00:00', today + ' 23:59:59')}
    return JsonResponse(data, content_type='application/json; charset=utf-8')