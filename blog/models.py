from django.contrib.auth.models import User
import math
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from rest_framework.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from taggit.managers import TaggableManager

# Create your models here.


# A model representing a blog post category
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    

# A model representing a blog post
class Blog(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
    ]
    title = models.CharField(max_length=255, blank= False,)
    thumbnail = CloudinaryField('image',upload_preset='octalideas')
    description = models.TextField()
    slug = models.SlugField()
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="blog", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='blogs')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    photographer = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-modified_at"]

    def get_api_url(self):
        try:
            return reverse("blogs_api:blog_detail", kwargs={"slug": self.slug})
        except:
            None

    def clean(self):
        if not self.pk:
            # Make sure the language exists
            lang_codes = [lang[0] for lang in self.LANGUAGES]
            if self.language not in lang_codes:
                raise ValidationError(f"{self.language} is not a valid language code.")
        
        # Make sure the caption is short
        if len(self.caption) > 100:
            raise ValidationError("The caption must be less than 100 characters long.")
        
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
class Comment(models.Model):
    content = models.TextField()
    modified_at = models.DateField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}\'s comment on {self.post}'
    class Meta:
        ordering = ["-date_posted", "-modified_at"]
        
class ViewCount(models.Model):
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    
        # A method to increment the number of viewers for the post
    def increment_viewers(self):
        self.count += 1
        self.save()

    def __str__(self):
        return f'{self.blog_post.title} - {self.count} viewers'
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
