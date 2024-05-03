from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('programmes', views.programmes, name='programmes'),
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