import requests  #pip install requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .utils import maj_db
from .models import Programme

#return HttpResponse("update_db_r") 


def home(request):    
    return render(request, 'omtv/home.html')

def update_db(request):  
    maj_db (request.GET.get('mode', 's'))
    return redirect ("omtv:programmes")
    

def programmes(request):
    context = {"programmes" : Programme.objects.order_by('start'), 
               "view" : request.GET.get('view', 'accordeon')}
    return render(request, 'omtv/programmes.html', context)
