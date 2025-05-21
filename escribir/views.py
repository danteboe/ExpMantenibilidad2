import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import WriteOperation
import logging

logger = logging.getLogger(__name__)

def forward_to_database(method, path, data=None, params=None):
    """Forward request to the write database"""
    try:
        url = f"{settings.ESCRIBIR_DB_URL}/api{path}"
        headers = {'Content-Type': 'application/json'}
        
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=headers, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return None, 405
        
        # Log the operation
        WriteOperation.objects.create(
            operation_type=f"{method} {path}",
            success=response.status_code < 400
        )
        
        return response.json() if response.content else {}, response.status_code
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error forwarding to database: {e}")
        WriteOperation.objects.create(
            operation_type=f"{method} {path}",
            success=False
        )
        return {'error': f'Database connection failed: {str(e)}'}, 502

@api_view(['POST'])
def create_report(request):
    """Create a new report"""
    data, status_code = forward_to_database('POST', '/reports/', request.data)
    return Response(data, status=status_code)

@api_view(['PUT', 'PATCH'])
def update_report(request, report_id):
    """Update an existing report"""
    method = 'PUT' if request.method == 'PUT' else 'PATCH'
    data, status_code = forward_to_database(method, f'/reports/{report_id}/', request.data)
    return Response(data, status=status_code)

@api_view(['DELETE'])
def delete_report(request, report_id):
    """Delete a report"""
    data, status_code = forward_to_database('DELETE', f'/reports/{report_id}/')
    return Response(data, status=status_code)

@api_view(['POST'])
def bulk_create_reports(request):
    """Create multiple reports at once"""
    if not isinstance(request.data, list):
        return Response({
            'error': 'Expected a list of reports'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    created_reports = []
    errors = []
    
    for i, report_data in enumerate(request.data):
        data, status_code = forward_to_database('POST', '/reports/', report_data)
        if status_code < 400:
            created_reports.append(data)
        else:
            errors.append({
                'index': i,
                'error': data,
                'data': report_data
            })
    
    return Response({
        'created': len(created_reports),
        'errors': len(errors),
        'created_reports': created_reports,
        'error_details': errors
    })

@api_view(['PATCH'])
def bulk_update_reports(request):
    """Update multiple reports at once"""
    if not isinstance(request.data, list):
        return Response({
            'error': 'Expected a list of reports with id and update data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    updated_reports = []
    errors = []
    
    for i, update_data in enumerate(request.data):
        if 'id' not in update_data:
            errors.append({
                'index': i,
                'error': 'Missing id field',
                'data': update_data
            })
            continue
        
        report_id = update_data.pop('id')
        data, status_code = forward_to_database('PATCH', f'/reports/{report_id}/', update_data)
        
        if status_code < 400:
            updated_reports.append(data)
        else:
            errors.append({
                'index': i,
                'id': report_id,
                'error': data,
                'data': update_data
            })
    
    return Response({
        'updated': len(updated_reports),
        'errors': len(errors),
        'updated_reports': updated_reports,
        'error_details': errors
    })

@api_view(['GET'])
def get_write_stats(request):
    """Get write operation statistics"""
    total_operations = WriteOperation.objects.count()
    successful_operations = WriteOperation.objects.filter(success=True).count()
    failed_operations = WriteOperation.objects.filter(success=False).count()
    
    return Response({
        'total_operations': total_operations,
        'successful_operations': successful_operations,
        'failed_operations': failed_operations,
        'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0
    })

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    # Test connection to write database
    try:
        data, status_code = forward_to_database('GET', '/health/')
        db_healthy = status_code == 200
    except:
        db_healthy = False
    
    return Response({
        'status': 'healthy',
        'service': 'escribir',
        'database_connection': 'healthy' if db_healthy else 'unhealthy',
        'total_operations': WriteOperation.objects.count()
    })