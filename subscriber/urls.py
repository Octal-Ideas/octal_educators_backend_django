from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriberViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'subscribers', SubscriberViewSet, basename='subscriber')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),

    
]