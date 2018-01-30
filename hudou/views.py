import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

# Create your views here.

def index(request):
    #hostname = os.getenv('HOSTNAME', 'unknown')
    #PageView.objects.create(hostname=hostname)

    return render(request, 'index.html',{
        'amount': 1807.47,
        'totalRooms': 65,
        'soldRooms': 13,
        'rentPercentage': '21%',
    })
    '''
    return render(request, 'hudou/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })
    '''

def health(request):
    return render(request,'index.html')
    #return HttpResponse(PageView.objects.count())
