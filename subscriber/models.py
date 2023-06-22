import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    # todo gets all users who have subscribed to your account
    
    # ! not working
    # def get_subscriber_users(self):
    #             return User.objects.filter(subscriptions=self.user)

    def get_subscriber_users(self):
        print ("get_subscriber_users")
        # return User.objects.filter(subscriptions__user=self.user)
        # subscriptions = Subscriber.objects.filter(user=self.user)
        # return [sub.subscription for sub in subscriptions]
        # return Subscriber.objects.filter(user=self.user)
        # return Subscriber.objects.filter(subscription__user=self.user)
        subscribed_users = []
        for user in User.objects.all():
            if self.user in user.subscriber.subscription.all():
                subscribed_users.append(user)
        return subscribed_users
    
    @receiver(post_save, sender=User)
    def create_subscriber(sender, instance, created, **kwargs):
        if created:
            Subscriber.objects.create(user=instance)