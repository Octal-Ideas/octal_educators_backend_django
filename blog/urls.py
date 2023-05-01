# Import necessary modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register('blogs', views.BlogViewSet, basename='blogs'),
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('view-counts', views.ViewCountViewSet, basename='view-counts')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:pk>/like/', views.post_like, name='post_like')
    
]
