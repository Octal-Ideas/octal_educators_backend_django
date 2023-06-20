import uuid
from django.db import models

from accounts.models import User
# Create your models here.


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='subscriber')
    
    #collects all users you have subscribed to
    subscription = models.ManyToManyField(
        User, related_name='subscriptions', blank=True)

    def __str__(self):
        return self.user.username

    #gets all subscribed users
    def get_subscribed_users(self):
        return self.subscription.all()

    #gets all users who have subscribed to your account
    def get_subscriber_users(self):
        return User.objects.filter(subscriptions__user=self.user)
