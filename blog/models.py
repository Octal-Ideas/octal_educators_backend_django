from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

    
# Create your models here.

# A model representing a blog post category
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    
# A model representing a blog post tag
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
     # The maximum number of tags allowed is 5
    def save(self, *args, **kwargs):
        if Tag.objects.count() >= 5:
            raise Exception("Maximum number of tags reached")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

# A model representing a blog post
class Blog(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = CloudinaryField('image')
    description = models.TextField()
    slug = models.SlugField(default='-')
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="blog", on_delete= models.CASCADE, default=3)
    created_at= models.DateField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    duration = models.DurationField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='blogs')

    # Returns the time since the blog was published
    @property
    def time_since_published(self):
        if self.published_date is None:
            return None
        return timezone.now() - self.published_date

    # Publishes the blog and calculates the duration since creation
    def publish(self):
        self.published_date = timezone.now()
        self.duration = self.published_date - self.created_at
        self.save()
    def __str__(self) -> str:
        return self.title
    
# A model representing a comment on a blog post
class Comment(models.Model):
    content = models.TextField()
    modified_at = models.DateField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}\'s comment on {self.post}'
    
class ViewCount(models.Model):
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    
        # A method to increment the number of viewers for the post
    def increment_viewers(self):
        self.count += 1
        self.save()

    def __str__(self):
        return f'{self.blog_post.title} - {self.count} viewers'
    
# Error handler for maximum number of tags reached
def handle_max_tags_reached(sender, **kwargs):
    if sender.objects.count() > 5:
        raise Exception("Maximum number of tags reached")

# Error handler for invalid blog post slug
def handle_invalid_slug(sender, instance, **kwargs):
    instance.slug = instance.title.replace(' ', '-')
    instance.save()


# Register error handlers
models.signals.pre_save.connect(handle_invalid_slug, sender=Blog)
models.signals.pre_save.connect(handle_max_tags_reached, sender=Tag)