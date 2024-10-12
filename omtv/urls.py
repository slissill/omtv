from django.contrib import admin
from django.urls import path
from . import views

app_name = "omtv"

urlpatterns = [
    path('', views.programmes, name='home'),
    path('home', views.home, name='home'),
    path('old_programmes', views.old_programmes, name='old_programmes'),    
    path('preferences', views.preferences, name='preferences'),
    path('import_xml_data', views.import_xml_data, name='import_xml_data'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('stats', views.stats, name='stats'),    
    path('get_imdb_datas/', views.get_imdb_datas, name='get_imdb_datas'),
    path('videos/', views.videos, name='videos'),    
    path('debug_datas', views.debug_datas, name='debug_datas'),
    path('my_carousel/', views.my_carousel, name='my_carousel'),
    path('programmes/', views.programmes, name='programmes'),
    path('programme_fiche/', views.programme_fiche, name='programme_fiche'),
    path('rapport/', views.rapport, name='rapport'),
]

'''
************************************************************
******* VENV ***********************************************
************************************************************

C:\ZDEPOT\VENV\SCRIPTS\activate.ps1
CD C:\ZDEPOT\omtv\
python manage.py runserver


C:\ZDEPOT\VENV\SCRIPTS\deactivate

************************************************************
******* SERVER  ********************************************
************************************************************

CD C:\ZDEPOT\omtv\
python manage.py runserver


http://127.0.0.1:8000/omtv/


************************************************************
******* Des modules à installer ****************************
************************************************************
Attention il faut les installer dans la VM active

pip install mysqlclient
pip install requests

************************************************************
LIBRARIES (dépendances)
************************************************************
pip freeze > requirements.txt

pip install -r requirements.txt

#************************************************************
#******* MIGRATION DB   *************************************
#************************************************************
python manage.py makemigrations omtv


#************************************************************
#******* Python Anywhere pull ********************************
#************************************************************
workon venv
cd omtv
git pull


'''