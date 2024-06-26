"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path


print ('<<<<<<< SETTINGS.PY >>>>>>>>>>>')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent

'''
BASE_DIR (local)            => C:\ZDEPOT\omtv
BASE_DIR (pythonanywhere)   => home/slissill/omtv
   

BASE_DIR
    |----[.git]
    |----[accounts]
    |----[omtv]
    |----[root]
           |----.env           
           |----settings.py
           |----wsgi.py
           |...

    |----.gitignore
    |----manage.py
    |----requirements.txt

'''

SETTINGS_PATH   = os.path.abspath(__file__)
PROJECT_DIR     = os.path.dirname(SETTINGS_PATH)
BASE_DIR        = os.path.dirname(PROJECT_DIR)
ENV_PATH        = os.path.join(PROJECT_DIR, '.env')     

print ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
print (f"SETTINGS_PATH  : {SETTINGS_PATH}")
print (f"PROJECT_PATH   : {PROJECT_DIR}")
print (f"BASE_DIR       : {BASE_DIR}")
print (f"ENV_PATH       : {ENV_PATH}")
print ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")

# Lit les key-value du fichier.env pour les loader dans les variables d'environnements
from dotenv import load_dotenv
load_dotenv(ENV_PATH)

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Obtient un bool qui indique si je suis dans l'environnement pythonanywhere
# Il faut préalablement ajouter dans .wsgi une variable d'environnement qui porte cette clée
IS_PA = 'PYTHONANYWHERE_DOMAIN' in os.environ
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
if IS_PA:
    DEBUG = False
    ALLOWED_HOSTS = ['slissill.pythonanywhere.com']
else:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

###################### SWITCH for pythonanywhere   ######################
#DEBUG = True
#DEBUG = False
#########################################################################
###################### SWITCH for pythonanywhere   ######################
#ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['slissill.pythonanywhere.com']
#########################################################################

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'omtv', 
    'accounts'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware', 
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

########################################################################################
# Database
# pip install mysqlclient
########################################################################################
if IS_PA:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'slissill$omtv',
            'USER': 'slissill',
            'PASSWORD': os.environ.get('BDD_PWD'),
            'HOST': 'slissill.mysql.pythonanywhere-services.com',
            }
        }
else:    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'omtv',
            'USER': 'root',
            'PASSWORD': os.environ.get('BDD_PWD_LOCAL'),
            'HOST': 'localhost',
            'PORT': '',             # Laissez vide pour utiliser le port par défaut (3306)
            }
        }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#STATIC_URL = 'static/'


#python manage.py collectstatic


# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Additional locations of static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'omtv', 'static'),]



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
