from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Optional

class User(AbstractUser):
    """Custom user model for the health insurance system."""
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    family_size = models.IntegerField(null=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

class InsurancePlan(models.Model):
    """Model for storing insurance plan details."""
    name = models.CharField(max_length=255)
    coverage = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def price_per_month(self) -> float:
        """Calculate monthly price of the insurance plan."""
        return float(self.price) / 12

class Feedback(models.Model):
    """Model for storing user feedback on insurance plans."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user.username}'s feedback - {self.rating} stars"

    @property
    def summary(self) -> str:
        """Get a brief summary of the feedback."""
        return f"{self.rating} stars - {self.comments[:50]}..."
