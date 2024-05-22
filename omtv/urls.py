from django.contrib import admin
from django.urls import path
from . import views

app_name = "omtv"

urlpatterns = [
    path('', views.programmes, name='home'),
    path('home', views.home, name='home'),
    path('programmes', views.programmes, name='programmes'),    
    path('preferences', views.preferences, name='preferences'),

    path('update_db', views.update_db, name='update_db'),
    path('task_main', views.task_main, name='task_main'),

    path('dashboard', views.dashboard, name='dashboard'),

    path('stats', views.stats, name='stats'),
    
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