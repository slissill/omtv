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
from .queries import *
import locale
from .utils.spotify_client import get_albums_by_artist

###### django_user_agents #################################
#pip install pyyaml ua-parser user-agents django-user-agents
# MIDDLEWARE[...'django_user_agents.middleware.UserAgentMiddleware',]
from django_user_agents.utils import get_user_agent
############################################################

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

    action = request.GET.get('action')
    nbr_suppression = 0  # Variable pour stocker le nombre de suppressions
    if action:
        if (action == "drop_dates") :
            date_to_compare = datetime.today().strftime("%Y-%m-%d")
            nbr_suppression, _ = Programme.objects.filter(pdate__gte=date_to_compare).delete()  #retourne un tuple

    last_imports = Import.objects.all()[:10]

    context = {        
        'last_imports' : last_imports,
        'nbr_suppression': nbr_suppression,
        }
    return render(request, 'omtv/dashboard.html', context)



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

    today = datetime.now().date()
    today_plus = today  + timedelta(days=4)
    dates = Programme.objects.filter(pdate__range=[today, today_plus], start__time__gte='20:00').order_by('pdate').values_list('pdate', flat=True).distinct()
    jours_semaine = ['lun', 'mar', 'mer', 'jeu', 'ven', 'sam', 'dim']


    formatted_dates = [
                            {'name': jours_semaine[dt.weekday()],
                             'code': dt.strftime('%Y%m%d'),
                             'selected': dt.strftime('%Y%m%d') == selected_date,
                            } for dt in dates
                    ]
    return formatted_dates

def old_programmes(request):
    print_request(request)

    selected_date = datetime.now().date().strftime('%Y%m%d')
    if request.method == "GET":
        selected_date = request.GET.get('date', selected_date)


    progs = get_programmes_on_date (request, datetime.strptime(selected_date, "%Y%m%d"))

    # Regoupemement par tranche-horaire
    grouped_programmes = {}
    for tranche, programmes_in_tranche in groupby(progs, key=lambda x: x.tranche):
        grouped_programmes[tranche] = list(programmes_in_tranche)

    visuel = request.COOKIES.get("visuel") == "true"

    context = {"grouped_programmes": grouped_programmes,
               "dates" : get_dates(selected_date),
               "visuel" : visuel,
               "device" : get_device(request)
               }
    return render(request, 'omtv/old_programmes.html', context)

def get_device(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile : return "mob"
    elif user_agent.is_tablet : return "tab"
    else: return "pc"


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
                return render(request, 'omtv/json2html.html', {'html_content': html_content, 'title' : title})

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

def debug_datas(request):
    overlapping_programmes_data = overlapping_programmes()
    ids_to_delete = overlapping_programmes_to_delete()
    ids_to_delete_str = ", ".join(str(id) for id in ids_to_delete)
    html_content = f"<strong>IDs to delete:</strong> {ids_to_delete_str}<br><br>"

    for overlap in overlapping_programmes_data:
        html_content += json2html.convert(json=overlap) + "<br><br>"
    return render(request, 'omtv/json2html.html', {'html_content': html_content, 'title': 'Chevauchements'})

def my_carousel(request):
    if request.method == 'GET':
        id = request.GET.get('id', '0')

        programme = get_object_or_404(Programme, id=id)

        context = {
            'programme': programme,
            }
        return render(request, 'omtv/my_carousel.html', context)

def programmes(request):
    print_request(request)

    selected_date = datetime.now().strftime('%Y%m%d')
    if request.method == "GET":
        selected_date = request.GET.get('date', selected_date)

    programmes = get_programmes_on_date (request, datetime.strptime(selected_date, "%Y%m%d"))

    context = {"programmes" : programmes,
               "dates" : get_dates(selected_date),
               "device" : get_device(request)
               }
    return render(request, 'omtv/programmes.html', context)

def get_programmes_on_date(request, dat):

    # obtient le filtre pour les channels

    # cookie = request.COOKIES.get("channels")
    # channels = []
    # if cookie == None:
    #     for item in Channel.objects.all(): channels.append(item.code)
    # else:
    #     channels = json.loads(cookie)

    excluded_codes = [
        'CanalPlus.fr',
        'ParisPremiere.fr',
        'CanalPlusSport.fr',
        'CanalPlusCinema.fr',
        'PlanetePlus.fr'
    ]
    channels = []
    for item in Channel.objects.exclude(code__in=excluded_codes):
        channels.append(item.code)

    # Filtre les programmes
    return Programme.objects.filter(pdate = dat, start__time__gte='20:00', channel__in=channels).order_by('start', 'channel__sort')

def programme_fiche(request):
    print_request(request)

    if request.method == 'GET':
        id = request.GET.get('id', '0')

    programme = get_object_or_404(Programme, id=id)

    # Obtient les programmes du meme jour
    programmes = get_programmes_on_date(request, programme.pdate)
    programme_ids = list(programmes.values_list('id', flat=True))
    try:
        current_index = programme_ids.index(int(id))
    except ValueError:
        current_index = None

    id_prev = programme_ids[-1]
    id_next = programme_ids[0]
    if current_index is not None:
        id_pos = f"{current_index + 1} / {len(programme_ids)}"
        if current_index > 0: 
            id_prev = programme_ids[current_index - 1]
        if current_index < len(programme_ids) - 1: 
            id_next = programme_ids[current_index + 1]                

    context = {
        'programme': programme,
        'programmes': programmes,
        'id_pos' : id_pos, 
        'id_prev' : id_prev, 
        'id_next' : id_next,
        'videos_json' : json.dumps(programme.dic_videos)
        }
    return render(request, 'omtv/programme_fiche.html', context)

def rapport(request):
    programmes = Programme.objects.values('title').annotate(count=Count('title')).order_by('-count')    
    context = {"programmes" : programmes,}
    return render(request, 'omtv/rapport.html', context)

def albums_list(request):
    albums = get_albums_by_artist("laylow")
    return render(request, "omtv/albums.html", {"albums": albums})