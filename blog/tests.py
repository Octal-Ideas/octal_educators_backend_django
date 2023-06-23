from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import Blog, ViewCount, Comment, Like, Category
from .views import BlogViewSet, CategoryViewSet, CommentViewSet, ViewCountViewSet, post_like
from accounts.models import User
from notification.models import Notification


class BlogViewSetTestCase(TestCase):
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
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)

    def test_blog_create(self):
        url = reverse('blogs-list')
        data = {'title': 'New Blog', 'content': 'New Content'}
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Blog.objects.count(), 2)
        self.assertEqual(Blog.objects.last().title, 'New Blog')


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = CategoryViewSet.as_view({'get': 'list'})

    def test_category_list(self):
        url = reverse('categories-list')
        request = self.factory.get(url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)


class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', phone_number='+1234967890', first_name='John', last_name='Doe')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category, created_by_id=self.user.id, slug='test-blog')
        self.viewset = CommentViewSet.as_view(
            {'get': 'list', 'post': 'create'})

    def test_comment_list(self):
        url = reverse('comments-list')
        request = self.factory.get(url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)

    def test_comment_create(self):
        url = reverse('comments-list')
        data = {'content': 'New Comment', 'post': self.blog.id}
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.last().content, 'New Comment')


class ViewCountViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category)
        self.viewset = ViewCountViewSet.as_view({'post': 'increment_viewers'})


class PostLikeViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', phone_number='+1234967990', first_name='John', last_name='Doe')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog', content='Test Content', category=self.category, created_by_id=self.user.id, slug='test-blog')
        self.url = reverse('post_like', kwargs={'pk': self.blog.id})

    def test_post_like(self):
        url = reverse('post_like', kwargs={'pk': self.blog.pk})
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'like created'})
        self.assertEqual(self.blog.likes_count, 1)
        self.assertEqual(self.blog.likes.first().created_by, self.user)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.notification_type, 'post_like')
        self.assertEqual(notification.post_id, self.blog.id)
        self.assertEqual(notification.recipient, self.blog.created_by)

    def test_post_like_already_liked(self):
        like = Like.objects.create(created_by=self.user)
        self.blog.likes.add(like)

        request = self.factory.post(self.url)
        force_authenticate(request, user=self.user)
        response = post_like(request, pk=self.blog.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.blog.likes_count, 1)
