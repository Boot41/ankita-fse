from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'plans', views.InsurancePlanViewSet)
router.register(r'recommendations', views.RecommendationViewSet, basename='recommendation')
router.register(r'feedback', views.FeedbackViewSet, basename='feedback')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
