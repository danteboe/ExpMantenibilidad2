# database/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('write/', views.write_data, name='write_data'),
    path('read/', views.read_data, name='read_data'),
    path('health/', views.health_check, name='health_check'),
]