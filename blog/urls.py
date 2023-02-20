from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views


router = DefaultRouter()

router.register('blogs', views.BlogViewSet, basename='blogs'),
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('view-counts', views.ViewCountViewSet, basename='view-counts')

urlpatterns =[path('', include(router.urls))]