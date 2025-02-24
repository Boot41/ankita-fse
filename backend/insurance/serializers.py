from rest_framework import serializers
from .models import (CustomUser, InsurancePlan, Feedback, Recommendation,
                    PlanComparison, UserDashboardPreference)
from typing import Dict, Any

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name',
                 'age', 'budget', 'family_size', 'medical_history', 'medical_conditions',
                 'preferred_hospital_network', 'is_profile_complete', 'dark_mode_enabled',
                 'created_at']
        read_only_fields = ['created_at', 'is_profile_complete']

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """Create and return a new user with encrypted password."""
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
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
                 'max_coverage', 'network_hospitals', 'features', 'is_active',
                 'popularity_score', 'created_at']
        read_only_fields = ['created_at', 'popularity_score']

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
