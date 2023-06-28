from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User

from course.models import Department, Course, Teacher
from .models import Lead

# Create your tests here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Lead
from .serializers import LeadSerializer

from .pagination import LeadLimitOffsetPagination


class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    pagination_class = LeadLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Lead.objects.all()
        else:
            queryset = Lead.objects.filter(created_by=user)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Lead successfully created"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LeadModelTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpassword', phone_number='+1234597890', first_name='John', last_name='Doe', role='teacher'
        )
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)

        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
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

        self.lead = Lead.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            course=self.course,
            phone_number='+1234567890',
            class_type='Type A',
            location='Location A',
            status='new',
            priority='low',
            created_by=self.user,
        )

    def test_lead_creation(self):
        lead_count = Lead.objects.count()
        self.assertEqual(lead_count, 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.first_name, 'John')
        self.assertEqual(lead.last_name, 'Doe')
        self.assertEqual(lead.email, 'john.doe@example.com')
        self.assertEqual(lead.course, self.course)
        self.assertEqual(lead.phone_number, '+1234567890')
        self.assertEqual(lead.class_type, 'Type A')
        self.assertEqual(lead.location, 'Location A')
        self.assertEqual(lead.status, 'new')
        self.assertEqual(lead.priority, 'low')
        self.assertEqual(lead.created_by, self.user)

    def test_lead_string_representation(self):
        lead_str = str(self.lead)
        expected_str = 'John Doe'
        self.assertEqual(lead_str, expected_str)


class LeadViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpassword', phone_number='+1234597890', first_name='John', last_name='Doe', role='teacher'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com', username='admin', password='adminpassword', phone_number='+1234597880', first_name='John', last_name='Doe', role='admin'
        )
        self.department = Department.objects.create(
            name='Test Department', created_by=self.user)

        self.teacher = Teacher.objects.create(
            user=self.user,
            gender='Male',
            date_of_birth='2000-01-01',
            address='Test Address',
            department=self.department,
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
        self.lead = Lead.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            course=self.course,
            phone_number='+1234567890',
            class_type='Type A',
            location='Location A',
            status='new',
            priority='low',
            created_by=self.user,
        )

    def test_lead_list(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('leads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(Lead.objects.all())
        self.assertEqual(Lead.objects.count(), 1)

    def test_lead_retrieve(self):
        url = reverse('leads-detail', args=[self.lead.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_lead_create(self):
        url = reverse('leads-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'course': str(self.course.id),
            'phone_number': '+254765789012',
            'class_type': 'Type B',
            'location': 'Location B',
            'status': 'new',
            'priority': 'high',
            'created_by': str(self.user.id),
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Print the response data for debugging
            # Print the raw response content for debugging
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 2)

    def test_lead_update(self):
        url = reverse('leads-detail', args=[self.lead.id])
        # data = {'lead': str(self.user.id)}
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'course': str(self.course.id),
            'phone_number': '+254756774012',
            'class_type': 'Type B',
            'location': 'Location B',
            'status': 'contacted',
            'priority': 'high',
            'created_by': str(self.user.id),
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, data)
        if response.status_code != status.HTTP_200_OK:
            print(response.data)  # Print the response data for debugging
            # Print the raw response content for debugging
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['class_type'], 'Type B')
        self.assertEqual(response.data['location'], 'Location B')

    def test_lead_delete(self):
        url = reverse('leads-detail', args=[self.lead.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lead.objects.count(), 0)
