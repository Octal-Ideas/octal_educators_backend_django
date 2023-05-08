from rest_framework import serializers
from .models import Course, Department, Teacher, Lecture

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    teacher = TeacherSerializer()
    lectures = LectureSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
        
