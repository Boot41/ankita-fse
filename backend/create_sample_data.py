import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import InsurancePlan

def create_sample_plans():
    # Create basic insurance plans
    plans = [
        {
            'name': 'Basic Health Plan',
            'coverage': 'Basic medical coverage including doctor visits and basic medications',
            'price': 2000.00,
            'conditions': 'No pre-existing conditions covered'
        },
        {
            'name': 'Family Health Plus',
            'coverage': 'Comprehensive family coverage including dental and vision',
            'price': 4000.00,
            'conditions': 'Covers pre-existing conditions after 6 months'
        },
        {
            'name': 'Premium Health Care',
            'coverage': 'Premium coverage with international treatment options',
            'price': 6000.00,
            'conditions': 'Full coverage including pre-existing conditions'
        }
    ]

    # Add plans to database
    for plan in plans:
        InsurancePlan.objects.create(**plan)

    print("Sample insurance plans created successfully!")

if __name__ == '__main__':
    create_sample_plans()
