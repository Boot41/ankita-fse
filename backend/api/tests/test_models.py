from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from api.models import InsurancePlan, Feedback

class TestUserModel(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'age': 30,
            'budget': Decimal('5000.00'),
            'family_size': 2,
            'medical_history': 'No major issues'
        }
        self.user = self.User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Test user creation with all fields"""
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.name, self.user_data['name'])
        self.assertEqual(self.user.age, self.user_data['age'])
        self.assertEqual(self.user.budget, self.user_data['budget'])
        self.assertEqual(self.user.family_size, self.user_data['family_size'])
        self.assertEqual(self.user.medical_history, self.user_data['medical_history'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_user_str_method(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), self.user_data['username'])

class TestInsurancePlanModel(TestCase):
    def setUp(self):
        self.plan_data = {
            'name': 'Test Plan',
            'coverage': 'Basic Coverage',
            'price': Decimal('2400.00'),
            'conditions': 'Standard conditions'
        }
        self.plan = InsurancePlan.objects.create(**self.plan_data)

    def test_plan_creation(self):
        """Test insurance plan creation"""
        self.assertEqual(self.plan.name, self.plan_data['name'])
        self.assertEqual(self.plan.coverage, self.plan_data['coverage'])
        self.assertEqual(self.plan.price, self.plan_data['price'])
        self.assertEqual(self.plan.conditions, self.plan_data['conditions'])

    def test_plan_str_method(self):
        """Test plan string representation"""
        self.assertEqual(str(self.plan), self.plan_data['name'])

    def test_price_per_month_property(self):
        """Test monthly price calculation"""
        expected_monthly = float(self.plan_data['price']) / 12
        self.assertEqual(self.plan.price_per_month, expected_monthly)

class TestFeedbackModel(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.plan = InsurancePlan.objects.create(
            name='Test Plan',
            coverage='Basic Coverage',
            price=Decimal('2400.00'),
            conditions='Standard conditions'
        )
        self.feedback_data = {
            'user': self.user,
            'rating': 5,
            'comments': 'This is a great insurance plan with excellent coverage',

        }
        self.feedback = Feedback.objects.create(**self.feedback_data)

    def test_feedback_creation(self):
        """Test feedback creation"""
        self.assertEqual(self.feedback.user, self.feedback_data['user'])
        self.assertEqual(self.feedback.rating, self.feedback_data['rating'])
        self.assertEqual(self.feedback.comments, self.feedback_data['comments'])

    def test_feedback_str_method(self):
        """Test feedback string representation"""
        expected_str = f"{self.user.username}'s feedback - {self.feedback.rating} stars"
        self.assertEqual(str(self.feedback), expected_str)

    def test_feedback_summary_property(self):
        """Test feedback summary property"""
        expected_summary = f"5 stars - This is a great insurance plan with excellent coverage..."
        self.assertEqual(self.feedback.summary, expected_summary[:55])
