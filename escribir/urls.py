from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.create_report, name='create_report'),
    path('reports/<uuid:report_id>/', views.update_report, name='update_report'),
    path('reports/<uuid:report_id>/delete/', views.delete_report, name='delete_report'),
    path('reports/bulk-create/', views.bulk_create_reports, name='bulk_create_reports'),
    path('reports/bulk-update/', views.bulk_update_reports, name='bulk_update_reports'),
    path('stats/', views.get_write_stats, name='write_stats'),
    path('health/', views.health_check, name='health_check'),
]