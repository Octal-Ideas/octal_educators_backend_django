import uuid

from django.db import models

from account.models import User
from blog.models import Blog
# Create your models here.


class Notification(models.Model):
    NEWBLOG = 'new_blog'
    SUBSCRIBED = 'subscribed_blog'
    UNSUBSCRIBED = 'unsubscribed_blog'
    BLOG_LIKE = 'blog_like'
    BLOG_COMMENT = 'blog_comment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWBLOG, 'New blog'),
        (SUBSCRIBED, 'subscribed blog'),
        (UNSUBSCRIBED, 'Rejected friendrequest'),
        (BLOG_LIKE, 'Blog like'),
        (BLOG_COMMENT, 'Blog comment')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)