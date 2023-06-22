from django.contrib.auth import get_user_model
from .models import User
from django.test import TestCase


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


def create_test_user(email='test@example.com', password='testpassword', phone_number='+1234547867',first_name='John', last_name='Doe', **kwargs):
    User = get_user_model()
    user = User.objects.create_user(email=email, password=password,phone_number=phone_number,first_name=first_name,last_name=last_name, **kwargs)
    return user
def create_test_user_sub(email='test1@example.com', password='testpassword', phone_number='+1234587867',first_name='John', last_name='Deoe', **kwargs):
    User = get_user_model()
    user = User.objects.create_user(email=email, password=password,phone_number=phone_number,first_name=first_name,last_name=last_name, **kwargs)
    return user
