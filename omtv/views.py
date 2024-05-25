from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .management.commands.maj_bdd import main as maj_bdd
from .models import Programme, Channel, Import
from .import_imdb_web import get_json_from_title
from datetime import date, datetime, timedelta
from django.db.models import Count, F, Max
from itertools import groupby
import plotly.graph_objs as go
from plotly.offline import plot
from django.contrib.auth.decorators import login_required
import json
from json2html import *
import requests
from django.http import JsonResponse
from django.conf import settings

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

def import_xml_data(request):  
    maj_bdd()
    return redirect ("omtv:programmes")

@login_required
def dashboard(request): 
    last_imports = Import.objects.all()[:10]
    return render(request, 'omtv/dashboard.html', {'last_imports' : last_imports})



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

    max_updated_at = Programme.objects.aggregate(max_updated_at=Max('updated_at'))['max_updated_at']


    programmes_count = Programme.objects.count()
    dates_count = Programme.objects.values('pdate').distinct().count

    div_count_by_date = get_graphic_2d(Programme.objects.values(lbl=F('pdate')).annotate(cnt=Count('pdate')).order_by('pdate'), 'Nombre de films par date')
    div_count_by_channel = get_graphic_2d(Channel.objects.values(lbl=F('name')).annotate(cnt=Count('fk_Programme_Channel')).order_by('-cnt'), 'Nombre de films par channel')
    div_count_by_genre = get_graphic_2d(Programme.objects.values(lbl=F('genre')).annotate(cnt=Count('genre')).order_by('-cnt'), 'Nombre de films par genre')

    context = {
        'programmes_count' : programmes_count,
        'dates_count' : dates_count,
        'max_updated_at' : max_updated_at, 
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


def get_imdb_datas(request):    
    if request.method == 'GET':
        title = request.GET.get('title', 'inception')
        bln_light = request.GET.get('light', '0') != '0'
        bln_jsonoutput = request.GET.get('jsonoutput', '0') != '0'
        json_datas = {}
        json_status = get_json_from_title(title, json_datas, light=bln_light) 
        
        if (json_status == 1):
            if bln_jsonoutput == True:
                return JsonResponse({'movie': json_datas})
            else:
                replace_jpg_urls(json_datas)
                html_content = json2html.convert(json = json_datas, clubbing=True, encode=False, table_attributes='border="1"')
                html_content = html_content.replace("#DEBUT#", "<img width=300 src='https://image.tmdb.org/t/p/original")
                html_content = html_content.replace("#FIN#", "></img>")
                return render(request, 'omtv/imdb_datas.html', {'html_content': html_content, 'title' : title})            

    return JsonResponse({'Failed': title}, status=404)


def replace_jpg_urls(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and (value.endswith('.jpg') or value.endswith('.png')):
                data[key] = f'#DEBUT#{value}#FIN#'
            elif isinstance(value, (dict, list)):
                replace_jpg_urls(value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, str) and (item.endswith('.jpg') or item.endswith('.png')):
                data[index] = f'#DEBUT#{item}#FIN#'
            elif isinstance(item, (dict, list)):
                replace_jpg_urls(item)

def videos(request):
    if request.method == 'GET':
        id = request.GET.get('id', '0')
        crit_video_type=request.GET.get('type')
        crit_video_key=request.GET.get('key')
        
        programme = get_object_or_404(Programme, id=id)

        if crit_video_type == None:
            videos_types = programme.videos_types
            crit_video_type = next(iter(videos_types))  # Premier type de vidéo
            
        if crit_video_key == None:
            filtered_videos = [video for video in programme.videos if video['type'] == crit_video_type]
            crit_video_key = filtered_videos[0]['key'] # Premiere vidéo du type

        context = {
            'programme': programme, 
            'crit_video_type' : crit_video_type, 
            'crit_video_key' : crit_video_key, 
            }
        return render(request, 'omtv/videos.html', context)

    return JsonResponse({'Failed': 'Failed'}, status=404)
