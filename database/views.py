from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer
import os
import logging

logger = logging.getLogger(__name__)

# Determine if this is a read-only or write-only database
DB_TYPE = os.environ.get('DB_TYPE', 'write')  # 'read' or 'write'

class ReportPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    
    def get_queryset(self):
        queryset = Report.objects.all()
        
        # Filter by query parameters
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        category = self.request.query_params.get('category', None)
        status_filter = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        department = self.request.query_params.get('department', None)
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if category:
            queryset = queryset.filter(category=category)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority:
            queryset = queryset.filter(priority=priority)
        if department:
            queryset = queryset.filter(department__icontains=department)
            
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        if DB_TYPE == 'read':
            return Response({
                'error': 'This database is read-only'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if DB_TYPE == 'read':
            return Response({
                'error': 'This database is read-only'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        if DB_TYPE == 'read':
            return Response({
                'error': 'This database is read-only'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if DB_TYPE == 'read':
            return Response({
                'error': 'This database is read-only'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)

@api_view(['GET'])
def report_search(request):
    """Advanced search endpoint"""
    if DB_TYPE == 'write':
        return Response({
            'error': 'This database is write-only'
        }, status=status.HTTP_403_FORBIDDEN)
    
    search_term = request.GET.get('q', '')
    reports = Report.objects.all()
    
    if search_term:
        reports = reports.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(tags__icontains=search_term)
        )
    
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def report_stats(request):
    """Get database statistics"""
    if DB_TYPE == 'write':
        return Response({
            'error': 'This database is write-only'
        }, status=status.HTTP_403_FORBIDDEN)
    
    total_reports = Report.objects.count()
    
    stats = {
        'total_reports': total_reports,
        'by_category': {},
        'by_status': {},
        'by_priority': {},
    }
    
    # Group by category
    for category, _ in Report._meta.get_field('category').choices:
        count = Report.objects.filter(category=category).count()
        stats['by_category'][category] = count
    
    # Group by status
    for status_choice, _ in Report._meta.get_field('status').choices:
        count = Report.objects.filter(status=status_choice).count()
        stats['by_status'][status_choice] = count
    
    # Group by priority
    for priority, _ in Report._meta.get_field('priority').choices:
        count = Report.objects.filter(priority=priority).count()
        stats['by_priority'][priority] = count
    
    return Response(stats)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'database',
        'db_type': DB_TYPE,
        'total_reports': Report.objects.count()
    })