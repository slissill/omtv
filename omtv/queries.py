from .models import Programme
from django.db import transaction
from datetime import datetime

def overlapping_programmes(from_date=None):
    programmes = Programme.objects.all()
    ids_deja_presents = set()
    chevauchements = []
    overlaps = []
    num_paquet = 0
    from_date2 = datetime(1900, 1, 1) if not from_date else from_date
    
    with transaction.atomic():

        for programme in programmes:

            if programme.id in ids_deja_presents: continue            
            
            overlapping_set = Programme.objects.filter(
                title=programme.title, 
                channel_id=programme.channel_id, 
                start__lt=programme.stop, 
                stop__gt=programme.start, 
                pdate__gte=from_date2
                ).exclude(pk=programme.pk)
            
            if overlapping_set.exists():
                num_paquet += 1                
                chevauchements.append({'programme': programme, 'num_paquet': num_paquet})
                ids_deja_presents.add(programme.id)
                for p in overlapping_set:
                    chevauchements.append({'programme': p, 'num_paquet': num_paquet})
                    ids_deja_presents.add(p.id) 


        for i in range(1, num_paquet + 1): 
            programmes_du_paquet = [p['programme'] for p in chevauchements if p['num_paquet'] == i]
            max_updated_at_programme = max(programmes_du_paquet, key=lambda p: p.updated_at)
            overlaps.append({
                    'num_paquet': i,
                    'programmes': [
                        {
                            'id': p.id,
                            'title': p.title,
                            'channel_id':p.channel_id, 
                            'start': p.start,
                            'updated_at': p.updated_at,
                            'to_delete': 0 if p == max_updated_at_programme else 1
                        } for p in programmes_du_paquet
                    ]
                })
        
    return overlaps

def overlapping_programmes_to_delete(from_date=None):
    overlaps = overlapping_programmes(from_date)
    to_delete_ids = []

    for overlap in overlaps:
        for programme in overlap['programmes']:
            if programme['to_delete'] == 1:
                to_delete_ids.append(programme['id'])

    return to_delete_ids

 