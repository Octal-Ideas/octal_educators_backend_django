# Import necessary modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register('departments', views.DepartmentViewSet, basename='departments')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('lectures', views.LectureViewSet, basename='lectures')
router.register('courses', views.CourseViewSet, basename='courses')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),

]
