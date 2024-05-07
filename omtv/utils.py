import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, date, timezone
from .models import cls_programme, Channel , Programme
from django.conf import settings
import urllib.request


def get_xml_root_static():
    absolute_path = os.path.join(settings.BASE_DIR, "omtv", "static", "xml", "xmltv_tnt.xml")
    tree = ET.parse(absolute_path)
    return tree.getroot()

def get_xml_root_requests():
    url = "https://xmltvfr.fr/xmltv/xmltv_tnt.xml"
    response = requests.get(url)
    xml_content = response.content
    return ET.fromstring(xml_content)

def get_xml_root_urllib():
    url = "https://xmltvfr.fr/xmltv/xmltv_tnt.xml"
    with urllib.request.urlopen(url) as response:
        xml_content = response.read().decode('utf-8')
        return ET.fromstring(xml_content)


def get_channels(root):
    dic_channels = {}
    items = root.findall('.//channel')
    for item in items:

        channel_db, created = Channel.create_or_update(
                code = item.get('id'), 
                name = get_xml_text(item, "display-name"), 
                visuel = get_xml_text(item, "icon", "src"))



        id_channel = item.get('id')        
        if id_channel in ["ParisPremiere.fr", "CanalPlus.fr", "CanalPlusCinema.fr"] : continue
        display_name = get_xml_text(item, "display-name") 
        image = get_xml_text(item, "icon", "src")
        dic_channels[id_channel] = (display_name, image)


    return dic_channels

def maj_db(mode):
    if mode == "s":     root = get_xml_root_static()
    elif mode == "r":   root = get_xml_root_requests()
    elif mode == "u":   root = get_xml_root_urllib()

    # *****************************************
    # CHANNELS 
    # *****************************************
    items = root.findall('.//channel')
    idx = 0
    for item in items:
        idx += 1 
        channel_db, created = Channel.create_or_update(
                code = item.get('id'), 
                name = get_xml_text(item, "display-name"), 
                visuel = get_xml_text(item, "icon", "src"), 
                sort = idx
                )
                

    # *****************************************
    # PROGRAMMES
    # *****************************************
    items = root.findall('.//programme[category="Film"]')
    for item in items:
        start_time = get_xml_date(item.get('start'))
        programme_db, created = Programme.create_or_update(
            channel  = Channel.objects.get(pk = item.get('channel')), 
            start    = start_time, 
            defaults = {
                    'stop'          : get_xml_date(item.get('stop')), 
                    'pdate'         : start_time.date(),
                    'title'         : get_xml_text(item, "title"), 
                    'description'   : get_xml_text(item, "desc"),                                
                    'category'      : item.findall("./category")[0].text, 
                    'genre'         : (item.findall("./category")[1].text).replace("Film", ""), 
                    'visuel'        : get_xml_text(item, "icon", "src"),                                    
                    }
            ) 

# def get_programmes(methode):
#     #if start.strftime("%Y%m%d") != datetime.now().date().strftime("%Y%m%d") or start.hour < 20 : return    
#     #return Programme.objects.filter(day = crit_day, category = crit_category, channel__channel_id__in=channels).order_by('channel__sort')
#     #return Programme.objects.filter(start > datetime.now()).order_by('start')
#     #return Programme.objects.filter(category = "Film").order_by('start')
#     return Programme.objects.order_by('start')


def get_xml_text(item, balise_name, arg = None):
        node = item.find(balise_name)
        if node is None:
                return ""
        else :
                return node.text if arg is None else node.get(arg)

def get_xml_date(s):
    s=s.replace("+0200", "+0000")
    return datetime.strptime(s, '%Y%m%d%H%M%S %z')

def comparer_par_start(programme):
    return programme.start

