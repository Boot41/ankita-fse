from django.test import TestCase
from decimal import Decimal
from api.models import InsurancePlan
from api.recommendation_engine import calculate_plan_score, get_recommendations

class TestRecommendationEngine(TestCase):
    def setUp(self):
        self.family_plan = InsurancePlan.objects.create(
            name='Family Plan',
            coverage='Comprehensive family coverage',
            price=Decimal('5000.00'),
            conditions='Standard family plan conditions'
        )
        self.individual_plan = InsurancePlan.objects.create(
            name='Individual Plan',
            coverage='Basic individual coverage',
            price=Decimal('2000.00'),
            conditions='Standard individual plan conditions'
        )
        self.senior_plan = InsurancePlan.objects.create(
            name='Senior Plan',
            coverage='Senior citizen coverage',
            price=Decimal('3000.00'),
            conditions='Senior plan conditions'
        )

    def test_calculate_plan_score_budget_consideration(self):
        """Test plan scoring based on budget"""
        user_data = {'budget': '6000.00'}
        score = calculate_plan_score(self.family_plan, user_data)
        self.assertGreater(score, 0.6)  # Score should be good as plan is within budget

        user_data = {'budget': '4000.00'}
        score = calculate_plan_score(self.family_plan, user_data)
        self.assertLess(score, 0.8)  # Score should be lower as plan is over budget

    def test_calculate_plan_score_family_size(self):
        """Test plan scoring based on family size"""
        user_data = {'family_size': 3}
        score = calculate_plan_score(self.family_plan, user_data)
        self.assertGreater(score, 0.8)  # Score should be boosted for family plan

        score = calculate_plan_score(self.individual_plan, user_data)
        self.assertLess(score, 1.0)  # Score should be lower for individual plan

    def test_calculate_plan_score_age(self):
        """Test plan scoring based on age"""
        user_data = {'age': 65}
        score = calculate_plan_score(self.senior_plan, user_data)
        self.assertGreater(score, 0.8)  # Score should be boosted for senior plan

        user_data = {'age': 30}
        score = calculate_plan_score(self.senior_plan, user_data)
        self.assertLess(score, 1.0)  # Score should be lower for senior plan

    def test_get_recommendations_sorting(self):
        """Test recommendations are properly sorted by score"""
        user_data = {
            'age': 35,
            'budget': '6000.00',
            'family_size': 3,
            'medical_history': 'No major issues'
        }
        recommendations = get_recommendations(user_data)
        
        # Verify recommendations are sorted by score
        scores = [rec['suitability_score'] for rec in recommendations]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_get_recommendations_limit(self):
        """Test recommendations are limited to top 5"""
        # Create more plans
        for i in range(6):
            InsurancePlan.objects.create(
                name=f'Extra Plan {i}',
                coverage='Basic coverage',
                price=Decimal('2000.00'),
                conditions='Standard conditions'
            )

        user_data = {
            'age': 35,
            'budget': '6000.00',
            'family_size': 1
        }
        recommendations = get_recommendations(user_data)
        self.assertLessEqual(len(recommendations), 5)  # Should return max 5 recommendations

    def test_get_recommendations_fields(self):
        """Test recommendation response structure"""
        user_data = {
            'age': 35,
            'budget': '6000.00',
            'family_size': 1
        }
        recommendations = get_recommendations(user_data)
        for rec in recommendations:
            self.assertIn('id', rec)
            self.assertIn('name', rec)
            self.assertIn('coverage', rec)
            self.assertIn('price', rec)
            self.assertIn('price_per_month', rec)
            self.assertIn('conditions', rec)
            self.assertIn('suitability_score', rec)
            self.assertIsInstance(rec['suitability_score'], float)
            self.assertGreaterEqual(rec['suitability_score'], 0)
            self.assertLessEqual(rec['suitability_score'], 1)
