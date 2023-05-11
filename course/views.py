from django.contrib.auth.mixins import UserPassesTestMixin

from rest_framework import viewsets, permissions, throttling

from .models import Course, Department, Teacher, Lecture
from .serializers import CourseSerializer, DepartmentSerializer, TeacherSerializer, LectureSerializer,PublicCourseSerializer
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LectureViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
