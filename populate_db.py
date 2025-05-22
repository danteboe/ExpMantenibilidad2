# populate_db.py
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpMantenibilidad2.settings')
django.setup()

from database.models import WriteData, ReadData
from bulkhead.models import ServiceStatus

def populate_database():
    """Populate database with sample data"""
    
    # Get server type
    server_type = os.environ.get('SERVER_TYPE', 'bulkhead')
    
    if server_type == 'write':
        print("Populating write database...")
        # Create sample write data
        sample_data = [
            {"title": "Sample Write 1", "content": "This is sample content for write database 1"},
            {"title": "Sample Write 2", "content": "This is sample content for write database 2"},
            {"title": "Sample Write 3", "content": "This is sample content for write database 3"},
        ]
        
        for data in sample_data:
            WriteData.objects.get_or_create(
                title=data["title"],
                defaults={"content": data["content"]}
            )
        print(f"Created {WriteData.objects.count()} write records")
        
    elif server_type == 'read':
        print("Populating read database...")
        # Create sample read data
        sample_data = [
            {"title": "Sample Read 1", "content": "This is sample content for read database 1"},
            {"title": "Sample Read 2", "content": "This is sample content for read database 2"},
            {"title": "Sample Read 3", "content": "This is sample content for read database 3"},
            {"title": "Sample Read 4", "content": "This is sample content for read database 4"},
            {"title": "Sample Read 5", "content": "This is sample content for read database 5"},
        ]
        
        for data in sample_data:
            ReadData.objects.get_or_create(
                title=data["title"],
                defaults={"content": data["content"]}
            )
        print(f"Created {ReadData.objects.count()} read records")
        
    else:  # bulkhead
        print("Initializing bulkhead service status...")
        # Initialize service status
        ServiceStatus.objects.get_or_create(
            service_name='GET',
            defaults={'is_enabled': True}
        )
        ServiceStatus.objects.get_or_create(
            service_name='POST',
            defaults={'is_enabled': True}
        )
        print("Service status initialized")

if __name__ == '__main__':
    populate_database()