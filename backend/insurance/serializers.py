from rest_framework import serializers
from .models import (User, InsurancePlan, Feedback, Recommendation,
                    PlanComparison, UserDashboardPreference)
from typing import Dict, Any

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'name',
                 'age', 'budget', 'family_size', 'medical_history',
                 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create and return a new user with encrypted password."""
        name_parts = validated_data.pop('name', '').split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name,
            age=validated_data.get('age'),
            budget=validated_data.get('budget'),
            family_size=validated_data.get('family_size'),
            medical_history=validated_data.get('medical_history', '')
        )
        return user

class InsurancePlanSerializer(serializers.ModelSerializer):
    """Serializer for the InsurancePlan model."""
    class Meta:
        model = InsurancePlan
        fields = ['id', 'name', 'plan_type', 'provider', 'description', 'coverage_details',
                 'eligibility_criteria', 'monthly_premium', 'deductible', 'copay',
                 'max_coverage', 'network_hospitals', 'created_at']
        read_only_fields = ['created_at']

class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for the Recommendation model."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    insurance_plan = InsurancePlanSerializer(read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'insurance_plan', 'recommendation_score',
                 'recommendation_date', 'notes', 'is_accepted', 'accepted_date']
        read_only_fields = ['recommendation_date', 'accepted_date']

class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the Feedback model."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    insurance_plan = InsurancePlanSerializer(read_only=True)
    recommendation = RecommendationSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'feedback_type', 'insurance_plan', 'recommendation',
                 'rating', 'ui_element', 'comments', 'created_at']
        read_only_fields = ['created_at']

    def validate_rating(self, value: int) -> int:
        """Validate that rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class PlanComparisonSerializer(serializers.ModelSerializer):
    """Serializer for the PlanComparison model."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    plans = InsurancePlanSerializer(many=True, read_only=True)
    plan_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = PlanComparison
        fields = ['id', 'user', 'plans', 'plan_ids', 'comparison_name',
                 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data: Dict[str, Any]) -> PlanComparison:
        plan_ids = validated_data.pop('plan_ids')
        comparison = PlanComparison.objects.create(**validated_data)
        comparison.plans.set(InsurancePlan.objects.filter(id__in=plan_ids))
        return comparison

class UserDashboardPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for the UserDashboardPreference model."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserDashboardPreference
        fields = ['id', 'user', 'default_view', 'show_premium_first',
                 'notification_preferences', 'widgets_order',
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
