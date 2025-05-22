# populate_db.py
import os
import django
import sys
import random

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpMantenibilidad2.settings')
django.setup()

from database.models import WriteData, ReadData
from bulkhead.models import ServiceStatus

# Palabras médicas comunes para generar contenido más realista
MEDICAL_WORDS = [
    'síntomas', 'diagnóstico', 'tratamiento', 'paciente', 'historial',
    'enfermedad', 'crónica', 'aguda', 'presión', 'cardíaco', 'neurológico',
    'respiratorio', 'cirugía', 'rehabilitación', 'dosis', 'prescripción',
    'examen', 'análisis', 'biopsia', 'radiografía', 'tomografía', 'medicación',
    'enfermero', 'consulta', 'especialista', 'dolor', 'fiebre', 'fatiga',
    'dermatitis', 'asma', 'diabetes', 'hipertensión', 'fractura',
    'infección', 'inmunológico', 'vascular', 'terapia', 'prevención',
    'hospitalización', 'urgencia', 'evaluación', 'síndrome', 'lesión'
]

def generate_medical_text(word_count):
    return ' '.join(random.choices(MEDICAL_WORDS, k=word_count)).capitalize()

def populate_database():
    """Populate database with sample medical data"""
    
    server_type = os.environ.get('SERVER_TYPE', 'bulkhead')

    if server_type == 'write':
        print("Populating write database with 2000 medical records...")
        for _ in range(2000):
            title = generate_medical_text(random.randint(3, 6))
            content = generate_medical_text(random.randint(15, 30))
            WriteData.objects.create(title=title, content=content)
        print(f"Total write records: {WriteData.objects.count()}")

    elif server_type == 'read':
        print("Populating read database with 2000 medical records...")
        for _ in range(2000):
            title = generate_medical_text(random.randint(3, 6))
            content = generate_medical_text(random.randint(15, 30))
            ReadData.objects.create(title=title, content=content)
        print(f"Total read records: {ReadData.objects.count()}")

    else:  # bulkhead
        print("Initializing bulkhead service status...")
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
