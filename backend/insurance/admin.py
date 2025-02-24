from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, InsurancePlan, Feedback, 
    PlanComparison, UserDashboardPreference
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'budget', 'family_size')
    list_filter = ('is_staff', 'is_active', 'age')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age', 'budget', 'family_size', 'medical_history', 'medical_conditions')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('age', 'budget', 'family_size', 'medical_history', 'medical_conditions')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'provider', 'monthly_premium', 'is_active')
    list_filter = ('plan_type', 'provider', 'is_active')
    search_fields = ('name', 'provider', 'description')
    ordering = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'rating', 'created_at')
    list_filter = ('feedback_type', 'rating', 'created_at')
    search_fields = ('user__username', 'comments')
    ordering = ('-created_at',)

@admin.register(PlanComparison)
class PlanComparisonAdmin(admin.ModelAdmin):
    list_display = ('user', 'comparison_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'comparison_name', 'notes')
    ordering = ('-created_at',)

@admin.register(UserDashboardPreference)
class UserDashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_view', 'show_premium_first')
    list_filter = ('default_view', 'show_premium_first')
    search_fields = ('user__username',)
    ordering = ('user__username',)
