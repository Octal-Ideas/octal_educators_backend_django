from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework import viewsets, permissions, throttling

from .models import Course, Department, Teacher, Lecture
from .serializers import CourseSerializer, DepartmentSerializer, TeacherSerializer, LectureSerializer, PublicCourseSerializer
from .pagination import CourseLimitOffsetPagination
from .throttles import CourseRateThrottle
from account.permissions import IsTeacherOrReadOnly, IsStudent


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        # Returns the list of permissions that this view requires
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeacherViewSet(viewsets.ModelViewSet, UserPassesTestMixin):
    permission_classes = [IsTeacherOrReadOnly]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_permissions(self):
        # Apply appropriate permissions based on the request method
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated, IsStudent]
        else:
            permission_classes = [
                permissions.IsAuthenticated, IsTeacherOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrReadOnly]
    queryset = Course.objects.all()
    pagination_class = CourseLimitOffsetPagination
    throttle_classes = [throttling.UserRateThrottle, CourseRateThrottle]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return CourseSerializer
        else:
            return PublicCourseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
