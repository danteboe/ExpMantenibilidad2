from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.report_search, name='report_search'),
    path('stats/', views.report_stats, name='report_stats'),
    path('health/', views.health_check, name='health_check'),
]