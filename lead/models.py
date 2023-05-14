from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

CHOICES_PRIORITY = (("low", 'Low'), ("medium", 'Medium'), ("high", 'High'))
CHOICES_STATUS = (("new", 'New'), ("contacted", 'Contacted'),
                  ("inprogress", 'In progress'), ("lost", 'Lost'), ("won", 'Won'))


class Lead(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, default='new')
    priority = models.CharField(
        max_length=20, choices=CHOICES_PRIORITY, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
