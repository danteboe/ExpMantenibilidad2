import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import ReadOperation
import logging

logger = logging.getLogger(__name__)

def forward_to_database(method, path, params=None):
    """Forward request to the read database"""
    try:
        url = f"{settings.LECTURA_DB_URL}/api{path}"
        headers = {'Content-Type': 'application/json'}
        
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=30)
        else:
            return None, 405
        
        # Log the operation
        ReadOperation.objects.create(
            operation_type=f"{method} {path}",
            success=response.status_code < 400
        )
        
        return response.json() if response.content else {}, response.status_code
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error forwarding to database: {e}")
        ReadOperation.objects.create(
            operation_type=f"{method} {path}",
            success=False
        )
        return {'error': f'Database connection failed: {str(e)}'}, 502

@api_view(['GET'])
def list_reports(request):
    """List all reports with optional filtering"""
    params = request.GET.dict()
    data, status_code = forward_to_database('GET', '/reports/', params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_report(request, report_id):
    """Get a specific report by ID"""
    data, status_code = forward_to_database('GET', f'/reports/{report_id}/')
    return Response(data, status=status_code)

@api_view(['GET'])
def search_reports(request):
    """Search reports"""
    params = request.GET.dict()
    data, status_code = forward_to_database('GET', '/search/', params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_report_stats(request):
    """Get report statistics"""
    data, status_code = forward_to_database('GET', '/stats/')
    return Response(data, status=status_code)

@api_view(['GET'])
def filter_reports(request):
    """Advanced filtering of reports"""
    params = request.GET.dict()
    
    # Build query parameters for filtering
    filter_params = {}
    
    # Basic filters
    for field in ['title', 'author', 'category', 'status', 'priority', 'department']:
        if field in params:
            filter_params[field] = params[field]
    
    # Date range filters
    if 'created_after' in params:
        filter_params['created_at__gte'] = params['created_after']
    if 'created_before' in params:
        filter_params['created_at__lte'] = params['created_before']
    
    # Pagination
    if 'page' in params:
        filter_params['page'] = params['page']
    if 'page_size' in params:
        filter_params['page_size'] = params['page_size']
    
    data, status_code = forward_to_database('GET', '/reports/', filter_params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_reports_by_author(request, author):
    """Get all reports by a specific author"""
    params = request.GET.dict()
    params['author'] = author
    data, status_code = forward_to_database('GET', '/reports/', params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_reports_by_category(request, category):
    """Get all reports by category"""
    params = request.GET.dict()
    params['category'] = category
    data, status_code = forward_to_database('GET', '/reports/', params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_reports_by_status(request, status_param):
    """Get all reports by status"""
    params = request.GET.dict()
    params['status'] = status_param
    data, status_code = forward_to_database('GET', '/reports/', params)
    return Response(data, status=status_code)

@api_view(['GET'])
def get_read_stats(request):
    """Get read operation statistics"""
    total_operations = ReadOperation.objects.count()
    successful_operations = ReadOperation.objects.filter(success=True).count()
    failed_operations = ReadOperation.objects.filter(success=False).count()
    
    return Response({
        'total_operations': total_operations,
        'successful_operations': successful_operations,
        'failed_operations': failed_operations,
        'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0
    })

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    # Test connection to read database
    try:
        data, status_code = forward_to_database('GET', '/health/')
        db_healthy = status_code == 200
    except:
        db_healthy = False
    
    return Response({
        'status': 'healthy',
        'service': 'lectura',
        'database_connection': 'healthy' if db_healthy else 'unhealthy',
        'total_operations': ReadOperation.objects.count()
    })