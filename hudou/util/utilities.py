from math import radians, cos, sin, asin, sqrt

from django.utils import timezone
from datetime import datetime, timedelta
import pytz


class Utilities:
    def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r * 1000

cst_tz = pytz.timezone('Asia/Shanghai')
utc_tz = pytz.timezone('UTC')
#tz_name = timezone.now().tzname()

def nowWithChineseTZ():
    return toChineseTZ(timezone.now())

def todayWithChineseTZ():
    return toChineseTZ(timezone.now())


def toChineseTZ(datetime):
    datetime = datetime.replace(tzinfo=utc_tz)
    cst = datetime.astimezone(cst_tz)
    return cst

def dateOfDaysBeforeToday(days):
    today = todayWithChineseTZ()
    return today - timedelta(days=days)