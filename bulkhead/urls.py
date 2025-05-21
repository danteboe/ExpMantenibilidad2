from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('control/<str:service_name>/', views.service_control, name='service_control'),
    path('api/<path:path>', views.bulkhead_proxy, name='bulkhead_proxy'),
    path('', views.bulkhead_proxy, name='bulkhead_proxy_root'),
]