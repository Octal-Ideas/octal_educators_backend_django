from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = CloudinaryField('image')
    description = models.TextField()
    slug = models.SlugField(default='-')
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="blog", on_delete= models.CASCADE, default=3)
    created_at= models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='blogs')

    def __str__(self) -> str:
        return self.title