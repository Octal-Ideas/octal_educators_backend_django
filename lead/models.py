from django.db import models
from django.conf import settings
import uuid

from phonenumber_field.modelfields import PhoneNumberField
from course.models import Course
# Create your models here.

CHOICES_PRIORITY = (("low", 'Low'), ("medium", 'Medium'), ("high", 'High'))
CHOICES_STATUS = (("new", 'New'), ("contacted", 'Contacted'),
                  ("inprogress", 'In progress'), ("lost", 'Lost'), ("won", 'Won'))


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course')
    phone_number = PhoneNumberField(unique=True)
    
    
    class_type =  models.CharField(max_length=25)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, default='new')
    priority = models.CharField(
        max_length=20, choices=CHOICES_PRIORITY, default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
 

    def __str__(self):
        return self.get_full_name()
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'