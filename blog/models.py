from django.contrib.auth.models import User
import math
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
        if Tag.objects.count() > 5:
            raise Exception("Maximum number of tags reached")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

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
    slug = models.SlugField(default='-')
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="blog", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='blogs')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    photographer = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    def clean(self):
        if not self.pk:
            # Make sure the language exists
            lang_codes = [lang[0] for lang in self.LANGUAGES]
            if self.language not in lang_codes:
                raise ValidationError(f"{self.language} is not a valid language code.")
        
        # Make sure the caption is short
        if len(self.caption) > 100:
            raise ValidationError("The caption must be less than 100 characters long.")
        
        
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


models.signals.pre_save.connect(handle_max_tags_reached, sender=Tag)