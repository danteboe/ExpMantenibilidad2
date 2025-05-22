#!/usr/bin/env python
"""
Script to populate the database with 300 random reports
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from database.models import Report
from faker import Faker

fake = Faker()

# Categories and priorities
CATEGORIES = ['financial', 'technical', 'operational', 'strategic', 'compliance']
PRIORITIES = ['low', 'medium', 'high', 'critical']
STATUSES = ['draft', 'review', 'approved', 'published', 'archived']
DEPARTMENTS = [
    'Finance', 'Engineering', 'Operations', 'Marketing', 'Sales',
    'Human Resources', 'Legal', 'IT', 'Research & Development', 'Quality Assurance'
]

# Sample tags for reports
TAGS = [
    'urgent', 'quarterly', 'budget', 'security', 'performance',
    'maintenance', 'compliance', 'strategic', 'customer', 'internal',
    'external', 'review', 'analysis', 'forecast', 'audit'
]

def generate_random_tags():
    """Generate random tags for a report"""
    num_tags = random.randint(1, 5)
    return random.sample(TAGS, num_tags)

def create_random_report():
    """Create a random report"""
    # Generate random due date (between now and 6 months from now)
    due_date = fake.date_time_between(start_date='now', end_date='+6M')
    
    # Generate tags
    tags = generate_random_tags()
    
    report = Report.objects.create(
        title=fake.catch_phrase() + " Report",
        description=fake.text(max_nb_chars=500),
        author=fake.name(),
        department=random.choice(DEPARTMENTS),
        category=random.choice(CATEGORIES),
        priority=random.choice(PRIORITIES),
        status=random.choice(STATUSES),
        due_date=due_date,
        tags=', '.join(tags)
    )
    
    return report

def populate_database():
    """Populate database with 300 random reports"""
    print("Starting database population...")
    
    # Clear existing reports
    Report.objects.all().delete()
    print("Cleared existing reports")
    
    # Create 300 random reports
    reports_created = 0
    for i in range(300):
        try:
            report = create_random_report()
            reports_created += 1
            
            if (i + 1) % 50 == 0:
                print(f"Created {i + 1} reports...")
                
        except Exception as e:
            print(f"Error creating report {i + 1}: {e}")
            continue
    
    print(f"Successfully created {reports_created} reports")
    
    # Print some statistics
    print("\nDatabase Statistics:")
    print(f"Total reports: {Report.objects.count()}")
    
    print("\nBy Category:")
    for category, _ in Report._meta.get_field('category').choices:
        count = Report.objects.filter(category=category).count()
        print(f"  {category.title()}: {count}")
    
    print("\nBy Priority:")
    for priority, _ in Report._meta.get_field('priority').choices:
        count = Report.objects.filter(priority=priority).count()
        print(f"  {priority.title()}: {count}")
    
    print("\nBy Status:")
    for status, _ in Report._meta.get_field('status').choices:
        count = Report.objects.filter(status=status).count()
        print(f"  {status.title()}: {count}")

if __name__ == '__main__':
    populate_database()
    print("Database population completed!")