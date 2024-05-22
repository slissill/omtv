from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from omtv.models import Channel, Programme, Import

'''
Dans pythonanywhere pour configurer la task il faut saisir : 
source /home/slissill/.virtualenvs/venv/bin/activate && python /home/slissill/omtv/manage.py import_xml_data

'''


class Command(BaseCommand):
    help = 'Import XML data from XMLTV'

    def handle(self, *args, **kwargs):
        main()

def main():
    
    #----  Log Import  -----------------------------------------------------------------
    # Log Import
    new_import = Import(start=timezone.now(), count_before=Programme.objects.count())
    new_import.save()
    #-----------------------------------------------------------------------------------

    url = "https://xmltvfr.fr/xmltv/xmltv_tnt.xml"
    response = requests.get(url)
    xml_content = response.content
    root = ET.fromstring(xml_content)

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
            channel = Channel.objects.get(pk = item.get('channel')), 
            start = start_time, 
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

    #----  Log Import  -----------------------------------------------------------------
    # Log Import
    new_import.end = timezone.now()
    new_import.count_after =  Programme.objects.count()
    new_import.save()    
    #-----------------------------------------------------------------------------------

def get_xml_text(item, balise_name, arg=None):
    node = item.find(balise_name)
    if node is None:
        return ""
    else:
        return node.text if arg is None else node.get(arg)

def get_xml_date(s):
    s = s.replace("+0200", "+0000")
    return datetime.strptime(s, '%Y%m%d%H%M%S %z')