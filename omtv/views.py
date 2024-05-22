import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .utils import maj_db
from .models import Programme, Channel
from datetime import date, datetime, timedelta
from django.db.models import Count, F
from itertools import groupby

import plotly.graph_objs as go
from plotly.offline import plot

from django.contrib.auth.decorators import login_required

# import django
# import sys
# from django.db.models import Q
# from django.db.models import Count
# from django.http import JsonResponse
import json

#return HttpResponse("update_db_r") 


def print_request(request):
    print ("**************************************")
    print (f"*********** {request.method} *********************")
    print ("**************************************")
    if request.method == "POST": print("POST data:", request.POST)
    print("GET data:", request.GET)
    print("Cookies:", request.COOKIES)
    print ("**************************************")


def home(request):    
    return render(request, 'omtv/home.html')

def update_db(request):  
    maj_db (request.GET.get('mode', 's'))
    return redirect ("omtv:programmes")

@login_required
def dashboard(request):
    return render(request, 'omtv/dashboard.html')



def get_graphic_2d(datas, title):
    # Using plotly library
    labels = []
    values = []
    for item in datas:
        labels.append(item['lbl'])
        values.append(item['cnt'])

    trace = go.Bar(x=labels, y=values)
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace], layout=layout)
    return plot(fig, output_type='div', include_plotlyjs=False)

def stats(request):
    
    programmes_count = Programme.objects.count()
    dates_count = Programme.objects.values('pdate').distinct().count

    div_count_by_date = get_graphic_2d(Programme.objects.values(lbl=F('pdate')).annotate(cnt=Count('pdate')).order_by('pdate'), 'Nombre de films par date')
    div_count_by_channel = get_graphic_2d(Channel.objects.values(lbl=F('name')).annotate(cnt=Count('fk_Programme_Channel')).order_by('-cnt'), 'Nombre de films par channel')
    div_count_by_genre = get_graphic_2d(Programme.objects.values(lbl=F('genre')).annotate(cnt=Count('genre')).order_by('-cnt'), 'Nombre de films par genre')

    context = {
        'programmes_count' : programmes_count,
        'dates_count' : dates_count,
        'div_count_by_date': div_count_by_date, 
        'div_count_by_channel' : div_count_by_channel, 
        'div_count_by_genre' : div_count_by_genre,
        }
    return render(request, 'omtv/stats.html', context)    

def get_dates(selected_date):

    dates = Programme.objects.order_by('pdate').values_list('pdate', flat=True).distinct()
    jours_semaine = ['lun', 'mar', 'mer', 'jeu', 'ven', 'sam', 'dim']
    today = datetime.now().date()
    today_plus = today  + timedelta(days=3)
    formatted_dates = [
                            {'name': f"{jours_semaine[date.weekday()]} {date.day}", 
                             'code': date.strftime('%Y%m%d'),  
                             'selected': date.strftime('%Y%m%d') == selected_date, 
                            } for date in dates if date >= today and date < today_plus
                    ]
    #for date in dates if date >= datetime.now().date() - timedelta(days=1)
    return formatted_dates

def programmes(request):
    print_request(request)
    
    if request.method == "POST":
        seleted_date = request.POST.get('crit_date')
    else:
        seleted_date = datetime.now().date().strftime('%Y%m%d')

    cookie = request.COOKIES.get("channels")
    channels = []
    if cookie == None: 
        for item in Channel.objects.all(): channels.append(item.code)
    else:    
        channels = json.loads(cookie)


    progs = Programme.objects.filter(
        pdate = datetime.strptime(seleted_date, "%Y%m%d"), 
        start__time__gte='20:00', 
        channel__in=channels
        ).order_by('start', 'channel__sort')
    
    # Regoupemement par tranche-horaire
    grouped_programmes = {}
    for tranche, programmes_in_tranche in groupby(progs, key=lambda x: x.tranche):
        grouped_programmes[tranche] = list(programmes_in_tranche)

    visuel = request.COOKIES.get("visuel") == "true"

    context = {"grouped_programmes": grouped_programmes,
               "dates" : get_dates(seleted_date), 
               "visuel" : visuel}
    return render(request, 'omtv/programmes.html', context)


def preferences(request):    
    print_request(request)
    if request.method == "POST":
        
        if 'chk_visuel' in request.POST:
             visuel = True
        else:
             visuel = False


        #visuel = request.POST("chk_visuel", False)
        channels = request.POST.getlist("chk_channel")
        response = redirect ("omtv:programmes")

        duration = 7*24*60*60 #7 jours
        response.set_cookie("visuel", json.dumps(visuel), max_age=duration, samesite=None)
        response.set_cookie("channels", json.dumps(channels), max_age=duration, samesite=None)


        return response
        
    elif request.method == "GET":

        visuel = request.COOKIES.get("visuel") == "true"

        all_channels = Channel.objects.all()        
        channel_codes = [channel.code for channel in all_channels]
        cookie_channels = request.COOKIES.get("channels")
        if cookie_channels != None: channel_codes = json.loads(cookie_channels)
        channels = [
                    {   'code'      : channel.code, 
                        'name'      : channel.name,  
                        'checked'   : channel.code in channel_codes,
                    } for channel in all_channels
                   ]
        context = { 
            "visuel" : visuel, 
            "channels" : channels
            }
        return render(request, 'omtv/preferences.html', context)

