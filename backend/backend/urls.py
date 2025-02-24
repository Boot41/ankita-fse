"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from insurance.password_reset import request_password_reset, reset_password
from rest_framework.documentation import include_docs_urls
from insurance.views import (UserViewSet, InsurancePlanViewSet, FeedbackViewSet,
                          PlanComparisonViewSet, UserDashboardPreferenceViewSet)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'plans', InsurancePlanViewSet)
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'comparisons', PlanComparisonViewSet, basename='comparison')
router.register(r'dashboard-preferences', UserDashboardPreferenceViewSet, basename='dashboard-preference')

urlpatterns = [
    # Redirect root URL to API docs
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    
    # Admin and API URLs
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password-reset/', request_password_reset, name='password_reset'),
    path('api/password-reset/confirm/', reset_password, name='password_reset_confirm'),
    path('api-auth/', include('rest_framework.urls')),  # Adds login to browsable API
]
