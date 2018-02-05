from django.utils.deprecation import MiddlewareMixin
import requests
import json
import threading

from hudou.services.houseservices import HouseService

class GeneralInvterceptor(MiddlewareMixin):
    def process_request(self,request):
        reqPath = request.path
        if (reqPath == '/'):
            t = threading.Thread(target=saveAccessHistory, args=(request,))
            t.start()

    def process_response(self, request, response):
        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_x_forwarded_for(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for

GET_IP_URL = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?' \
             'resource_id=6006&t=%(ts)s&ie=utf8&oe=utf8&format=json&tn=baidu&' \
             'query=%(ip)s'
def get_ip_source(ip):
    requests.session()
    url = GET_IP_URL%{'ts': 1, 'ip': ip}
    resp = requests.get(url)
    #resp.encoding = 'utf-8'
    jsonData = json.loads(resp.text)
    data = jsonData['data'][0]
    location = data['location']
    #location = '北京市北京市 联通'
    items = location.split()

    city = ''
    provider=''
    if (len(items) == 1):
        city = location
    else:
        city = items[0]
        provider = items[1]
    source = {'city': city, 'provider': provider}
    return source

def saveAccessHistory(request):
    ip = get_client_ip(request)
    xforward = get_x_forwarded_for(request)
    source = get_ip_source(ip)
    data = {'ip': ip, 'xforward': xforward}
    data.update(source)
    HouseService.saveAccessHistory(data)
