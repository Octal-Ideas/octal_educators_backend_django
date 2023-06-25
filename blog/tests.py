from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Blog, ViewCount, Comment, Like, Category
from .views import BlogViewSet, CategoryViewSet, CommentViewSet, ViewCountViewSet, post_like
from accounts.models import User
from notification.models import Notification


class BlogViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', phone_number='+1234967880', first_name='John', last_name='Doe')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category, created_by_id=self.user.id, slug='test-blog')
        self.viewset = BlogViewSet.as_view({'get': 'list'})

    def test_blog_list(self):
        url = reverse('blogs-list')
        request = self.factory.get(url)
        self.client.force_authenticate(user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_create(self):
        url = reverse('blogs-list')
        self.category = Category.objects.create(title='Test Category 2')
        data = {'title': 'New Blog', 'content': 'New Content', 'category': str(
            self.category.id), 'created_by_id': str(self.user.id), 'slug': 'test-blog2'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        # self.client.force_authenticate(user=self.user)
        # response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)
        self.assertEqual(Blog.objects.first().title, 'New Blog')


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = CategoryViewSet.as_view({'get': 'list'})

    def test_category_list(self):
        url = reverse('categories-list')
        request = self.factory.get(url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test2@example.com', password='testpassword', phone_number='+1234907090', first_name='John', last_name='Doe')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category, created_by_id=self.user.id, slug='test-blog2')
        self.viewset = CommentViewSet.as_view(
            {'get': 'list', 'post': 'create'})

    def test_comment_list(self):
        url = reverse('comments-list')
        request = self.factory.get(url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create(self):
        url = reverse('comments-list')
        data = {'content': 'New Comment',
                'post': self.blog.id, 'author': self.user.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.last().content, 'New Comment')


class ViewCountViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category)
        self.viewset = ViewCountViewSet.as_view({'post': 'increment_viewers'})


class PostLikeViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', phone_number='+1234967990', first_name='John', last_name='Doe')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category, created_by_id=self.user.id, slug='test-blog')
        self.url = reverse('post_like', kwargs={'pk': self.blog.pk})

    def test_post_like(self):
        url = reverse('post_like', kwargs={'pk': self.blog.pk})
        data = {'pk': str(self.blog.pk)}
        # request = self.factory.post(url)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'like created'})
        self.blog.refresh_from_db()

        self.assertEqual(self.blog.likes_count, 1)

        self.assertEqual(self.blog.likes.first().created_by, self.user)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.type_of_notification, 'blog_like')
        self.assertEqual(notification.blog, self.blog)
        self.assertEqual(notification.created_for, self.blog.created_by)

    def test_post_like_already_liked(self):
        like = Like.objects.create(created_by=self.user)
        self.client.force_authenticate(user=self.user)
        self.blog.likes.add(like)
        print("post.likes_count " + str(self.blog.likes_count))
        data = {'pk': str(self.blog.pk)}

        response = self.client.post(self.url, data)
        print("post.likes_count " + str(self.blog.likes_count))
        self.assertEqual(response.json(), {'message': 'post already liked'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        print("post.likes_count " + str(self.blog.likes_count))
        self.assertEqual(self.blog.likes.count(), 1)
