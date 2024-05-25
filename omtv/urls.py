from django.contrib import admin
from django.urls import path
from . import views

app_name = "omtv"

urlpatterns = [
    path('', views.programmes, name='home'),
    path('home', views.home, name='home'),
    path('programmes', views.programmes, name='programmes'),    
    path('preferences', views.preferences, name='preferences'),
    path('import_xml_data', views.import_xml_data, name='import_xml_data'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('stats', views.stats, name='stats'),    
    path('get_imdb_datas/', views.get_imdb_datas, name='get_imdb_datas'),
]

'''
************************************************************
******* VENV ***********************************************
************************************************************

C:\ZDEPOT\VENV\SCRIPTS\activate.ps1

C:\ZDEPOT\VENV\SCRIPTS\deactivate

************************************************************
******* SERVER  ********************************************
************************************************************

CD C:\ZDEPOT\omtv\
python manage.py runserver



************************************************************
******* Des modules à installer ****************************
************************************************************
Attention il faut les installer dans la VM active

pip install mysqlclient
pip install requests

Obtenir les dépendances
pip freeze > requirements.txt


#************************************************************
#******* MIGRATION DB   *************************************
#************************************************************
python manage.py makemigrations omtv


'''