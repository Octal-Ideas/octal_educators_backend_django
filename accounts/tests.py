from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            phone_number='+1234567880',
            first_name='John',
            last_name='Doe',
            username='johndoe',
            password='testpassword'
        )

        # Assert that the user was created successfully
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '+1234567880')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.username, 'johndoe')
        self.assertTrue(user.check_password('testpassword'))


def create_test_user(email='test@example.com', password='testpassword', phone_number='+1234547867', first_name='John', last_name='Doe', **kwargs):
    User = get_user_model()
    user = User.objects.create_user(email=email, password=password, phone_number=phone_number,
                                    first_name=first_name, last_name=last_name, **kwargs)
    return user


def create_test_user_sub(email='test1@example.com', password='testpassword', phone_number='+1234587867', first_name='John', last_name='Deoe', **kwargs):
    User = get_user_model()
    user = User.objects.create_user(email=email, password=password, phone_number=phone_number,
                                    first_name=first_name, last_name=last_name, **kwargs)
    return user


class DjoserAuthenticationTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.registration_url = reverse('user-list')
        self.login_url = reverse('jwt-create')

        # Create a user for testing
        self.user_data = {
            "email": "test@example.com",
            "phone_number": "+1234560890",
            "first_name": "John",
            "last_name": "Doe",
            "password": "testpass123",
            "username": "johndoe",
            "role": "student"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_registration(self):
        data = {
            "email": "tes1t@example.com",
            "phone_number": "+254745678903",
            "first_name": "John",
            "last_name": "Doe",
            "password": "testpass123",
            "re_password": "testpass123",
            "username": "johndoe1",
            "role": "student"
        }
        response = self.client.post(self.registration_url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Print the response data for debugging
            # Print the raw response content for debugging
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # Add more tests for other Djoser and social authentication routes

#!not sure how to handle social authentication
# class SocialAuthenticationTest(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.social_auth_url = reverse('provider-auth')

#     def test_social_authentication(self):
#         # Mock the social authentication data for testing
#         social_data = {
#             "provider": "facebook",
#             "access_token": "sample-access-token"
#         }
#         response = self.client.get(self.social_auth_url, social_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("access", response.data)
#         self.assertIn("refresh", response.data)
