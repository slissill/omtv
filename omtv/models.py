from django.db import models
import json

'''
Pwd for mysql on pythonanywhere : beatles?pa

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Pour préparer les instructions sql
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python manage.py makemigrations omtv

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Pour Consulter les actions prévues
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python manage.py sqlmigrate omtv 0001

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Pour Modififier la base
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python manage.py migrate

'''

#******************************************************
# Class Channel
#******************************************************
class Channel(models.Model):
    code = models.CharField(max_length=50, verbose_name="Code", primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Chaine")
    visuel = models.CharField(max_length=500, verbose_name="Visuel")
    sort = models.IntegerField(default=0, verbose_name="Tri")
    class Meta:
        verbose_name = "Chaine"
        verbose_name_plural = "Chaines"
        ordering = ['sort']

    def __str__(self): return self.name

    @classmethod
    def create_or_update(cls, **kwargs): return cls.objects.get_or_create(**kwargs)


#******************************************************
# Class Programme
#******************************************************
class Programme(models.Model):
    # Comme je ne lui précise pas de PK, le champ id (pk) sera automatiquement généré
    start = models.DateTimeField(verbose_name="Début")    
    stop = models.DateTimeField(verbose_name="Fin")
    pdate = models.DateField(verbose_name="Date")
    title = models.CharField(max_length=300, verbose_name="Titre")
    description = models.CharField(max_length=1000, verbose_name="Description")
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    genre = models.CharField(max_length=100, verbose_name="Genre")
    visuel = models.CharField(max_length=500, verbose_name="Visuel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='fk_Programme_Channel')
    json_status = models.IntegerField(default=0, verbose_name="Json Status")
    json_datas = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        constraints = [models.UniqueConstraint(fields=['start', 'channel'], name='unique_programme_key')]        
        ordering = ['start', 'channel']
    
    def __str__(self): return f"{self.pdate} - {self.title}"

    @classmethod
    def create_or_update(cls, **kwargs): return cls.objects.get_or_create(**kwargs)

    @property
    def xdate(self): return self.start.date()

    @property
    def date_str(self): return self.start.strftime("%Y-%m-%d")
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
    
    @property
    def hdeb_and_duree(self): return f"{self.hdeb} {self.duree}"
    @property
    def tranche(self):
        if self.hdeb >= "00:00" and self.hdeb <= "05:59" :      return "Nuit"
        elif self.hdeb >= "06:00" and self.hdeb <= "11:59" :    return "Matin"
        elif self.hdeb >= "12:00" and self.hdeb <= "19:59" :    return "Après-midi"
        elif self.hdeb >= "20:00" and self.hdeb <= "21:29" :    return "Soirée 1"
        else :                                                  return "Soirée 2"

    def get_json_data(self, prop):
        if self.json_datas and prop in self.json_datas:           
            return self.json_datas[prop]
        else:
            return ""

    @property
    def imdb_id(self): return self.get_json_data('imdb_id')
    @property
    def imdb_url(self): return f"https://www.imdb.com/title/{self.get_json_data('imdb_id')}" 
    @property
    def homepage(self): return self.get_json_data('homepage')
    @property
    def poster_path(self): return self.get_json_data('poster_path')
    @property
    def poster_url_original(self): return f"https://image.tmdb.org/t/p/original{self.get_json_data('poster_path')}" 
    @property
    def poster_url_w500(self): return f"https://image.tmdb.org/t/p/w500{self.get_json_data('poster_path')}" 
    @property
    def release_date(self): return self.get_json_data('release_date')
    @property
    def release_year(self): return self.release_date.split('-')[0] if self.release_date else ''    
    @property
    def vote_average(self): return self.get_json_data('vote_average')
    @property
    def popularity(self): return self.get_json_data('popularity')
    @property
    def vote_count(self): return self.get_json_data('vote_count')
    @property
    def countries(self):
        if self.json_datas and 'origin_country' in self.json_datas:           
            return ", ".join(self.json_datas['origin_country'])
        else:
            return ""
    @property
    def year_and_countries(self): return f"{self.release_year} - {self.countries}"

    @property
    def carousel(self):
        sources = []        
        if self.poster_url_w500:
            sources.append(self.poster_url_w500)
        if self.visuel:
            sources.append(self.visuel)

        carousel_items = [{'index': idx + 1, 'url': url} for idx, url in enumerate(sources)]
        return carousel_items

    def actors(self):
        if self.json_datas and 'actors' in self.json_datas:           
            return ", ".join(self.json_datas['actors'][:4])
        else:
            return ""


    # @property
    # def actors(self):
    #     data = json.loads(self.json_datas)
    #     return data.get('actors', [])
    # @property
    # def genres(self):
    #     data = json.loads(self.json_datas)
    #     return data.get('genres', [])
    # @property


#******************************************************
# Class Import
#******************************************************
class Import(models.Model):
    # Comme je ne lui précise pas de PK, le champ id (pk) sera automatiquement généré
    start = models.DateTimeField(verbose_name="Début", primary_key=True)
    end = models.DateTimeField(verbose_name="Fin", blank=True, null=True)
    count_before = models.IntegerField (verbose_name="Count avant")
    count_after = models.IntegerField (verbose_name="Count après", blank=True, null=True)

    class Meta:
        verbose_name = "Import"
        verbose_name_plural = "Imports"        
        ordering = ['-start']
    
    def __str__(self):
        start_str = self.start.strftime("%Y-%m-%d %H:%M:%S")
        if self.end:
            duration = (self.end - self.start).total_seconds()
            return f"{start_str} : {round(duration, 1)} secondes, {self.count_after - self.count_before} programmes"
        else:
            return f"{start_str} - No end time"