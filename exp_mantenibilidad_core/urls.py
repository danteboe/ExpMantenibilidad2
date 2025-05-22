from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import os

SERVICE_TYPE = os.environ.get('SERVICE_TYPE', 'bulkhead')

if SERVICE_TYPE == 'bulkhead':
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('bulkhead.urls')),
    ]
elif SERVICE_TYPE == 'database':
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('database.urls')),
    ]
elif SERVICE_TYPE == 'escribir':
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('escribir.urls')),
    ]
elif SERVICE_TYPE == 'lectura':
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('lectura.urls')),
    ]
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]