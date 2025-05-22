# bulkhead/views.py
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from .models import ServiceStatus
import json

# Get database IPs from environment variables
WRITE_DB_IP = os.environ.get('WRITE_DB_IP', 'localhost:8001')
READ_DB_IP = os.environ.get('READ_DB_IP', 'localhost:8002')

def get_service_status(service_name):
    """Get service status from database"""
    try:
        status = ServiceStatus.objects.get(service_name=service_name)
        return status.is_enabled
    except ServiceStatus.DoesNotExist:
        # Create default enabled status if doesn't exist
        ServiceStatus.objects.create(service_name=service_name, is_enabled=True)
        return True

@method_decorator(csrf_exempt, name='dispatch')
class BulkheadView(View):
    
    def get(self, request):
        """Handle GET requests - forward to read database"""
        # Check if GET service is enabled
        if not get_service_status('GET'):
            return JsonResponse({
                'error': 'GET service is currently unavailable',
                'status': 'disabled'
            }, status=503)
        
        try:
            # Forward request to read database
            response = requests.get(f'http://{READ_DB_IP}/database/read/', 
                                  params=request.GET.dict(),
                                  timeout=30)
            
            return JsonResponse(response.json(), status=response.status_code)
            
        except requests.RequestException as e:
            return JsonResponse({
                'error': 'Failed to connect to read database',
                'details': str(e)
            }, status=500)
    
    def post(self, request):
        """Handle POST requests - forward to write database"""
        # Check if POST service is enabled
        if not get_service_status('POST'):
            return JsonResponse({
                'error': 'POST service is currently unavailable',
                'status': 'disabled'
            }, status=503)
        
        try:
            # Parse JSON data
            try:
                data = json.loads(request.body) if request.body else {}
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            # Forward request to write database
            response = requests.post(f'http://{WRITE_DB_IP}/database/write/',
                                   json=data,
                                   headers={'Content-Type': 'application/json'},
                                   timeout=30)
            
            return JsonResponse(response.json(), status=response.status_code)
            
        except requests.RequestException as e:
            return JsonResponse({
                'error': 'Failed to connect to write database',
                'details': str(e)
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def toggle_service(request):
    """Toggle service availability"""
    try:
        data = json.loads(request.body)
        service_name = data.get('service_name', '').upper()
        
        if service_name not in ['GET', 'POST']:
            return JsonResponse({'error': 'Invalid service name. Use GET or POST'}, status=400)
        
        status, created = ServiceStatus.objects.get_or_create(
            service_name=service_name,
            defaults={'is_enabled': True}
        )
        
        # Toggle the status
        status.is_enabled = not status.is_enabled
        status.save()
        
        return JsonResponse({
            'service': service_name,
            'status': 'enabled' if status.is_enabled else 'disabled',
            'message': f'{service_name} service is now {"enabled" if status.is_enabled else "disabled"}'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def service_status(request):
    """Get current service status"""
    try:
        get_status = get_service_status('GET')
        post_status = get_service_status('POST')
        
        return JsonResponse({
            'GET': 'enabled' if get_status else 'disabled',
            'POST': 'enabled' if post_status else 'disabled'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)