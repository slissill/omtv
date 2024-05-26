from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from omtv.models import Channel, Programme, Import
from omtv.import_xml import import_xml
from omtv.import_imdb_web import get_json_from_title as get_json_from_title_web
from omtv.import_imdb_api import get_json_from_title as get_json_from_title_api
from imdb import IMDb
from omtv.queries import *
'''

Dans pythonanywhere pour configurer la task il faut saisir : 
source /home/slissill/.virtualenvs/venv/bin/activate && python /home/slissill/omtv/manage.py maj_bdd

Dans Vs Code (en VENV), se positionner sur le dossier où il y a Manage.py (C:\ZDEPOT\omtv>) et exécuter
python manage.py maj_bdd

'''

class Command(BaseCommand):
    help = 'Import XML data from XMLTV'
    def handle(self, *args, **kwargs):
        main()

def main():
    
    # Log Import START
    new_import = Import(start=timezone.now(), count_before=Programme.objects.count())
    new_import.save()

    # Import des programmes TNT
    min_max_times = [None, None]
    import_xml(min_max_times)    
    min_start, max_start = min_max_times    
    
    # Récupération des extras-info depuis IMDB
    current_date = datetime.now()
    programmes = Programme.objects.filter(json_status=0, pdate__gte=current_date)
    for p in programmes:
        json = {}
        p.json_status = get_json_from_title_web (p.title, json, light=True)
        #p.json_status = get_json_from_title_api (p.title, json, inst_imdb)
        p.json_datas = json
        p.save()

    
    # Programmes en doublon (chevauchement) : on delete (les vieilles données)
    ids_to_delete = overlapping_programmes_to_delete(min_start.date())
    programmes_a_supprimer = Programme.objects.filter(id__in=ids_to_delete)
    programmes_a_supprimer.delete()


    # Log Import END
    new_import.end = timezone.now()
    new_import.count_after =  Programme.objects.count()
    new_import.deleted = len(ids_to_delete)
    new_import.min_start = min_start
    new_import.max_start = max_start
    new_import.save()
