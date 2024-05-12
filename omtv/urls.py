from django.urls import path
from . import views

app_name = "omtv"

urlpatterns = [
    path('', views.home, name='home'),
    path('programmes', views.programmes, name='programmes'),
    path('channels', views.channels, name='channels'),

    path('update_db', views.update_db, name='update_db'),
    path('programmes_update', views.programmes_update, name='programmes_update'),


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