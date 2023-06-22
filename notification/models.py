from uuid import uuid4
from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('blog_like', 'Blog Like'),
        ('blog_comment', 'Blog Comment'),
        ('new_blog', 'New Blog'),
        ('subscribe', 'Subscribe'),
        ('unsubscribe', 'Unsubscribe'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_read = models.BooleanField(default=False)
    body = models.TextField()
    type_of_notification = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        'blog.Blog', on_delete=models.CASCADE, null=True, blank=True)
    created_for = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_of_notification} - {self.created_by} to {self.created_for}"
