from django.db import models

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