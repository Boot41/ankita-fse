from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from typing import Any, Dict, List
from decimal import Decimal

from .models import User, InsurancePlan, Feedback, PlanComparison, UserDashboardPreference
from .serializers import (UserSerializer, InsurancePlanSerializer, FeedbackSerializer,
                        PlanComparisonSerializer, UserDashboardPreferenceSerializer)
from gemini_client import get_insurance_recommendation, analyze_insurance_plan

from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User registration and management."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Allow registration without authentication."""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get the current user's details."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def get_ai_recommendation(self, request, pk=None):
        """Get AI-powered insurance recommendations for a user."""
        try:
            user = self.get_object()
            
            # Validate required user data
            if not all([user.age, user.budget, user.family_size]):
                raise ValidationError(
                    'Please complete your profile with age, budget, and family size '
                    'to receive personalized recommendations.'
                )
            
            # Check cache first
            cache_key = f'user_recommendation_{user.id}'
            cached_recommendation = cache.get(cache_key)
            if cached_recommendation:
                return Response({'recommendation': cached_recommendation, 'cached': True})
            
            user_data = {
                'age': user.age,
                'budget': float(user.budget),
                'family_size': user.family_size,
                'medical_history': user.medical_history or 'No medical history provided'
            }
            
            recommendation = get_insurance_recommendation(user_data)
            
            # Cache the recommendation for 1 hour
            cache.set(cache_key, recommendation, 3600)
            
            return Response({
                'recommendation': recommendation,
                'cached': False
            })
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Failed to generate recommendation. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def recommended_plans(self, request, pk=None):
        """Get a list of recommended insurance plans for the user."""
        try:
            user = self.get_object()
            
            if not user.budget:
                raise ValidationError('Please set your budget to receive plan recommendations.')
            
            # Get all active plans within user's budget
            plans = InsurancePlan.objects.filter(
                is_active=True,
                monthly_premium__lte=user.budget
            ).order_by('monthly_premium')
            
            if not plans:
                return Response({
                    'message': 'No plans found within your budget. Consider adjusting your budget.'
                })
            
            recommendations = []
            for plan in plans:
                plan_data = {
                    'id': plan.id,
                    'name': plan.name,
                    'monthly_premium': float(plan.monthly_premium),
                    'coverage_details': plan.coverage_details,
                    'suitability_score': self._calculate_suitability_score(plan, user)
                }
                recommendations.append(plan_data)
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
            
            return Response({'recommendations': recommendations[:5]})
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Failed to get recommendations. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _calculate_suitability_score(self, plan: InsurancePlan, user: User) -> float:
        """Calculate how suitable a plan is for a user (0-1 score)."""
        score = 1.0
        
        # Budget factor (0-0.4)
        budget_ratio = float(plan.monthly_premium) / float(user.budget)
        score *= 0.4 * (1 - budget_ratio) + 0.6
        
        # Age factor (0-0.3)
        if user.age > 60 and 'senior' in plan.coverage_details.lower():
            score *= 1.3
        elif user.age < 30 and 'young' in plan.coverage_details.lower():
            score *= 1.3
        
        # Family size factor (0-0.3)
        if user.family_size > 1 and 'family' in plan.coverage_details.lower():
            score *= 1.3
        elif user.family_size == 1 and 'individual' in plan.coverage_details.lower():
            score *= 1.3
        
        return min(1.0, score)

class InsurancePlanViewSet(viewsets.ModelViewSet):
    """ViewSet for insurance plan management."""
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def analyze(self, request, pk=None):
        """Get AI analysis of an insurance plan."""
        try:
            plan = self.get_object()
            
            # Check cache first
            cache_key = f'plan_analysis_{plan.id}'
            cached_analysis = cache.get(cache_key)
            if cached_analysis:
                return Response({'analysis': cached_analysis, 'cached': True})
            
            plan_data = {
                'name': plan.name,
                'coverage': plan.coverage_details,
                'price': float(plan.monthly_premium),
                'conditions': plan.eligibility_criteria
            }
            
            analysis = analyze_insurance_plan(plan_data)
            
            # Cache the analysis for 24 hours since plan details don't change often
            cache.set(cache_key, analysis, 86400)
            
            return Response({
                'analysis': analysis,
                'cached': False
            })
            
        except Exception as e:
            return Response(
                {'error': 'Failed to analyze plan. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def similar_plans(self, request, pk=None):
        """Find similar insurance plans."""
        try:
            plan = self.get_object()
            price_range = Decimal('100.00')
            
            similar_plans = InsurancePlan.objects.filter(
                monthly_premium__gte=plan.monthly_premium - price_range,
                monthly_premium__lte=plan.monthly_premium + price_range
            ).exclude(id=plan.id)[:5]
            
            serializer = self.get_serializer(similar_plans, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': 'Failed to find similar plans.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def compare(self, request):
        """Compare multiple insurance plans."""
        plan_ids = request.data.get('plan_ids', [])
        if not plan_ids:
            return Response(
                {'error': 'No plan IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plans = InsurancePlan.objects.filter(id__in=plan_ids)
        comparisons = []
        
        for plan in plans:
            plan_data = {
                'name': plan.name,
                'coverage': plan.coverage,
                'price': float(plan.price),
                'conditions': plan.conditions
            }
            analysis = analyze_insurance_plan(plan_data)
            comparisons.append({
                'plan': InsurancePlanSerializer(plan).data,
                'analysis': analysis
            })
        
        return Response(comparisons)

class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user feedback."""
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Associate feedback with the current user."""
        serializer.save(user=self.request.user)


class PlanComparisonViewSet(viewsets.ModelViewSet):
    """ViewSet for managing plan comparisons."""
    serializer_class = PlanComparisonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset to user's comparisons."""
        return PlanComparison.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Associate comparison with the current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def detailed_comparison(self, request, pk=None):
        """Get a detailed comparison of the plans."""
        comparison = self.get_object()
        plans = comparison.plans.all()
        
        if len(plans) < 2:
            return Response(
                {'error': 'Need at least 2 plans to compare'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comparison_data = {
            'name': comparison.comparison_name,
            'plans': InsurancePlanSerializer(plans, many=True).data,
            'differences': self._get_plan_differences(plans),
            'recommendation': self._get_comparison_recommendation(plans, request.user)
        }
        
        return Response(comparison_data)
    
    def _get_plan_differences(self, plans):
        """Analyze the differences between plans."""
        differences = {
            'price_range': {
                'min': float(min(p.monthly_premium for p in plans)),
                'max': float(max(p.monthly_premium for p in plans))
            },
            'coverage_differences': [],
            'feature_differences': []
        }
        
        # Add more detailed comparison logic here
        return differences
    
    def _get_comparison_recommendation(self, plans, user):
        """Get a recommendation based on compared plans."""
        best_plan = None
        best_score = 0
        
        for plan in plans:
            score = self._calculate_plan_score(plan, user)
            if score > best_score:
                best_score = score
                best_plan = plan
        
        return {
            'recommended_plan': InsurancePlanSerializer(best_plan).data if best_plan else None,
            'score': best_score
        }
    
    def _calculate_plan_score(self, plan, user):
        """Calculate a plan's suitability score."""
        score = 1.0
        
        if user.budget:
            budget_ratio = float(plan.monthly_premium) / float(user.budget)
            score *= 0.4 * (1 - budget_ratio) + 0.6
        
        if user.age:
            if user.age > 60 and plan.plan_type == 'senior':
                score *= 1.3
            elif user.age < 30 and 'young' in plan.features:
                score *= 1.3
        
        if user.family_size:
            if user.family_size > 1 and plan.plan_type == 'family':
                score *= 1.3
            elif user.family_size == 1 and plan.plan_type == 'basic':
                score *= 1.3
        
        return min(1.0, score)


class UserDashboardPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user dashboard preferences."""
    serializer_class = UserDashboardPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get user's dashboard preferences."""
        return UserDashboardPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Associate preferences with the current user."""
        # Delete existing preferences if any
        UserDashboardPreference.objects.filter(user=self.request.user).delete()
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current_preferences(self, request):
        """Get current user's dashboard preferences."""
        preferences = UserDashboardPreference.objects.filter(user=request.user).first()
        if not preferences:
            # Create default preferences
            preferences = UserDashboardPreference.objects.create(
                user=request.user,
                default_view='grid',
                show_premium_first=False,
                notification_preferences={},
                widgets_order=['recommendations', 'recent_plans', 'feedback']
            )
        
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)
