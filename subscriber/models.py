import uuid
from django.db import models

# Create your models here.
from accounts.models import User
# Create your models here.


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)
    content_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.user.username}'
