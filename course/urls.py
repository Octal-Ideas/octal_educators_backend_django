# Import necessary modules
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register('departments', views.DepartmentList, basename='departments'),
router.register('departments/<uuid:pk>',
                views.DepartmentDetail, basename='department'),
router.register('teachers', views.TeacherList, basename='teachers'),
router.register('teachers/<uuid:pk>', views.TeacherDetail, basename='teacher'),
router.register('lectures', views.LectureList, basename='lectures'),
router.register('lectures/<uuid:pk>', views.LectureDetail, basename='lecture'),
router.register('courses', views.CourseList, basename='courses'),
router.register('courses/<uuid:pk>', views.CourseDetail, basename='course'),

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),

]
