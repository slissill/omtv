from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('omtv/', include('omtv.urls')),
    path('', include('omtv.urls', namespace='toto')),
    path('accounts/', include('accounts.urls')),
]