import requests  #pip install requests
from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from datetime import datetime, date


def index(request):    
    return HttpResponse("Hello World")


def get_xml_text(item, balise_name, arg = None):
        node = item.find(balise_name)
        if node is None:
                return ""
        else :
                return node.text if arg is None else node.get(arg)

def get_xml_date(s):return datetime.strptime(s, '%Y%m%d%H%M%S %z')

def comparer_par_start(programme):
    return programme.start

def programmes(request):

    #******************************************************
    # Class Programme
    #******************************************************
    class Programme:
        def __init__(self, id, title, genre, channel, start, stop, description, image, channel_image):
            self.id = id
            self.title = title
            self.genre = genre
            self.channel = channel
            self.start = start
            self.stop = stop
            self.description = description 
            self.image = image
            self.channel_image = channel_image

        def __str__(self): return self.channel_image 

        @property
        def hdeb(self): return self.start.strftime("%H:%M")
        @property
        def hfin(self): return self.stop.strftime("%H:%M")        

        @property
        def duree(self):
            difference = self.stop - self.start
            heures, seconds = divmod(difference.seconds, 3600)
            minutes, _ = divmod(seconds, 60)
            duree_formatee = f"{heures:02}h{minutes:02}"
            return duree_formatee[1:]

    id = 1
    url = "https://xmltvfr.fr/xmltv/xmltv_tnt.xml"
    response = requests.get(url)
    xml_content = response.content
    root = ET.fromstring(xml_content)
    dic_channels = {}
    items = root.findall('.//channel')
    for item in items:
        id_channel = item.get('id')
        display_name = get_xml_text(item, "display-name") 
        image = get_xml_text(item, "icon", "src")
        dic_channels[id_channel] = (display_name, image)


    items = root.findall('.//programme[category="Film"]')
    programmes = []
    date_time_now = datetime.now()
    channels_out = ["ParisPremiere", "CanalPlus", "CanalPlusCinema"]

    for item in items:

        # filtre sur la date du jour
        start = get_xml_date(item.get('start'))
        if start.strftime("%Y%m%d") != date_time_now.date().strftime("%Y%m%d") or start.hour < 20 : continue
        
        # Info de channel depuis le dico des channeles
        id_channel = item.get('channel')
        channel = dic_channels[id_channel][0]
        channel_image = dic_channels[id_channel][1]
        
        #channel = item.get('channel').replace(".fr", "") 

        # filtre sur les channels
        if channel in channels_out : continue

        # recupère les autres propriétés
        stop = get_xml_date(item.get('stop'))
        title = get_xml_text(item, "title") 
        genre = (item.findall("./category")[1].text).replace("Film", "")
        description = get_xml_text(item, "desc")
        image = get_xml_text(item, "icon", "src")
        p = Programme(id, title, genre, channel, start, stop, description, image, channel_image)
        programmes.append(p)
        
        #print (p)

        id += 1
        if id > 50 : break
    
    programmes.sort(key=comparer_par_start)
    context = {"programmes" : programmes, 
               "view" : request.GET.get('view', 'accordeon')}
    return render(request, 'omtv/programmes.html', context)
