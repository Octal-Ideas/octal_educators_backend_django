from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from accounts.tests import create_test_user,create_test_user_sub
from subscriber.models import Subscriber
# # Create your tests here.
class SubscriberModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='test1@example.com',
            phone_number='+1234567090',
            first_name='John',
            last_name='Doe',
            username='johndoe',
            password='testpassword'
        )

    def test_create_subscriber(self):
        # Retrieve an existing subscriber or create a new one
        subscriber, created = Subscriber.objects.get_or_create(user=self.user)

        if created:
            # Assert that the subscriber was created successfully
            self.assertEqual(subscriber.user, self.user)
        else:
            # Assert that the subscriber already exists
            self.assertEqual(subscriber.user, self.user)

        # Add subscribers to the subscriber
        subscriber.subscription.add(self.user)

        # Assert that the subscriber has subscribers
        self.assertEqual(subscriber.subscription.count(), 1)
        self.assertTrue(subscriber.subscription.filter(pk=self.user.pk).exists())

        # Remove a subscriber
        subscriber.subscription.remove(self.user)

        # Assert that the subscriber no longer has the removed subscriber
        self.assertEqual(subscriber.subscription.count(), 0)
        self.assertFalse(subscriber.subscription.filter(pk=self.user.pk).exists())

        # Delete the subscriber
        subscriber.delete()

        # Assert that the subscriber is deleted
        self.assertFalse(Subscriber.objects.filter(pk=subscriber.pk).exists())
        
class SubscriberViewSetTests(APITestCase):
    def setUp(self):
        self.user = create_test_user()  # Create a test user
        self.subscription_user = create_test_user_sub()  # Create another test user for subscription

    def test_subscribe(self):
        url = reverse('subscriber-subscribe')
        data = {'subscription': str(self.subscription_user.id)}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the subscription was added
        self.assertTrue(self.subscription_user in self.user.subscriber.subscription.all())
        self.assertTrue(self.user in self.subscription_user.subscribers.all())
        
    def test_subscriptions(self):
        url = reverse('subscriber-subscriptions')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check the response data

    def test_subscribers(self):
        url = reverse('subscriber-subscribers')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check the response data

    def test_total_subscribers(self):
        url = reverse('subscriber-total-subscribers')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check the response data