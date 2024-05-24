from django.contrib import admin
from .models import Channel, Programme, Import

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')

class ProgrammeAdmin(admin.ModelAdmin):
    
    #********  config en mode liste ********************
    list_filter = ('pdate', 'json_status', 'genre', 'channel', )
    search_fields = ['title', 'genre']
    list_per_page = 50
    readonly_fields = ['created_at', 'updated_at']
    
    #******** config en mode fiche *********************
    #fields = ['title', 'genre', 'pdate', 'start', 'stop']              # <= on ne peut pas faire les 2 en meme temps
    fieldsets = [
        ('Timing', {'fields' : ['pdate', 'start', 'stop']}), 
        ('Autres', {'fields' : ['title', 'genre', 'json_status', 'json_datas']}), 
        ('Audit', {'fields' : ['created_at', 'updated_at']}), 
    ]

class ImportAdmin(admin.ModelAdmin):
    # list_display = ('start', 'end', 'count_before', 'count_after')
    list_filter = ('start', 'end')
    search_fields = ('start',)
    date_hierarchy = 'start'
    # Autres configurations personnalisées si nécessaire

# Register your models here.
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Import, ImportAdmin)

