# database/views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import WriteData, ReadData
import json

# Get server type from environment variable
SERVER_TYPE = os.environ.get('SERVER_TYPE', 'both')  # 'write', 'read', or 'both'

@csrf_exempt
@require_http_methods(["POST"])
def write_data(request):
    """Handle write operations - only available on write servers"""
    if SERVER_TYPE not in ['write', 'both']:
        return JsonResponse({
            'error': 'Write operations not available on this server',
            'server_type': SERVER_TYPE
        }, status=403)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '')
        content = data.get('content', '')
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        
        # Create new record
        write_record = WriteData.objects.create(
            title=title,
            content=content
        )
        
        return JsonResponse({
            'id': write_record.id,
            'title': write_record.title,
            'content': write_record.content,
            'created_at': write_record.created_at.isoformat(),
            'message': 'Data written successfully'
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def read_data(request):
    """Handle read operations - only available on read servers"""
    if SERVER_TYPE not in ['read', 'both']:
        return JsonResponse({
            'error': 'Read operations not available on this server',
            'server_type': SERVER_TYPE
        }, status=403)
    
    try:
        # Get query parameters
        record_id = request.GET.get('id')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        
        # If specific ID requested
        if record_id:
            try:
                record = ReadData.objects.get(id=record_id)
                return JsonResponse({
                    'id': record.id,
                    'title': record.title,
                    'content': record.content,
                    'created_at': record.created_at.isoformat(),
                    'updated_at': record.updated_at.isoformat()
                })
            except ReadData.DoesNotExist:
                return JsonResponse({'error': 'Record not found'}, status=404)
        
        # Get all records with pagination
        all_records = ReadData.objects.all()
        paginator = Paginator(all_records, page_size)
        
        try:
            records = paginator.page(page)
        except:
            return JsonResponse({'error': 'Invalid page number'}, status=400)
        
        # Serialize records
        data = [{
            'id': record.id,
            'title': record.title,
            'content': record.content,
            'created_at': record.created_at.isoformat(),
            'updated_at': record.updated_at.isoformat()
        } for record in records]
        
        return JsonResponse({
            'data': data,
            'pagination': {
                'current_page': records.number,
                'total_pages': paginator.num_pages,
                'total_records': paginator.count,
                'has_next': records.has_next(),
                'has_previous': records.has_previous()
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'server_type': SERVER_TYPE
    })