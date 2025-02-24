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
    """
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='10/m', method=['GET']))
    def list(self, request: Request) -> Response:
        """Get personalized insurance recommendations."""
        try:
            user_data = {
                'age': request.user.age,
                'budget': request.user.budget,
                'family_size': request.user.family_size,
                'medical_history': request.user.medical_history
            }
            recommendations = get_recommendations(user_data)
            return Response(recommendations)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user feedback.
    Users can only view their own feedback unless they're staff.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            queryset = Feedback.objects.all()
        else:
            queryset = Feedback.objects.filter(user=self.request.user)
        return queryset.order_by('-created_at')[:5]  # Return only last 5 feedback items

    def perform_create(self, serializer: FeedbackSerializer) -> None:
        """Associate feedback with the current user."""
        serializer.save(user=self.request.user)
