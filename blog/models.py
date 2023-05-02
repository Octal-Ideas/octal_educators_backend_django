# Import required modules
# from django.contrib.auth.models import User
import uuid
import math

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse

from cloudinary.models import CloudinaryField
from rest_framework.exceptions import ValidationError
# Create your models here.

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Model representing a blog post category
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    

# Model representing a blog post
class Blog(models.Model):
    # Language choices for the blog post
    LANGUAGES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
    ]
    
    # Fields for the blog post model  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False)
    thumbnail = CloudinaryField('image',upload_preset='octalideas')
    description = models.TextField()
    slug = models.SlugField()
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="blogs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='blogs')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    photographer = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-modified_at"]
    
    # Get the URL for the blog post API
    def get_api_url(self):
        try:
            return reverse("blogs_api:blog_detail", kwargs={"slug": self.slug})
        except:
            None
    
    # Clean data before saving
    def clean(self):
        # Check that the language code is valid
        if not self.pk:
            lang_codes = [lang[0] for lang in self.LANGUAGES]
            if self.language not in lang_codes:
                raise ValidationError(f"{self.language} is not a valid language code.")
        
        # Check that the caption is less than 100 characters long
        if len(self.caption) > 100:
            raise ValidationError("The caption must be less than 100 characters long.")
        
    # Generate a slug for the blog post before saving
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Blog, self).save(*args, **kwargs)

    # Returns the time since the blog was published
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return "Just now"
            
            else:
                return "Just now"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(post=instance)
        return qs
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Blog)


# A model representing a comment on a blog post
# Defining a Comment model
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Field for storing the content of the comment
    content = models.TextField()
    # Field for storing the last modified date
    modified_at = models.DateField(auto_now=True)
    # Field for storing the date when the comment was posted
    date_posted = models.DateTimeField(default=timezone.now)
    # Field for creating a foreign key relationship with the Blog model
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Field for creating a foreign key relationship with the User model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        # Returns the string representation of the comment object
        return f'{self.author}\'s comment on {self.post}'

    # Class for defining the ordering of comments
    class Meta:
        ordering = ["-date_posted", "-modified_at"]

# Defining a ViewCount model
class ViewCount(models.Model):
    # Field for creating a foreign key relationship with the Blog model
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Field for storing the number of viewers
    count = models.PositiveIntegerField(default=0)
    # Field for creating a foreign key relationship with the User model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='views')
    
    # A method to increment the number of viewers for the post
    def increment_viewers(self):
        self.count += 1
        self.save()

    def __str__(self):
        # Returns the string representation of the ViewCount object
        return f'{self.blog_post.title} - {self.count} viewers'
    

    
# Function to create a slug for a Blog post
def create_slug(instance, new_slug=None):
    # Generate a slug based on the title of the blog post
    slug = slugify(instance.title)
    # If a new slug is provided, use that instead
    if new_slug is not None:
        slug = new_slug
    # Check if a Blog object with the same slug already exists
    qs = Blog.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    # If a Blog object with the same slug already exists, add a unique identifier to the slug
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        # Recursively call the function with the new slug until a unique slug is found
        return create_slug(instance, new_slug=new_slug)
    # If a unique slug is found, return it
    return slug

