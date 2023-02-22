import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octaleducatorsbackend.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Blog, Category, Comment, Tag, ViewCount
# from django.urls import reverse



class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), "Test Category")


class TagTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")
        self.tag3 = Tag.objects.create(name="tag3")
        self.tag4 = Tag.objects.create(name="tag4")
        self.tag5 = Tag.objects.create(name="tag5")

    def test_tag_string_representation(self):
        self.assertEqual(str(self.tag1), "tag1")

    def test_max_tags_limit(self):
        with self.assertRaises(Exception):
            tag6 = Tag.objects.create(name="tag6")


class BlogTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.category = Category.objects.create(title='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog Post',
            description='Test description',
            category=self.category,
            created_by=self.user
        )

    def test_blog_created(self):
        self.assertEqual(str(self.blog), 'Test Blog Post')

    def test_blog_published_date(self):
        self.assertIsNone(self.blog.published_date)

    def test_blog_publish(self):
        self.blog.published_date = None
        self.blog.publish()
        self.assertIsNotNone(self.blog.published_date)

    def test_blog_time_since_published(self):
        self.blog.published_date = timezone.now()
        self.blog.save()
        self.assertEqual(self.blog.time_since_published.days, 0)

    def test_category_created(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_tag_created(self):
        tag = Tag.objects.create(name='Test Tag')
        self.assertEqual(str(tag), 'Test Tag')

    def test_tag_max_count(self):
        with self.assertRaises(Exception):
            for i in range(10):
                Tag.objects.create(name=f'Test Tag {i}')

    def test_blog_tags(self):
        tag = Tag.objects.create(name='Test Tag')
        self.blog.tags.add(tag)
        self.assertEqual(self.blog.tags.count(), 1)

    # def test_blog_list_view(self):
    #     url = reverse('blog:blog-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    # def test_blog_detail_view(self):
    #     url = reverse('blog:blog-detail', args=[self.blog.pk])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(title="Test Category")
        self.blog = Blog.objects.create(
            title="Test Blog",
            description="Test Blog Description",
            category=self.category,
            created_by=self.user,
        )
        self.comment = Comment.objects.create(
            content="Test comment content",
            post=self.blog,
            author=self.user,
        )

    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), f"{self.user}'s comment on {self.blog}")


class ViewCountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(title="Test Category")
        self.blog = Blog.objects.create(
            title="Test Blog",
            description="Test Blog Description",
            category=self.category,
            created_by=self.user,
        )
        self.view_count = ViewCount.objects.create(blog_post=self.blog, count=0)

    def test_view_count_string_representation(self):
        self.assertEqual(str(self.view_count), f"{self.blog.title} - {self.view_count.count} viewers")

    def test_increment_viewers(self):
        self.view_count.increment_viewers()
        self.assertEqual(self.view_count.count, 1)