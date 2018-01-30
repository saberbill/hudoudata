import datetime
import sys
from django.utils import timezone
from hudou.model.valueobjects import House, HouseSold, Area
from hudou.util.utilities import Utilities

class HouseService:
    def list(self):
        return House.objects.filter('status=1')

    def count(self):
        return House.objects.count('status=1')

    def saveHouse(houseData):
        now = timezone.datetime.now()
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
                          area_id = area.id,
                          area_name = area.area_name,
                          status=1,
                          create_time=now,
                          last_updated = now)
            house.save()

        house = House.objects.get(uuid=houseData['id'])

        return house.id

    def saveHouseSold(houseId, data):
        now = timezone.datetime.now()
        today = timezone.datetime.today()
        houseSold = HouseSold()
        try:
            houseSold = HouseSold.objects.get(house_id=houseId, date=today)
            houseSold.price = float(data['price4hour'])
            houseSold.special_price=float(data['specialPrice']) if data['specialPrice'] else 0
            houseSold.status=int(data['sold'])
            if((houseSold.status == 1) and (not houseSold.last_updated)):
                houseSold.last_updated = now
            houseSold.save()
        except houseSold.DoesNotExist:
            houseSold = HouseSold(house_id=houseId,
                                  date=today,
                                  price=float(data['price4hour']),
                                  special_price=float(data['specialPrice']) if data['specialPrice'] else 0,
                                  status=int(data['sold']),
                                  last_updated=now)
            houseSold.save()


    def saveAllHouses(data):
        for item in data:
            houseId = HouseService.saveHouse(item)
            HouseService.saveHouseSold(houseId, item)

    def listAllHouses(self):
        return House.objects.all()

    def listHousesSoldByDate(dateStr):
        return HouseSold.objects.filter(date=dateStr)

    def listHousesSoldBetweenDates(dateFrom, dateTo):
        return House.objects.filter(date__gte=dateFrom, date__lte=dateTo)

    def listAllAreas(self):
        return Area.objects.all()

    def getOrSaveAreaByLid(lid):
        area = Area(lid=lid, area_name='新增')
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