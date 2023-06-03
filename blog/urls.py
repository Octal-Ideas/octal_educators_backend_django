# Import necessary modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register('blogs', views.BlogViewSet, basename='blogs'),
router.register('comments', views.CommentViewSet, basename='comments'),
router.register('categories', views.CategoryViewSet, basename='categories'),
router.register('view-counts', views.ViewCountViewSet, basename='view-counts'),

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:pk>/like/', views.post_like, name='post_like')
    path('blogs/<int:blog_id>/subscribe/', views.subscribe_to_blog, name='subscribe_to_blog'),
    path('blogs/<int:blog_id>/unsubscribe/', views.unsubscribe_from_blog, name='unsubscribe_from_blog'),
     path('blogs/<int:blog_id>/check-subscription/', views.is_user_subscribed, name='check_subscription'),
     path('blogs/<int:blog_id>/subscribers/', list_subscribers, name='list_subscribers'),
    
]
