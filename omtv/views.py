import requests  #pip install requests
from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_programmes

def index(request):    
    return HttpResponse("Hello World")



def programmes(request):

    programmes = get_programmes
    
    context = {"programmes" : programmes, 
               "view" : request.GET.get('view', 'accordeon')}
    return render(request, 'omtv/programmes.html', context)
