from django.shortcuts import render

from django.db.models import Q
from django.db import models
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer

from blog.models import Blog, Category
from course.models import Course, Department, Lecture
from blog.serializers import BlogSerializer, CategorySerializer
from course.serializers import DepartmentSerializer,  LectureSerializer, CourseSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def search(request):
    data = request.data
    query = data['query']

    # Search for users
    users = User.objects.filter(
        models.Q(username__icontains=query) |
        models.Q(first_name__icontains=query) |
        models.Q(last_name__icontains=query) |
        models.Q(email__icontains=query)
    )
    users_serializer = UserSerializer(users, many=True)

    # Search for blog posts
    posts = Blog.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(content__icontains=query)
    )
    posts_serializer = BlogSerializer(posts, many=True)

    # Search for categories
    categories = Category.objects.filter(title__icontains=query)
    categories_serializer = CategorySerializer(categories, many=True)

    # Search for courses
    courses = Course.objects.filter(
        models.Q(course_name__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(prerequisites__icontains=query)
    )
    courses_serializer = CourseSerializer(courses, many=True)

    # Search for departments
    departments = Department.objects.filter(name__icontains=query)
    departments_serializer = DepartmentSerializer(departments, many=True)

    # Search for lectures
    lectures = Lecture.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(content__icontains=query)
    )
    lectures_serializer = LectureSerializer(lectures, many=True)
    
    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'categories': categories_serializer.data,
        'courses': courses_serializer.data,
        'departments': departments_serializer.data,
        'lectures': lectures_serializer.data,
    }, safe=False)
