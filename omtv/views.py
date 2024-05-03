import requests  #pip install requests
from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_programmes

def home(request):    
    #return HttpResponse("Hello World")
    return render(request, 'omtv/home.html')

def programmes(request):    return do_programmes (request, "s")
def programmes_s(request):  return do_programmes (request, "s")
def programmes_r(request):  return do_programmes (request, "r")
def programmes_u(request):  return do_programmes (request, "u")

def do_programmes(request, methode):
    programmes = get_programmes(methode)    
    context = {"programmes" : programmes, 
               "view" : request.GET.get('view', 'accordeon')}
    return render(request, 'omtv/programmes.html', context)
