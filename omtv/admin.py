from django.contrib import admin
from .models import Channel, Programme

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')

class ProgrammeAdmin(admin.ModelAdmin):
    
    #********  config en mode liste ********************
    list_filter = ('genre', 'channel', )
    search_fields = ['title', 'genre']
    list_per_page = 50
    readonly_fields = ['created_at', 'updated_at']
    
    #******** config en mode fiche *********************
    #fields = ['title', 'genre', 'pdate', 'start', 'stop']              # <= on ne peut pas faire les 2 en meme temps
    fieldsets = [
        ('Timing', {'fields' : ['pdate', 'start', 'stop']}), 
        ('Autres', {'fields' : ['title', 'genre']}), 
        ('Audit', {'fields' : ['created_at', 'updated_at']}), 
    ]


# Register your models here.
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Programme, ProgrammeAdmin)


