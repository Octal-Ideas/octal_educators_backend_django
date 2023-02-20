from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Blog, Category, Tag, Comment, ViewCount
from .serializers import BlogSerializer


class BlogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title="Test Category")
        self.tag1 = Tag.objects.create(name="Test Tag 1")
        self.tag2 = Tag.objects.create(name="Test Tag 2")
        self.blog = Blog.objects.create(
            title="Test Blog",
            thumbnail="test_image.jpg",
            description="This is a test blog.",
            category=self.category
        )
        self.blog.tags.add(self.tag1)
        self.blog.tags.add(self.tag2)
        self.comment = Comment.objects.create(
            content="This is a test comment.",
            post=self.blog
        )

    def test_blog_model(self):
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.category, self.category)
        self.assertIn(self.tag1, self.blog.tags.all())
        self.assertIn(self.tag2, self.blog.tags.all())
        self.assertEqual(self.blog.comments.first(), self.comment)

    def test_blog_list_view(self):
        response = self.client.get(reverse("blog-list"))
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_detail_view(self):
        url = reverse("blog-detail", kwargs={"pk": self.blog.pk})
        response = self.client.get(url)
        serializer = BlogSerializer(self.blog)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blog_create_view(self):
        data = {
            "title": "New Test Blog",
            "thumbnail": "new_test_image.jpg",
            "description": "This is a new test blog.",
            "category": self.category.pk,
            "tags": [self.tag1.pk]
        }
        response = self.client.post(reverse("blog-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)
        self.assertEqual(Blog.objects.last().title, "New Test Blog")
        self.assertEqual(Blog.objects.last().category, self.category)
        self.assertIn(self.tag1, Blog.objects.last().tags.all())