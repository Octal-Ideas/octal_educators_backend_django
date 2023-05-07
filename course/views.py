from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.throttling import UserRateThrottle

from .models import Course, Department, Teacher, Lecture
from .serializers import CourseSerializer, DepartmentSerializer, TeacherSerializer, LectureSerializer
from .pagination import CourseLimitOffsetPagination
from .throttles import CourseRateThrottle
class DepartmentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class TeacherList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class LectureList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class LectureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class CourseList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 
    pagination_class = CourseLimitOffsetPagination
    throttle_classes = [UserRateThrottle, CourseRateThrottle]

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
