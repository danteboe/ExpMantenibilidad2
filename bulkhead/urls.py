# bulkhead/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BulkheadView.as_view(), name='bulkhead'),
    path('toggle/', views.toggle_service, name='toggle_service'),
    path('status/', views.service_status, name='service_status'),
]