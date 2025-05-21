#!/usr/bin/env python
"""
Script to populate the database with 300 random reports
"""
import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from database.models import Report

fake = Faker()

# Predefined data for more realistic reports
DEPARTMENTS = [
    'Finance', 'Engineering', 'Marketing', 'Sales', 'Human Resources',
    'Operations', 'Legal', 'Product Management', 'Quality Assurance',
    'Customer Support', 'Research & Development', 'Business Development'
]

CATEGORIES = ['financial', 'technical', 'operational', 'strategic', 'compliance']
PRIORITIES = ['low', 'medium', 'high', 'critical']
STATUSES = ['draft', 'review', 'approved', 'published', 'archived']

TAGS_POOL = [
    'quarterly', 'annual', 'budget', 'forecast', 'analysis', 'performance',
    'metrics', 'kpi', 'revenue', 'costs', 'productivity', 'efficiency',
    'security', 'compliance', 'audit', 'risk', 'strategy', 'planning',
    'development', 'improvement', 'innovation', 'market', 'customer',
    'user', 'feedback', 'survey', 'research', 'data', 'insights',
    'trends', 'technology', 'digital', 'automation', 'process'
]

def generate_report_title(category, department):
    """Generate a realistic report title based on category and department"""
    title_patterns = {
        'financial': [
            f'{department} Financial Performance Report',
            f'Q{random.randint(1,4)} Budget Analysis - {department}',
            f'{department} Cost Optimization Report',
            f'Revenue Forecast - {department}',
            f'{department} ROI Analysis'
        ],
        'technical': [
            f'{department} Technical Architecture Review',
            f'System Performance Report - {department}',
            f'{department} Infrastructure Assessment',
            f'Security Analysis Report - {department}',
            f'{department} Technology Stack Evaluation'
        ],
        'operational': [
            f'{department} Operational Efficiency Report',
            f'Process Improvement Analysis - {department}',
            f'{department} Workflow Optimization',
            f'Resource Utilization Report - {department}',
            f'{department} Service Level Report'
        ],
        'strategic': [
            f'{department} Strategic Planning Report',
            f'Market Analysis - {department}',
            f'{department} Competitive Intelligence',
            f'Growth Strategy Report - {department}',
            f'{department} Business Transformation Plan'
        ],
        'compliance': [
            f'{department} Compliance Audit Report',
            f'Regulatory Review - {department}',
            f'{department} Risk Assessment',
            f'Policy Compliance Report - {department}',
            f'{department} Governance Review'
        ]
    }
    
    return random.choice(title_patterns[category])

def generate_report_description(category, title):
    """Generate a detailed description based on the report category and title"""
    descriptions = {
        'financial': [
            f"Comprehensive analysis of financial performance including revenue trends, cost structures, and profitability metrics. This report examines budget variance, cash flow projections, and provides recommendations for financial optimization.",
            f"Detailed financial review covering key performance indicators, expense analysis, and revenue forecasting. The report includes comparative analysis with previous periods and industry benchmarks.",
            f"In-depth financial assessment examining cost drivers, revenue opportunities, and budget allocation effectiveness. Includes recommendations for improving financial efficiency and ROI."
        ],
        'technical': [
            f"Technical evaluation covering system architecture, performance metrics, and infrastructure capabilities. This report analyzes scalability, security, and maintenance requirements.",
            f"Comprehensive technical review examining system performance, security vulnerabilities, and optimization opportunities. Includes recommendations for technology improvements and upgrades.",
            f"Technical assessment covering infrastructure reliability, performance bottlenecks, and security posture. Provides actionable recommendations for system enhancement."
        ],
        'operational': [
            f"Operational analysis examining process efficiency, resource utilization, and service delivery metrics. This report identifies bottlenecks and provides improvement recommendations.",
            f"Comprehensive operational review covering workflow optimization, productivity metrics, and quality assurance. Includes best practices and process improvement strategies.",
            f"Operational assessment focusing on efficiency gains, cost reduction opportunities, and service level improvements. Provides detailed action plans for implementation."
        ],
        'strategic': [
            f"Strategic analysis examining market opportunities, competitive positioning, and growth strategies. This report provides recommendations for long-term business development.",
            f"Comprehensive strategic review covering market trends, competitive analysis, and business model optimization. Includes strategic recommendations and implementation roadmap.",
            f"Strategic assessment focusing on market expansion, competitive advantages, and strategic partnerships. Provides actionable insights for business growth."
        ],
        'compliance': [
            f"Compliance review examining regulatory requirements, policy adherence, and risk mitigation strategies. This report identifies compliance gaps and provides remediation plans.",
            f"Comprehensive compliance assessment covering regulatory compliance, internal controls, and audit findings. Includes corrective action plans and compliance improvement strategies.",
            f"Compliance analysis focusing on regulatory requirements, policy compliance, and risk management. Provides detailed recommendations for compliance enhancement."
        ]
    }
    
    base_desc = random.choice(descriptions[category])
    additional_context = f" Key findings include {fake.sentence()} The report also covers {fake.sentence()}"
    
    return base_desc + additional_context

def create_reports(count=300):
    """Create the specified number of random reports"""
    print(f"Creating {count} random reports...")
    
    reports_created = 0
    
    for i in range(count):
        # Random selections
        category = random.choice(CATEGORIES)
        department = random.choice(DEPARTMENTS)
        priority = random.choice(PRIORITIES)
        status = random.choice(STATUSES)
        
        # Generate realistic title and description
        title = generate_report_title(category, department)
        description = generate_report_description(category, title)
        
        # Random author name
        author = fake.name()
        
        # Random dates
        created_date = fake.date_time_between(start_date='-2y', end_date='now')
        
        # Due date (some reports might not have one)
        due_date = None
        if random.random() > 0.3:  # 70% chance of having a due date
            due_date = fake.date_time_between(start_date=created_date, end_date='+6M')
        
        # Random tags
        num_tags = random.randint(2, 5)
        tags = random.sample(TAGS_POOL, num_tags)
        tags_str = ', '.join(tags)
        
        try:
            # Create the report
            report = Report.objects.create(
                title=title,
                description=description,
                author=author,
                department=department,
                category=category,
                priority=priority,
                status=status,
                created_at=created_date,
                due_date=due_date,
                tags=tags_str
            )
            
            reports_created += 1
            
            if reports_created % 50 == 0:
                print(f"Created {reports_created} reports...")
                
        except Exception as e:
            print(f"Error creating report {i+1}: {e}")
    
    print(f"Successfully created {reports_created} reports!")
    return reports_created

def main():
    """Main function to populate the database"""
    print("Starting database population...")
    
    # Check if reports already exist
    existing_count = Report.objects.count()
    if existing_count > 0:
        response = input(f"Database already contains {existing_count} reports. Do you want to add more? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Create reports
    created_count = create_reports(300)
    
    # Print summary
    total_count = Report.objects.count()
    print(f"\nDatabase population complete!")
    print(f"Total reports in database: {total_count}")
    print(f"Reports created in this run: {created_count}")
    
    # Print some statistics
    print(f"\nStatistics:")
    for category in CATEGORIES:
        count = Report.objects.filter(category=category).count()
        print(f"  {category.title()}: {count} reports")

if __name__ == '__main__':
    main()