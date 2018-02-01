import datetime
import sys
from django.utils import timezone
from hudou.model.valueobjects import House, HouseSold, Area, DailySummary
from hudou.util.utilities import Utilities, todayWithTZ, nowWithTZ
from django.db import connection, transaction

class HouseService:
    def list(self):
        return House.objects.filter('status=1')

    def count(self):
        return House.objects.count('status=1')

    def saveHouse(houseData):
        now = nowWithTZ()
        try:
            house = House.objects.get(uuid=houseData['id'])
        except House.DoesNotExist:
            lid = houseData['lid']
            areaId = HouseService.matchArea(float(houseData['lng']), float(houseData['lat']))
            area = Area.objects.get(id=areaId)
            house = House(uuid=houseData['id'],
                          lid=lid,
                          title=houseData['title'],
                          lang=float(houseData['lng']),
                          lat=float(houseData['lat']),
                          price=houseData['price4hour'],
                          model=houseData['housemodel'],
                          areaId = area.id,
                          areaName = area.areaName,
                          status=1,
                          createTime=now,
                          lastUpdated = now)
            house.save()

        house = House.objects.get(uuid=houseData['id'])

        return house.id

    def saveHouseSold(houseId, data):
        now = nowWithTZ()
        today = todayWithTZ()
        try:
            houseSold = HouseSold.objects.get(houseId=houseId, date=today)
            houseSold.price = float(data['price4hour'])
            houseSold.specialPrice=float(data['specialPrice']) if data['specialPrice'] else 0
            houseSold.status=int(data['sold'])
            if((houseSold.status == 1) and (not houseSold.lastUpdated)):
                houseSold.lastUpdated = now
        except HouseSold.DoesNotExist:
            houseSold = HouseSold(houseId=houseId,
                                  date=today,
                                  price=float(data['price4hour']),
                                  specialPrice=float(data['specialPrice']) if data['specialPrice'] else 0,
                                  status=int(data['sold']),
                                  lastUpdated=now)
        houseSold.save()

    def saveAllHouses(data):
        for item in data:
            houseId = HouseService.saveHouse(item)
            HouseService.saveHouseSold(houseId, item)

    def generateDailySummary(date):
        solds = HouseService.listHousesSoldByDate(date)
        totalRooms = 0
        soldRooms = 0
        turnover = float(0.0)
        for item in solds:
            totalRooms = totalRooms + 1
            if (item.status == 1):
                soldRooms = soldRooms + 1
                turnover = turnover + item.price
        turnover = round(turnover, 2)
        HouseService.saveDailySummary({
            'totalRooms': totalRooms,
            'soldRooms': soldRooms,
            'turnover': turnover,
            'date': date})

    def saveDailySummary(data):
        now = nowWithTZ()
        today = todayWithTZ()
        try:
            dailySummary = DailySummary.objects.get(date=data['date'])
            dailySummary.totalRooms = data['totalRooms']
            dailySummary.soldRooms = data['soldRooms']
            dailySummary.turnover = data['turnover']
            dailySummary.date = data['date']
            dailySummary.lastUpdated = now
        except DailySummary.DoesNotExist:
            dailySummary = DailySummary(
                totalRooms=data['totalRooms'],
                soldRooms=data['soldRooms'],
                turnover=data['turnover'],
                date=data['date'],
                lastUpdated=now)
        dailySummary.save()

    def listAllHouses(self):
        return House.objects.all()

    def listHousesSoldByDate(date):
        return HouseSold.objects.filter(date=date)

    def listHousesSoldBetweenDates(dateFrom, dateTo):
        return House.objects.filter(date__gte=dateFrom, date__lte=dateTo)

    def listDailySummary(dateStr):
        return DailySummary.objects.filter(date=dateStr)

    def listDailySummaryBetweenDates(dateFrom, dateTo):
        return DailySummary.objects.filter(date__gte=dateFrom, date__lte=dateTo)

    def listDailySummaryByLatest7Days(self):
        return HouseService.listLatestDailySummary(7)

    def listDailySummaryByLatest30Days(self):
        return HouseService.listLatestDailySummary(30)

    def listLatestDailySummary(days):
        return DailySummary.objects.all().order_by('-date')[:days]

    def listAllAreas(self):
        return Area.objects.all()

    def getOrSaveAreaByLid(lid):
        area = Area(lid=lid, areaName='新增')
        try:
            area = Area.objects.get(lid=lid)
        except area.DoesNotExist:
            area.save()

        area = Area.objects.get(lid=lid)

        return area

    def matchArea(long, lat):
        areaSet = HouseService.listAllAreas(HouseService)

        mixDistance = sys.float_info.max
        areaId = 0

        for area in areaSet:
            distance = Utilities.haversine(long, lat, area.long, area.lat)
            if(distance < mixDistance):
                mixDistance = distance
                areaId = area.id
        return areaId

    def handleHistory(self):
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT date FROM house_sold ORDER BY date')
        dates = cursor.fetchall()

        for item in dates:
            HouseService.generateDailySummary(item[0])

    def getOnlineHouses(dateStr):
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT A.id, A.area_id, A.area_name, B.status "
                       "FROM house A, house_sold B "
                       "WHERE A.id=B.house_id AND B.date='%s'" % (dateStr))
        '''
        cursor.execute("SELECT id, area_id, area_name "
                       "FROM house WHERE id IN "
                       "(SELECT house_id FROM house_sold WHERE date='%s')"%(dateStr))
        houses = cursor.fetchall()
        cursor.execute("SELECT house_id, status "
                       "FROM  house_sold WHERE date='%s'" % (dateStr))
        '''
        houses = cursor.fetchall()
        toalHouseAreas = {}
        soldHouseAreas = {}
        for item in houses:
            key = item[2]
            if key in toalHouseAreas:
                count = toalHouseAreas.pop(key) + 1
            else:
                count = 1
            toalHouseAreas.setdefault(key, count)

            if key in soldHouseAreas:
                if (item[3] == 1):
                    count = soldHouseAreas.pop(key) + 1
            else:
                count = 1 if (item[3] == 1) else 0
            soldHouseAreas.setdefault(key, count)

        return toalHouseAreas