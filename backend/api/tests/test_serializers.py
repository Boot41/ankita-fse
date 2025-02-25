from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from api.models import InsurancePlan, Feedback
from api.serializers import UserSerializer, InsurancePlanSerializer, FeedbackSerializer

class TestUserSerializer(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'age': 30,
            'budget': '5000.00',
            'family_size': 2,
            'medical_history': 'No major issues'
        }

    def test_user_serialization(self):
        """Test user serialization"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_user_serialization_missing_required(self):
        """Test user serialization with missing required fields"""
        invalid_data = self.user_data.copy()
        del invalid_data['username']
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_user_serialization_invalid_email(self):
        """Test user serialization with invalid email"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class TestInsurancePlanSerializer(TestCase):
    def setUp(self):
        self.plan_data = {
            'name': 'Test Plan',
            'coverage': 'Basic Coverage',
            'price': '2400.00',
            'conditions': 'Standard conditions'
        }
        self.plan = InsurancePlan.objects.create(
            name=self.plan_data['name'],
            coverage=self.plan_data['coverage'],
            price=Decimal(self.plan_data['price']),
            conditions=self.plan_data['conditions']
        )

    def test_plan_serialization(self):
        """Test insurance plan serialization"""
        serializer = InsurancePlanSerializer(self.plan)
        data = serializer.data
        self.assertEqual(data['name'], self.plan_data['name'])
        self.assertEqual(data['coverage'], self.plan_data['coverage'])
        self.assertEqual(float(data['price']), float(self.plan_data['price']))
        self.assertEqual(data['conditions'], self.plan_data['conditions'])
        self.assertEqual(data['price_per_month'], float(self.plan_data['price']) / 12)

    def test_plan_deserialization(self):
        """Test insurance plan deserialization"""
        serializer = InsurancePlanSerializer(data=self.plan_data)
        self.assertTrue(serializer.is_valid())
        plan = serializer.save()
        self.assertEqual(plan.name, self.plan_data['name'])
        self.assertEqual(plan.coverage, self.plan_data['coverage'])
        self.assertEqual(float(plan.price), float(self.plan_data['price']))

class TestFeedbackSerializer(TestCase):
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
            'rating': 5,
            'comments': 'Great service!'
        }
        self.feedback = Feedback.objects.create(
            user=self.user,
            rating=self.feedback_data['rating'],
            comments=self.feedback_data['comments'],

        )

    def test_feedback_serialization(self):
        """Test feedback serialization"""
        serializer = FeedbackSerializer(self.feedback)
        data = serializer.data
        self.assertEqual(data['rating'], self.feedback_data['rating'])
        self.assertEqual(data['comments'], self.feedback_data['comments'])
        self.assertIn('summary', data)

    def test_feedback_validation_invalid_rating(self):
        """Test feedback validation with invalid rating"""
        invalid_data = self.feedback_data.copy()
        invalid_data['rating'] = 6
        serializer = FeedbackSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_feedback_validation_valid_rating(self):
        """Test feedback validation with valid ratings"""
        for rating in range(1, 6):
            data = self.feedback_data.copy()
            data['rating'] = rating
            serializer = FeedbackSerializer(data=data)
            self.assertTrue(serializer.is_valid())
