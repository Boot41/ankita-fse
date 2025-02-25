from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import QuerySet
from typing import Any, Dict
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import User, InsurancePlan, Feedback
from .serializers import UserSerializer, InsurancePlanSerializer, FeedbackSerializer
from .recommendation_engine import get_recommendations
from .llm_utils import GeminiHandler

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User registration and management.
    Rate limited to 5 requests per minute for create operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Allow registration without auth."""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request: Request) -> Response:
        """Get current user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class InsurancePlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for insurance plan management.
    Includes endpoints for plan comparison and eligibility checks.
    """
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def compare(self, request: Request) -> Response:
        """Compare multiple insurance plans."""
        plan_ids = request.data.get('plan_ids', [])
        if not plan_ids:
            return Response(
                {'error': 'No plan IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        plans = InsurancePlan.objects.filter(id__in=plan_ids)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def eligible(self, request: Request, pk: int = None) -> Response:
        """Check eligibility for a specific plan."""
        plan = self.get_object()
        user_data = {
            'age': request.user.age,
            'budget': request.user.budget,
            'family_size': request.user.family_size,
            'medical_history': request.user.medical_history
        }

        # Simple eligibility check based on budget
        if user_data['budget'] and float(user_data['budget']) < plan.price:
            return Response({
                'eligible': False,
                'reason': 'Plan price exceeds budget'
            })

        return Response({'eligible': True})

class RecommendationViewSet(viewsets.ViewSet):
    """
    ViewSet for getting insurance plan recommendations.
    Rate limited to 10 requests per minute.
    Includes AI-powered personalized recommendations.
    """
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gemini = GeminiHandler()

    @method_decorator(ratelimit(key='user', rate='10/m', method=['GET']))
    def list(self, request: Request) -> Response:
        """Get personalized insurance recommendations with AI analysis."""
        try:
            user_data = {
                'age': request.user.age,
                'budget': request.user.budget,
                'family_size': request.user.family_size,
                'medical_history': request.user.medical_history
            }

            # Get base recommendations from existing logic
            base_recommendations = get_recommendations(user_data)

            # For now, return only the base recommendations without AI analysis
            response_data = {
                'recommended_plans': base_recommendations
            }

            return Response(response_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user feedback.
    Users can only view their own feedback unless they're staff.
    Includes AI-powered feedback analysis.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gemini = GeminiHandler()

    def get_queryset(self) -> QuerySet:
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            queryset = Feedback.objects.all()
        else:
            queryset = Feedback.objects.filter(user=self.request.user)
        return queryset.order_by('-created_at')[:5]  # Return only last 5 feedback items

    async def perform_create(self, serializer: FeedbackSerializer) -> None:
        """Associate feedback with the current user and analyze feedback."""
        # Save the feedback first
        feedback = serializer.save(user=self.request.user)

        try:
            # Analyze the feedback using Gemini
            analysis = await self.gemini.analyze_feedback(feedback.comments)
            
            # Update the feedback with the analysis summary
            feedback.summary = analysis['analysis'][:200]  # Limit summary to 200 chars
            feedback.save()
        except Exception as e:
            # Log the error but don't fail the feedback submission
            print(f"Error analyzing feedback: {str(e)}")

    @action(detail=False, methods=['get'])
    async def analytics(self, request: Request) -> Response:
        """Get AI-powered analytics of all feedback."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can access feedback analytics'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Get all feedback
            feedbacks = self.get_queryset().values_list('comments', flat=True)
            
            # Combine all feedback for analysis
            combined_feedback = '\n'.join(feedbacks)
            
            # Get AI analysis of all feedback
            analysis = await self.gemini.analyze_feedback(combined_feedback)
            
            return Response(analysis)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
