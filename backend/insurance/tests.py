"""
Test suite for the insurance application.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from insurance.models import InsurancePlan, Feedback, Recommendation, PlanComparison
from decimal import Decimal
import time
from .test_logger import TestLogger

User = get_user_model()

class InsuranceBaseTestCase(APITestCase):
    """Base test case with common utilities."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger = TestLogger()
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.logger.log_summary()
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            name='Test User',
            age=30,
            budget=Decimal('1000.00'),
            family_size=2,
            medical_history='None'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            name='Admin User'
        )
        
        # Create test insurance plan
        self.plan = InsurancePlan.objects.create(
            name='Test Plan',
            plan_type='basic',
            provider='Test Insurance Co',
            description='A test insurance plan',
            coverage_details='Basic Coverage Details',
            eligibility_criteria='Standard eligibility criteria',
            monthly_premium=Decimal('500.00'),
            deductible=Decimal('1000.00'),
            copay=Decimal('20.00'),
            max_coverage=Decimal('100000.00'),
            network_hospitals='Hospital A, Hospital B'
        )
        
        # Create test feedback
        self.feedback = Feedback.objects.create(
            user=self.user,
            rating=4,
            comments='Great service!'
        )

    def get_tokens_for_user(self, user):
        """Get authentication tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def authenticate_user(self, user=None):
        """Authenticate a user for testing."""
        if user is None:
            user = self.user
        token = self.get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')

class UserTests(InsuranceBaseTestCase):
    """Test cases for UserViewSet."""

    def test_user_registration(self):
        self.logger.log_test_start("test_user_registration")
        start_time = time.time()
        """Test user registration endpoint."""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'name': 'New User',
            'age': 25,
            'budget': '800.00',
            'family_size': 1,
            'medical_history': 'Healthy'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertNotIn('password', response.data)
        self.logger.log_test_result(
            "test_user_registration",
            "PASS",
            time.time() - start_time
        )

    def test_user_detail(self):
        self.logger.log_test_start("test_user_detail")
        start_time = time.time()
        """Test retrieving user details."""
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.logger.log_test_result(
            "test_user_detail",
            "PASS",
            time.time() - start_time
        )
        self.logger.log_test_result(
            "test_user_detail",
            "PASS",
            time.time() - start_time
        )

class InsurancePlanTests(InsuranceBaseTestCase):
    """Test cases for InsurancePlanViewSet."""

    def test_list_plans(self):
        self.logger.log_test_start("test_list_plans")
        start_time = time.time()
        """Test listing insurance plans."""
        url = reverse('insuranceplan-list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(response.data['results'][0]['name'], self.plan.name)
        self.logger.log_test_result(
            "test_list_plans",
            "PASS",
            time.time() - start_time
        )

    def test_create_plan(self):
        self.logger.log_test_start("test_create_plan")
        start_time = time.time()
        """Test creating a new insurance plan."""
        url = reverse('insuranceplan-list')
        self.authenticate_user(self.admin_user)
        data = {
            'name': 'Premium Plan',
            'plan_type': 'premium',
            'provider': 'Premium Insurance Co',
            'description': 'A premium insurance plan',
            'coverage_details': 'Premium Coverage Details',
            'eligibility_criteria': 'Premium eligibility criteria',
            'monthly_premium': '1000.00',
            'deductible': '2000.00',
            'copay': '30.00',
            'max_coverage': '200000.00',
            'network_hospitals': 'Hospital X, Hospital Y'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Premium Plan')
        self.logger.log_test_result(
            "test_create_plan",
            "PASS",
            time.time() - start_time
        )
        self.logger.log_test_result(
            "test_create_plan",
            "PASS",
            time.time() - start_time
        )

    def test_analyze_plan(self):
        self.logger.log_test_start("test_analyze_plan")
        start_time = time.time()
        """Test analyzing an insurance plan."""
        url = reverse('insuranceplan-analyze', kwargs={'pk': self.plan.pk})
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('analysis', response.data)
        self.logger.log_test_result(
            "test_analyze_plan",
            "PASS",
            time.time() - start_time
        )
        self.logger.log_test_result(
            "test_analyze_plan",
            "PASS",
            time.time() - start_time
        )

    def test_similar_plans(self):
        self.logger.log_test_start("test_similar_plans")
        start_time = time.time()
        """Test finding similar insurance plans."""
        second_plan = InsurancePlan.objects.create(
            name='Second Plan',
            plan_type='standard',
            provider='Second Insurance Co',
            description='A standard insurance plan',
            coverage_details='Extended Coverage Details',
            eligibility_criteria='Extended eligibility criteria',
            monthly_premium=Decimal('750.00'),
            deductible=Decimal('1500.00'),
            copay=Decimal('25.00'),
            max_coverage=Decimal('150000.00'),
            network_hospitals='Hospital C, Hospital D'
        )
        
        url = reverse('insuranceplan-similar-plans', kwargs={'pk': self.plan.pk})
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.logger.log_test_result(
            "test_similar_plans",
            "PASS",
            time.time() - start_time
        )

    def test_get_recommendations(self):
        self.logger.log_test_start("test_get_recommendations")
        start_time = time.time()
        """Test getting recommendations for authenticated user."""
        url = reverse('insuranceplan-recommendations')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertIn('suitability_score', response.data['results'][0])
        self.logger.log_test_result(
            "test_get_recommendations",
            "PASS",
            time.time() - start_time
        )

class FeedbackTests(InsuranceBaseTestCase):
    """Test cases for FeedbackViewSet."""

    def test_create_feedback(self):
        self.logger.log_test_start("test_create_feedback")
        start_time = time.time()
        """Test creating new feedback."""
        url = reverse('feedback-list')
        self.authenticate_user()
        data = {
            'rating': 5,
            'comments': 'Excellent service and support!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['user'], self.user.pk)
        self.logger.log_test_result(
            "test_create_feedback",
            "PASS",
            time.time() - start_time
        )

    def test_list_feedback_as_user(self):
        self.logger.log_test_start("test_list_feedback_as_user")
        start_time = time.time()
        """Test that users can only see their own feedback."""
        url = reverse('feedback-list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(response.data['results'][0]['user'], self.user.pk)
        self.logger.log_test_result(
            "test_list_feedback_as_user",
            "PASS",
            time.time() - start_time
        )
