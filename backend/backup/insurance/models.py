from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from typing import Optional

class User(AbstractUser):
    """Custom user model for the health insurance system."""
    name = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        null=True,
        help_text="User's age in years"
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        help_text="Monthly budget for insurance in dollars"
    )
    family_size = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        help_text="Number of family members to be covered"
    )
    medical_history = models.TextField(
        blank=True,
        help_text="Detailed medical history of the user"
    )
    preferred_hospital_network = models.CharField(
        max_length=100,
        blank=True,
        help_text="Preferred hospital network"
    )
    is_profile_complete = models.BooleanField(
        default=False,
        help_text="Whether the user has completed their profile"
    )
    dark_mode_enabled = models.BooleanField(
        default=False,
        help_text="User's preference for dark mode"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

class InsurancePlan(models.Model):
    """Model for storing insurance plan details."""
    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('family', 'Family'),
        ('senior', 'Senior'),
        ('specialized', 'Specialized')
    ]

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of the insurance plan"
    )
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPE_CHOICES,
        default='basic',
        help_text="Type of insurance plan"
    )
    provider = models.CharField(
        max_length=255,
        help_text="Insurance provider company name"
    )
    description = models.TextField(
        help_text="Brief description of the insurance plan"
    )
    coverage_details = models.TextField(
        help_text="Detailed information about what the plan covers"
    )
    eligibility_criteria = models.TextField(
        help_text="Requirements that must be met to be eligible for this plan"
    )
    monthly_premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Monthly premium cost in dollars"
    )
    deductible = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Annual deductible amount in dollars"
    )
    copay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Copay amount in dollars"
    )
    max_coverage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Maximum coverage amount in dollars"
    )
    network_hospitals = models.TextField(
        blank=True,
        help_text="List of network hospitals (comma-separated)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Insurance Plan"
        verbose_name_plural = "Insurance Plans"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['provider']),
        ]

    def __str__(self):
        return self.name

    def price_per_month(self):
        """Calculate monthly price of the insurance plan."""
        return self.monthly_premium

class Feedback(models.Model):
    """Model for storing user feedback on insurance plans."""
    FEEDBACK_TYPE_CHOICES = [
        ('recommendation', 'Recommendation'),
        ('plan', 'Insurance Plan'),
        ('ui', 'User Interface'),
        ('general', 'General')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedback',
        help_text="User who provided the feedback"
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPE_CHOICES,
        default='general',
        help_text="Type of feedback"
    )
    insurance_plan = models.ForeignKey(
        InsurancePlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedback',
        help_text="Insurance plan this feedback is about"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    ui_element = models.CharField(
        max_length=100,
        blank=True,
        help_text="UI element this feedback is about"
    )
    comments = models.TextField(
        blank=True,
        help_text="Additional comments or feedback"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s feedback on {self.feedback_type}"

    def summary(self):
        """Get a brief summary of the feedback."""
        return f"{self.rating} stars - {self.comments[:50]}..."

class Recommendation(models.Model):
    """Model for storing AI-generated insurance plan recommendations."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recommendations',
        help_text="User receiving the recommendation"
    )
    insurance_plan = models.ForeignKey(
        InsurancePlan,
        on_delete=models.CASCADE,
        related_name='recommendations',
        help_text="Recommended insurance plan"
    )
    recommendation_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="AI confidence score for this recommendation (0-1)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or explanation for the recommendation"
    )
    is_accepted = models.BooleanField(
        default=None,
        null=True,
        help_text="Whether the user accepted this recommendation"
    )
    accepted_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the user accepted/rejected this recommendation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['recommendation_score']),
        ]

    def __str__(self):
        return f"Recommendation for {self.user.username}"

    def accept(self):
        """Mark the recommendation as accepted."""
        self.is_accepted = True
        self.accepted_date = timezone.now()
        self.save()

    def reject(self):
        """Mark the recommendation as rejected."""
        self.is_accepted = False
        self.accepted_date = timezone.now()
        self.save()

class PlanComparison(models.Model):
    """Model for storing user's plan comparisons."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comparisons',
        help_text="User who created the comparison"
    )
    plans = models.ManyToManyField(
        InsurancePlan,
        related_name='comparisons',
        help_text="Plans being compared"
    )
    comparison_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional name for this comparison"
    )
    notes = models.TextField(
        blank=True,
        help_text="User notes about the comparison"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan Comparison"
        verbose_name_plural = "Plan Comparisons"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s comparison - {self.comparison_name}"

class UserDashboardPreference(models.Model):
    """Model for storing user's dashboard preferences."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_preferences',
        help_text="User whose preferences these are"
    )
    default_view = models.CharField(
        max_length=20,
        choices=[
            ('list', 'List View'),
            ('grid', 'Grid View'),
            ('compact', 'Compact View')
        ],
        default='grid',
        help_text="User's preferred view type"
    )
    show_premium_first = models.BooleanField(
        default=False,
        help_text="Whether to prioritize premium plans in display"
    )
    notification_preferences = models.JSONField(
        default=dict,
        help_text="JSON object containing notification preferences"
    )
    widgets_order = models.TextField(
        blank=True,
        default='',
        help_text="Order of dashboard widgets (comma-separated)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dashboard Preference"
        verbose_name_plural = "Dashboard Preferences"

    def __str__(self):
        return f"{self.user.username}'s dashboard preferences"
