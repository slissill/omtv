import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from omtv.models import Channel, Programme


def import_xml(min_max_times):

    url = "https://xmltvfr.fr/xmltv/xmltv_tnt.xml"
    response = requests.get(url)
    xml_content = response.content
    root = ET.fromstring(xml_content)

    # *****************************************
    # Pour les stats de l'import
    # *****************************************    
    items = root.findall('.//programme')
    start_times = [datetime.strptime(program.attrib['start'][:14], "%Y%m%d%H%M%S") for program in root.findall('.//programme')]
    min_max_times[0] = min(start_times)
    min_max_times[1] = max(start_times)

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
        title = get_xml_text(item, "title")         

        # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # print (f"{idx}/{cnt} => {title}")
        # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        categories = item.findall("./category")  # Récupère tous les éléments <category>
        genre = categories[1].text.replace("Film", "") if len(categories) > 1 else ""

        start_time = get_xml_date(item.get('start'))
        programme_db, created = Programme.create_or_update(
            channel = Channel.objects.get(pk = item.get('channel')), 
            start = start_time, 
            defaults = {
                'stop'          : get_xml_date(item.get('stop')), 
                'pdate'         : start_time.date(),
                'title'         : title, 
                'description'   : get_xml_text(item, "desc"),                                
                'category'      : categories[0].text if categories else "",
                'genre'         : genre, 
                'visuel'        : get_xml_text(item, "icon", "src"),                                    
            }
        )
    

#********************************************************************
# XMl Helper : get_xml_text
#********************************************************************
def get_xml_text(item, balise_name, arg=None):
    node = item.find(balise_name)
    if node is None:
        return ""
    else:
        return node.text if arg is None else node.get(arg)
    
#********************************************************************
# XMl Helper : get_xml_date
#********************************************************************
def get_xml_date(s):
    s = s.replace("+0200", "+0000")
    return datetime.strptime(s, '%Y%m%d%H%M%S %z')
