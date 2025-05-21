import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ServiceStatus
import json
import logging

logger = logging.getLogger(__name__)

def get_service_status(service_name):
    """Get the status of a service"""
    try:
        service = ServiceStatus.objects.get(service_name=service_name)
        return service.is_active
    except ServiceStatus.DoesNotExist:
        # Create default active status if doesn't exist
        ServiceStatus.objects.create(service_name=service_name, is_active=True)
        return True

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def bulkhead_proxy(request):
    """Main bulkhead proxy that routes requests based on HTTP method"""
    
    if request.method in ['POST', 'PUT', 'DELETE']:
        # Write operations go to escribir service
        if not get_service_status('escribir'):
            return JsonResponse({
                'error': 'Escribir service is currently disabled',
                'status': 'service_unavailable'
            }, status=503)
        
        try:
            url = f"{settings.ESCRIBIR_SERVICE_URL}{request.path}"
            headers = {'Content-Type': 'application/json'}
            
            if request.body:
                response = requests.request(
                    method=request.method,
                    url=url,
                    data=request.body,
                    headers=headers,
                    timeout=30
                )
            else:
                response = requests.request(
                    method=request.method,
                    url=url,
                    headers=headers,
                    timeout=30
                )
            
            return JsonResponse(response.json() if response.content else {}, 
                              status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to escribir service: {e}")
            return JsonResponse({
                'error': 'Failed to connect to escribir service',
                'details': str(e)
            }, status=502)
    
    elif request.method == 'GET':
        # Read operations go to lectura service
        if not get_service_status('lectura'):
            return JsonResponse({
                'error': 'Lectura service is currently disabled',
                'status': 'service_unavailable'
            }, status=503)
        
        try:
            url = f"{settings.LECTURA_SERVICE_URL}{request.path}"
            params = request.GET.dict()
            
            response = requests.get(url, params=params, timeout=30)
            
            return JsonResponse(response.json() if response.content else {}, 
                              status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to lectura service: {e}")
            return JsonResponse({
                'error': 'Failed to connect to lectura service',
                'details': str(e)
            }, status=502)

@api_view(['GET', 'POST'])
def service_control(request, service_name):
    """Control endpoint to activate/deactivate services"""
    
    if service_name not in ['escribir', 'lectura']:
        return Response({
            'error': 'Invalid service name. Valid services: escribir, lectura'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        # Get service status
        is_active = get_service_status(service_name)
        return Response({
            'service': service_name,
            'status': 'active' if is_active else 'inactive',
            'is_active': is_active
        })
    
    elif request.method == 'POST':
        # Set service status
        action = request.data.get('action')
        
        if action not in ['activate', 'deactivate']:
            return Response({
                'error': 'Invalid action. Valid actions: activate, deactivate'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        is_active = action == 'activate'
        
        service, created = ServiceStatus.objects.get_or_create(
            service_name=service_name,
            defaults={'is_active': is_active}
        )
        
        if not created:
            service.is_active = is_active
            service.save()
        
        return Response({
            'service': service_name,
            'status': 'active' if is_active else 'inactive',
            'is_active': is_active,
            'message': f'Service {service_name} has been {"activated" if is_active else "deactivated"}'
        })

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'bulkhead',
        'services': {
            'escribir': {
                'active': get_service_status('escribir'),
                'status': 'active' if get_service_status('escribir') else 'inactive'
            },
            'lectura': {
                'active': get_service_status('lectura'),
                'status': 'active' if get_service_status('lectura') else 'inactive'
            }
        }
    })