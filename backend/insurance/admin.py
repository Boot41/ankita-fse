from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    User, InsurancePlan, Feedback,
    PlanComparison, UserDashboardPreference, Recommendation
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'age', 'budget_display', 'family_size', 'medical_history_display')
    list_filter = ('is_staff', 'is_active', 'age')
    fieldsets = UserAdmin.fieldsets + (
        ('Health Information', {
            'fields': ('age', 'medical_history'),
            'classes': ('wide',)
        }),
        ('Insurance Details', {
            'fields': ('budget', 'family_size'),
            'classes': ('wide',)
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Health Information', {
            'fields': ('age', 'medical_history'),
            'classes': ('wide',)
        }),
        ('Insurance Details', {
            'fields': ('budget', 'family_size'),
            'classes': ('wide',)
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def budget_display(self, obj):
        return f'${obj.budget}' if obj.budget else '-'
    budget_display.short_description = 'Monthly Budget'

    def medical_history_display(self, obj):
        if not obj.medical_history:
            return '-'
        return obj.medical_history[:50] + '...' if len(obj.medical_history) > 50 else obj.medical_history
    medical_history_display.short_description = 'Medical History'

@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'provider', 'monthly_premium', 'coverage_details')
    list_filter = ('plan_type', 'provider')
    search_fields = ('name', 'provider', 'description')
    ordering = ('name',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'plan_type', 'provider', 'description')
        }),
        ('Coverage Details', {
            'fields': ('coverage_details', 'eligibility_criteria', 'network_hospitals', 'features')
        }),
        ('Financial Information', {
            'fields': ('monthly_premium', 'deductible', 'copay', 'max_coverage')
        }),
        ('Status', {
            'fields': ('is_active', 'popularity_score')
        }),
    )

    def premium_display(self, obj):
        return format_html('<b>${}</b>', obj.monthly_premium)
    premium_display.short_description = 'Monthly Premium'

    def coverage_status(self, obj):
        if obj.max_coverage:
            return format_html('<span style="color: green;">Up to ${}</span>', obj.max_coverage)
        return format_html('<span style="color: orange;">Unlimited</span>')
    coverage_status.short_description = 'Coverage Limit'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'rating_display', 'insurance_plan', 'created_at')
    list_filter = ('feedback_type', 'rating', 'created_at')
    search_fields = ('user__username', 'comments', 'insurance_plan__name')
    ordering = ('-created_at',)

    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_display.short_description = 'Rating'

@admin.register(PlanComparison)
class PlanComparisonAdmin(admin.ModelAdmin):
    list_display = ('user', 'comparison_name', 'plans_count', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'comparison_name', 'notes')
    ordering = ('-created_at',)
    filter_horizontal = ('plans',)

    def plans_count(self, obj):
        count = obj.plans.count()
        return format_html('{} plan{}', count, 's' if count != 1 else '')
    plans_count.short_description = 'Number of Plans'

@admin.register(UserDashboardPreference)
class UserDashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_view', 'show_premium_first', 'widgets_display')
    list_filter = ('default_view', 'show_premium_first')
    search_fields = ('user__username',)
    ordering = ('user__username',)

    def widgets_display(self, obj):
        if not obj.widgets_order:
            return '-'
        return ', '.join(obj.widgets_order)
    widgets_display.short_description = 'Widget Order'

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance_plan', 'score_display', 'status_display', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'insurance_plan__name', 'notes')
    ordering = ('-created_at',)

    def score_display(self, obj):
        color = 'green' if obj.recommendation_score >= 0.7 else 'orange' if obj.recommendation_score >= 0.4 else 'red'
        return format_html('<span style="color: {};">{:.1%}</span>', color, obj.recommendation_score)
    score_display.short_description = 'Confidence Score'

    def status_display(self, obj):
        if obj.is_accepted is None:
            return format_html('<span style="color: blue;">Pending</span>')
        return format_html('<span style="color: {};">✓ Accepted</span>' if obj.is_accepted else '<span style="color: red;">✗ Rejected</span>', 'green')
    status_display.short_description = 'Status'
