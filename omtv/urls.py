from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('programmes', views.programmes, name='programmes'),
]


'''

######## ENV activate ##################################################
C:\VMS2\A\ENV\SCRIPTS\activate.ps1


######## ENV deactivate ##################################################
git

######## Run Server ##################################################
CD C:\VMS2\A\root\
python manage.py runserver



######## Migration DB ##################################################
python manage.py makemigrations omtv


'''