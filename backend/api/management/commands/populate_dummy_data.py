import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import User, InsurancePlan, Feedback

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create dummy users
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                name=fake.name(),
                age=random.randint(18, 70),
                budget=random.uniform(1000, 5000),
                family_size=random.randint(1, 5),
                medical_history=fake.text(max_nb_chars=200)
            )

        # Create dummy insurance plans
        for _ in range(5):
            plan = InsurancePlan.objects.create(
                name=fake.company(),
                coverage=fake.text(max_nb_chars=100),
                price=random.uniform(100, 1000),
                conditions=fake.text(max_nb_chars=100)
            )

        # Create dummy feedback
        users = User.objects.all()
        plans = InsurancePlan.objects.all()
        for _ in range(20):
            Feedback.objects.create(
                user=random.choice(users),
                rating=random.randint(1, 5),
                comments=fake.text(max_nb_chars=200)
            )

        self.stdout.write(self.style.SUCCESS('Dummy data populated successfully!'))
