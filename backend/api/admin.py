from django.contrib import admin
from .models import User, InsurancePlan, Feedback

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'name', 'age', 'budget', 'family_size']
    search_fields = ['username', 'email', 'name']
    list_filter = ['age', 'family_size']

@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'price_per_month', 'created_at']
    search_fields = ['name', 'coverage', 'conditions']
    list_filter = ['created_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    search_fields = ['user__username', 'comments']
    list_filter = ['rating', 'created_at']
