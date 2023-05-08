from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework import viewsets, permissions, throttling

from .models import Course, Department, Teacher, Lecture
from .serializers import CourseSerializer, DepartmentSerializer, TeacherSerializer, LectureSerializer
from .pagination import CourseLimitOffsetPagination
from .throttles import CourseRateThrottle


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeacherViewSet(viewsets.ModelViewSet, UserPassesTestMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def test_func(self):
        return self.request.user.groups.filter(name='teacher').exists()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LectureViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLimitOffsetPagination
    throttle_classes = [throttling.UserRateThrottle, CourseRateThrottle]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
