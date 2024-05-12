from django.db import models

'''
Pwd for mysql on pythonanywhere : litswd?pa

=====> pour préparer les instructions sql
python manage.py makemigrations omtv

=====> Pour vérifier les instructions sql qui vont être générées : (0001 étant le prefixe du fichier 0001_initial.py)
python manage.py sqlmigrate omtv 0001

=====> Pour Modififier la base
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

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        constraints = [models.UniqueConstraint(fields=['start', 'channel'], name='unique_programme_key')]        
        ordering = ['start', 'channel']
    
    def __str__(self): return self.title

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
    def tranche(self):
        if self.hdeb >= "00:00" and self.hdeb <= "05:59" :      return "Nuit"
        elif self.hdeb >= "06:00" and self.hdeb <= "11:59" :    return "Matin"
        elif self.hdeb >= "12:00" and self.hdeb <= "19:59" :    return "Après-midi"
        elif self.hdeb >= "20:00" and self.hdeb <= "21:29" :    return "Soirée 1"
        else :                                                  return "Soirée 2"

    



#******************************************************
# Class cls_programme
#******************************************************
class cls_programme:
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