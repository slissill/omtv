import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .utils import maj_db
from .models import Programme, Channel
from datetime import date, datetime, timedelta
from django.db.models import Count


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


def programmes_update(request):
    return render(request, 'omtv/programmes_update.html')

def statistics(request):

    dates_with_program_counts = Programme.objects.values('pdate').annotate(cnt=Count('pdate'))
    
    #channels_with_program_counts = Channel.objects.annotate(program_count=Count('fk_Programme_Channel'))
    channels_with_program_counts = Channel.objects.annotate(cnt=Count('fk_Programme_Channel')).order_by('-cnt')

    genres_with_program_counts = Programme.objects.values('genre').annotate(cnt=Count('genre')).order_by('-cnt')



    context = {
        'dates_with_program_counts' : dates_with_program_counts,
        'channels_with_program_counts' : channels_with_program_counts, 
        'genres_with_program_counts' : genres_with_program_counts, 
        }
    return render(request, 'omtv/statistics.html', context)


def graphics(request):
# Votre logique pour obtenir les données pour le graphique
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 15, 25, 30]

    # Créer un graphique à l'aide de Matplotlib
    plt.plot(x, y)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Titre du graphique')

    # Sauvegarder le graphique dans un fichier
    absolute_path = os.path.join(settings.BASE_DIR, "omtv", "static", "graphics", "graph.png")
    graph_file = absolute_path
    plt.savefig(graph_file)

    # Passer le chemin du fichier au modèle pour l'affichage dans la page HTML


    dates_with_program_counts = Programme.objects.values('pdate').annotate(cnt=Count('pdate'))
    context = {
        'dates_with_program_counts' : dates_with_program_counts,
        'graph_file': graph_file
        }
    return render(request, 'omtv/graphics.html', context)    


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
        pdate = datetime.strptime(seleted_date, "%Y%m%d"), # date.today(),
        start__time__gte='20:00', 
        channel__in=channels
        ).order_by('start', 'channel__sort')
    

    context = {"programmes" : progs, 
               "dates" : get_dates(seleted_date)}
    return render(request, 'omtv/programmes.html', context)

def channels(request):    
    print_request(request)
    if request.method == "POST":
        channels = request.POST.getlist("chk_channel")
        response =  redirect ("omtv:programmes")
        response.set_cookie("channels", json.dumps(channels), max_age=7*24*60*60, samesite=None) #7 jours
        return response
        
    elif request.method == "GET":
        all_channels = Channel.objects.all()        
        channel_codes = [channel.code for channel in all_channels]        
        cookie = request.COOKIES.get("channels")
        if cookie != None: channel_codes = json.loads(cookie)
        channels = [
                    {   'code'      : channel.code, 
                        'name'      : channel.name,  
                        'checked'   : channel.code in channel_codes,
                    } for channel in all_channels
                   ]
        context = {"channels" : channels}
        return render(request, 'omtv/channels.html', context)

