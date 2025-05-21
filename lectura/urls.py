from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.list_reports, name='list_reports'),
    path('reports/<uuid:report_id>/', views.get_report, name='get_report'),
    path('reports/author/<str:author>/', views.get_reports_by_author, name='reports_by_author'),
    path('reports/category/<str:category>/', views.get_reports_by_category, name='reports_by_category'),
    path('reports/status/<str:status_param>/', views.get_reports_by_status, name='reports_by_status'),
    path('search/', views.search_reports, name='search_reports'),
    path('filter/', views.filter_reports, name='filter_reports'),
    path('stats/', views.get_report_stats, name='report_stats'),
    path('read-stats/', views.get_read_stats, name='read_stats'),
    path('health/', views.health_check, name='health_check'),
]