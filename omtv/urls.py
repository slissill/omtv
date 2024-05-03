from django.urls import path
from . import views

app_name = "omtv"

urlpatterns = [
    path('', views.home, name='home'),
    path('programmes', views.programmes_s, name='programmes'),
    path('programmes_s', views.programmes_s, name='programmes_s'),
    path('programmes_r', views.programmes_r, name='programmes_r'),
    path('programmes_u', views.programmes_u, name='programmes_u'),
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