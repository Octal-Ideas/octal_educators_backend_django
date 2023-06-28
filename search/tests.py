from django.test import TestCase

from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from blog.models import Blog, Category
from course.models import Course, Department, Teacher, Lecture
from .views import search

# Create your tests here.


class SearchViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe', role="teacher")
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', description="test", category=self.category, created_by=self.user, slug='test-blog')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)
        self.teacher = Teacher.objects.create(
            user=self.user, department=self.department, date_of_birth='2000-01-04', created_by=self.user)
        self.course = Course.objects.create(
            course_name='Test Course', description='Test Description', prerequisites='Test Prerequisites', department=self.department, created_by=self.user, teacher=self.teacher)
        self.lecture = Lecture.objects.create(
            title='Test Lecture', description='Test Description', video_url='http://example.com', content='Test Content', course=self.course, created_by=self.user)

    def test_search_view(self):
        url = reverse('search')
        request_data = {'query': 'test'}
        response = self.client.post(url, data=request_data)
        # response = search(request)
        if response.status_code != status.HTTP_200_OK:
            print(response.data)  # Print the response data for debugging
            # Print the raw response content for debugging
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Assert users
        self.assertIn('users', data)
        users = data['users']
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user['username'], self.user.username)

        # Assert posts
        self.assertIn('posts', data)
        posts = data['posts']
        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post['title'], self.blog.title)

        # Assert categories
        self.assertIn('categories', data)
        categories = data['categories']
        self.assertEqual(len(categories), 1)
        category = categories[0]
        self.assertEqual(category['title'], self.category.title)

        # Assert courses
        self.assertIn('courses', data)
        courses = data['courses']
        self.assertEqual(len(courses), 1)
        course = courses[0]
        self.assertEqual(course['course_name'], self.course.course_name)

        # Assert departments
        self.assertIn('departments', data)
        departments = data['departments']
        self.assertEqual(len(departments), 1)
        department = departments[0]
        self.assertEqual(department['name'], self.department.name)

        # Assert lectures
        self.assertIn('lectures', data)
        lectures = data['lectures']
        self.assertEqual(len(lectures), 1)
        lecture = lectures[0]
        self.assertEqual(lecture['title'], self.lecture.title)
