from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Course, Department, Teacher, Lecture
from .views import CourseViewSet
from accounts.models import User

# Create your tests here.


class DepartmentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com',
                                             username='testuser', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)

    def test_department_name(self):
        self.assertEqual(str(self.department), 'Test Department')


class TeacherModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com',
                                             username='testuser', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)
        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
            total_time='10 hours',
            created_by=self.user
        )

    def test_teacher_username(self):
        self.assertEqual(str(self.teacher), 'testuser')


class CourseModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com',
                                             username='testuser', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)
        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
            total_time='10 hours',
            created_by=self.user
        )
        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Description',
            prerequisites='Test Prerequisites',
            department=self.department,
            teacher=self.teacher,
            price_all=100.00,
            price_per=10.00,
            created_by=self.user
        )

    def test_course_name(self):
        self.assertEqual(str(self.course), 'Test Course')


class LectureModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com',
                                             username='testuser', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)
        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
            total_time='10 hours',
            created_by=self.user
        )
        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Description',
            prerequisites='Test Prerequisites',
            department=self.department,
            teacher=self.teacher,
            price_all=100.00,
            price_per=10.00,
            created_by=self.user
        )
        self.lecture = Lecture.objects.create(
            title='Test Lecture',
            description='Test Description',
            video_url='http://example.com',
            content='Test Content',
            course=self.course,
            created_by=self.user
        )

    def test_lecture_title(self):
        self.assertEqual(str(self.lecture), 'Test Lecture')


class CourseViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email='test@example.com',
                                             username='testuser', password='testpassword', phone_number='+1234597890', first_name='John', last_name='Doe', role='teacher')
        self.admin = User.objects.create_user(email='test1@example.com',
                                              username='admin', password='testpassword', phone_number='+1234768890', first_name='John', last_name='Doe', role='admin')
        self.department = Department.objects.create(
            name='Test Department', created_by=self.admin)
        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
            total_time='10 hours',
            created_by=self.user
        )
        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Description',
            prerequisites='Test Prerequisites',
            department=self.department,
            teacher=self.teacher,
            price_all=100.00,
            price_per=10.00,
            created_by=self.user
        )

        self.lecture = Lecture.objects.create(
            title='Test Lecture',
            description='Test Description',
            video_url='http://example.com',
            content='Test Content',
            course=self.course,
            created_by=self.user
        )
        self.viewset = CourseViewSet.as_view(
            {'get': 'list', 'post': 'create'})

    def test_setup_creates_items(self):

        # Assert that the items are created successfully
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Lecture.objects.count(), 1)

        # Retrieve the created objects from the database
        user = User.objects.get(email='test@example.com')
        admin = User.objects.get(email='test1@example.com')
        department = Department.objects.get(name='Test Department')
        teacher = Teacher.objects.get(user=user)
        course = Course.objects.get(course_name='Test Course')
        lecture = Lecture.objects.get(title='Test Lecture')

        # Assert the attributes of the created objects
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(admin.username, 'admin')
        self.assertEqual(department.name,
                         'Test Department')
        self.assertEqual(teacher.gender, 'Male')
        self.assertEqual(course.description, 'Test Description')
        self.assertEqual(lecture.video_url, 'http://example.com')

    def test_course_list(self):
        url = reverse('courses-list')
        request = self.factory.get(url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)
