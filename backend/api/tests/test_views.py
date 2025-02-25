from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.core.exceptions import ValidationError
from api.models import User, InsurancePlan, Feedback
from api.recommendation_engine import calculate_plan_score, get_recommendations

class TestUserViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            'name': 'Test User',
            'age': 30,
            'budget': '5000.00',
            'family_size': 2,
            'medical_history': 'No major issues'
        }
        self.user = None
        
    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        
    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data"""
        url = reverse('user-list')
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_registration_duplicate_username(self):
        """Test user registration with duplicate username"""
        url = reverse('user-list')
        # Create first user
        self.client.post(url, self.user_data, format='json')
        # Try to create second user with same username
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile(self):
        """Test retrieving user profile"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

class TestInsurancePlanViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            age=30,
            budget=Decimal('5000.00'),
            family_size=2,
            medical_history='No major issues'
        )
        self.client.force_authenticate(user=self.user)
        self.plan = InsurancePlan.objects.create(
            name='Test Plan',
            coverage='Basic Coverage',
            price=Decimal('2000.00'),
            conditions='Standard conditions'
        )
        self.plan2 = InsurancePlan.objects.create(
            name='Family Plan',
            coverage='Family Coverage',
            price=Decimal('4000.00'),
            conditions='Premium conditions'
        )

    def test_list_plans(self):
        """Test listing insurance plans"""
        url = reverse('insuranceplan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_list_plans_unauthenticated(self):
        """Test listing plans without authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('insuranceplan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_plan_detail(self):
        """Test getting single plan details"""
        url = reverse('insuranceplan-detail', args=[self.plan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.plan.name)

    def test_plan_comparison(self):
        """Test plan comparison endpoint"""
        url = reverse('insuranceplan-compare')
        response = self.client.post(url, {'plan_ids': [self.plan.id, self.plan2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_plan_comparison_empty_ids(self):
        """Test plan comparison with no plan IDs"""
        url = reverse('insuranceplan-compare')
        response = self.client.post(url, {'plan_ids': []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_plan_eligibility(self):
        """Test plan eligibility check"""
        url = reverse('insuranceplan-eligible', args=[self.plan.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        
    def test_plan_eligibility_over_budget(self):
        """Test plan eligibility when plan is over budget"""
        expensive_plan = InsurancePlan.objects.create(
            name='Expensive Plan',
            coverage='Premium Coverage',
            price=Decimal('10000.00'),
            conditions='Premium conditions'
        )
        url = reverse('insuranceplan-eligible', args=[expensive_plan.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['eligible'])

class TestRecommendationViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            age=30,
            budget=Decimal('5000.00'),
            family_size=2,
            medical_history='No issues'
        )
        self.client.force_authenticate(user=self.user)
        # Create multiple plans for testing recommendations
        self.plans = [
            InsurancePlan.objects.create(
                name='Family Plan',
                coverage='Family Coverage',
                price=Decimal('4000.00'),
                conditions='Standard conditions'
            ),
            InsurancePlan.objects.create(
                name='Individual Plan',
                coverage='Individual Coverage',
                price=Decimal('2000.00'),
                conditions='Basic conditions'
            ),
            InsurancePlan.objects.create(
                name='Senior Plan',
                coverage='Senior Coverage',
                price=Decimal('3000.00'),
                conditions='Senior conditions'
            )
        ]

    def test_get_recommendations(self):
        """Test getting personalized recommendations"""
        response = self.client.post('/api/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)
        
    def test_get_recommendations_unauthenticated(self):
        """Test getting recommendations without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_calculate_plan_score(self):
        """Test plan score calculation"""
        user_data = {
            'age': 30,
            'budget': Decimal('5000.00'),
            'family_size': 2,
            'medical_history': 'No issues'
        }
        score = calculate_plan_score(self.plans[0], user_data)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)

class TestFeedbackViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.plan = InsurancePlan.objects.create(
            name='Test Plan',
            coverage='Basic Coverage',
            price=Decimal('2000.00'),
            conditions='Standard conditions'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_feedback(self):
        """Test creating feedback"""
        url = reverse('feedback-list')
        data = {
            'rating': 5,
            'comments': 'Great service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(Feedback.objects.get().rating, 5)
        
    def test_create_feedback_invalid_rating(self):
        """Test creating feedback with invalid rating"""
        url = reverse('feedback-list')
        data = {
            'rating': 6,  # Invalid rating > 5
            'comments': 'Great service!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_feedback(self):
        """Test listing user's feedback"""
        Feedback.objects.create(user=self.user, rating=5, comments='Great!')
        url = reverse('feedback-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_list_all_feedback_as_admin(self):
        """Test listing all feedback as admin user"""
        Feedback.objects.create(user=self.user, rating=5, comments='Great!')
        Feedback.objects.create(user=self.admin_user, rating=4, comments='Good!')
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('feedback-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_feedback_summary(self):
        """Test feedback summary property"""
        feedback = Feedback.objects.create(
            user=self.user,
            rating=5,
            comments='This is a very long comment that should be truncated in the summary',

        )
        self.assertTrue(len(feedback.summary) <= 55)  # 50 chars + '...'
