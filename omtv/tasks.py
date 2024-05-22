import sys
import os

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from omtv.models import Channel, Programme

# https://www.pythonanywhere.com/forums/topic/31949/
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3/28154841#28154841
# https://www.pythonanywhere.com/forums/topic/13787/



def main():

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

if __name__ == "__main__":
    main()

def get_xml_text(item, balise_name, arg = None):
        node = item.find(balise_name)
        if node is None:
                return ""
        else :
                return node.text if arg is None else node.get(arg)

def get_xml_date(s):
    s=s.replace("+0200", "+0000")
    return datetime.strptime(s, '%Y%m%d%H%M%S %z')

