import os
import datetime
from hudou.model.valueobjects import House, HouseSold, Area
from hudou.services.houseservices import HouseService

def getTodayReportSummary():
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
        key = 'areaId-' + str(houseDetail.area_id)
        areaCountData = soldHouseAreaCountMap.get(key, None)
        if(not areaCountData):
            areaCountData = {'areaId': houseDetail.area_id,
                             'areaName': houseDetail.area_name,
                             'count': 1,
                             'soldCount': 0}
        else:
            areaCountData['count'] = areaCountData['count'] + 1
            soldHouseAreaCountMap[key] = areaCountData

        if (housesold.status == 1):
            sold = sold + 1
            if (housesold.special_price):
                price = housesold.special_price
            else:
                price = housesold.price * 0.88
            amount = amount + price

            areaCountData = soldHouseAreaCountMap.get(key, None)
            if (not areaCountData):
                areaCountData = {'areaId': houseDetail.area_id,
                                 'areaName': houseDetail.area_name,
                                 'count': 1,
                                 'soldCount': 1}
            else:
                areaCountData['soldCount'] = areaCountData['soldCount'] + 1
            soldHouseAreaCountMap[key] = areaCountData

    summary = {'total': total, 'sold': sold, 'amount': round(amount, 2), 'soldPercent': round(sold/float(total), 2),
               'soldHouseAreas': soldHouseAreaCountMap}

    return summary