from rest_framework import serializers
from .models import User, InsurancePlan, Feedback
from typing import Dict, Any

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'name', 'age', 
                 'budget', 'family_size', 'medical_history', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create and return a new user with encrypted password."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            age=validated_data.get('age'),
            budget=validated_data.get('budget'),
            family_size=validated_data.get('family_size'),
            medical_history=validated_data.get('medical_history', '')
        )
        return user

class InsurancePlanSerializer(serializers.ModelSerializer):
    """Serializer for the InsurancePlan model."""
    price_per_month = serializers.FloatField(read_only=True)

    class Meta:
        model = InsurancePlan
        fields = ['id', 'name', 'coverage', 'price', 'price_per_month', 
                 'conditions', 'created_at']
        read_only_fields = ['created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the Feedback model."""
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    summary = serializers.CharField(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'rating', 'comments', 'summary', 'created_at']
        read_only_fields = ['created_at']

    def validate_rating(self, value: int) -> int:
        """Validate that rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
