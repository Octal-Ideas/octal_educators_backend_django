from rest_framework import serializers
from .models import Course, Department, Teacher, Lecture


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'thumbnail')
        read_only_fields = ('created_by', 'created_at', 'modified_at')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'address', 'department', 'total_time', 'user')
        read_only_fields = ('created_by', 'created_at', 'modified_at')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'title', 'description',
                  'video_url', 'content', 'course')
        read_only_fields = ('created_by', 'created_at', 'modified_at')


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    teacher = TeacherSerializer()
    # Serializes the lecturers for the Course
    lecturers = LectureSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'description', 'prerequisites', 'department',
                  'cover', 'teacher', 'price_all', 'price_per', 'department', 'lecturers')
        read_only_fields = ('created_by', 'created_at', 'modified_at')


class PublicCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'description',
                  'prerequisites', 'cover', 'price_all', 'price_per')
        read_only_fields = ('created_by', 'created_at', 'modified_at')
