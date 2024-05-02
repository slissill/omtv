from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('programmes', views.programmes, name='programmes'),
]


'''

#************************************************************
#******* VENV ***********************************************
#************************************************************
C:\VMS2\B\ENV\SCRIPTS\activate.ps1
C:\VMS2\B\ENV\SCRIPTS\deactivate

#************************************************************
#******* Des modules à installer ****************************
#************************************************************
# Attention il faut les installer dans la VM active
pip install mysqlclient
pip install requests


#************************************************************
#******* SERVER  ********************************************
#************************************************************
CD C:\VMS2\B\omtv\
python manage.py runserver


#************************************************************
#******* MIGRATION DB   *************************************
#************************************************************
python manage.py makemigrations omtv


'''