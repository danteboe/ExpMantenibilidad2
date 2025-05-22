# ExpMantenibilidad2/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bulkhead/', include('bulkhead.urls')),
    path('database/', include('database.urls')),
    path('', include('bulkhead.urls')),  # Default to bulkhead
]