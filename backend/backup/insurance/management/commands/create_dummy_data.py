from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from insurance.models import InsurancePlan, PlanComparison, UserDashboardPreference, Feedback
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Clear existing data
        User.objects.exclude(is_superuser=True).delete()
        InsurancePlan.objects.all().delete()
        PlanComparison.objects.all().delete()
        UserDashboardPreference.objects.all().delete()
        Feedback.objects.all().delete()
        
        self.stdout.write('Creating dummy data...')

        # Create test users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'testuser{i}@example.com',
                password='testpass123',
                age=random.randint(25, 70),
                budget=Decimal(str(random.randint(200, 1000))),
                family_size=random.randint(1, 5),
                medical_conditions=['none'] if i % 2 == 0 else ['diabetes', 'hypertension'],
                is_profile_complete=True
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Create insurance plans
        plans = []
        plan_types = ['basic', 'standard', 'premium', 'family', 'senior']
        features = [
            'Dental coverage',
            'Vision care',
            'Mental health support',
            'Prescription drugs',
            'Specialist visits',
            'Emergency care',
            'Preventive care'
        ]

        for i in range(10):
            plan = InsurancePlan.objects.create(
                name=f'Insurance Plan {i}',
                plan_type=random.choice(plan_types),
                provider=f'Provider {i % 3}',
                description=f'Comprehensive health insurance plan {i}',
                coverage_details='Full coverage for most medical needs',
                eligibility_criteria='Open to all residents',
                monthly_premium=Decimal(str(random.randint(200, 800))),
                deductible=Decimal(str(random.randint(500, 2000))),
                copay=Decimal(str(random.randint(20, 50))),
                max_coverage=Decimal(str(random.randint(100000, 500000))),
                network_hospitals=[f'Hospital {j}' for j in range(5)],
                features=random.sample(features, 4),
                popularity_score=round(random.uniform(3.0, 5.0), 1)
            )
            plans.append(plan)
            self.stdout.write(f'Created plan: {plan.name}')

        # Create plan comparisons
        for user in users:
            comparison = PlanComparison.objects.create(
                user=user,
                comparison_name=f'My Comparison {user.id}',
                notes='Comparing different plans'
            )
            # Add 2-3 random plans to comparison
            comparison_plans = random.sample(plans, random.randint(2, 3))
            comparison.plans.set(comparison_plans)
            self.stdout.write(f'Created comparison for user: {user.username}')

        # Create dashboard preferences
        for user in users:
            UserDashboardPreference.objects.create(
                user=user,
                default_view=random.choice(['list', 'grid', 'compact']),
                show_premium_first=random.choice([True, False]),
                notification_preferences={
                    'email_notifications': True,
                    'premium_alerts': True,
                    'recommendation_updates': True
                },
                widgets_order=['recommendations', 'recent_plans', 'feedback']
            )
            self.stdout.write(f'Created dashboard preferences for user: {user.username}')

        # Create feedback
        feedback_types = ['recommendation', 'plan', 'ui', 'general']
        for user in users:
            for _ in range(2):
                Feedback.objects.create(
                    user=user,
                    feedback_type=random.choice(feedback_types),
                    insurance_plan=random.choice(plans) if random.choice([True, False]) else None,
                    rating=random.randint(1, 5),
                    ui_element='dashboard' if random.choice([True, False]) else '',
                    comments=f'Test feedback from {user.username}'
                )
            self.stdout.write(f'Created feedback for user: {user.username}')

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data'))
