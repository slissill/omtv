import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date
from .models import Programme
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
        id_channel = item.get('id')        
        if id_channel in ["ParisPremiere.fr", "CanalPlus.fr", "CanalPlusCinema.fr"] : continue
        display_name = get_xml_text(item, "display-name") 
        image = get_xml_text(item, "icon", "src")
        dic_channels[id_channel] = (display_name, image)

    return dic_channels

def get_programmes(methode):

    if methode == "s":     root = get_xml_root_static()
    elif methode == "r": root = get_xml_root_requests()
    elif methode == "u":   root = get_xml_root_urllib()

    dic_channels = get_channels(root)
    items = root.findall('.//programme[category="Film"]')
    programmes = []

    for item in items:
        id = len(programmes) + 1
        add_programme(programmes, item, dic_channels)

    programmes.sort(key=comparer_par_start)
    return programmes

def add_programme(programmes, item, dic_channels):
    
    # Filtre sur la date du jour
    start = get_xml_date(item.get('start'))
    id_channel = item.get('channel')

    # EXIT dans ces cas là :
    if start.strftime("%Y%m%d") != datetime.now().date().strftime("%Y%m%d") or start.hour < 20 : return    
    if id_channel not in dic_channels: return
    
    channel = dic_channels[id_channel][0]
    channel_image = dic_channels[id_channel][1]

    # Recupère les autres propriétés
    stop = get_xml_date(item.get('stop'))
    title = get_xml_text(item, "title") 
    genre = (item.findall("./category")[1].text).replace("Film", "")
    description = get_xml_text(item, "desc")
    image = get_xml_text(item, "icon", "src")

    p = Programme(len(programmes)+1, title, genre, channel, start, stop, description, image, channel_image)
    programmes.append(p)
    

def get_xml_text(item, balise_name, arg = None):
        node = item.find(balise_name)
        if node is None:
                return ""
        else :
                return node.text if arg is None else node.get(arg)

def get_xml_date(s):return datetime.strptime(s, '%Y%m%d%H%M%S %z')

def comparer_par_start(programme):
    return programme.start

