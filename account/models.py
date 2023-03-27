from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('blogger', 'Blogger'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='blogger')
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField( unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = f"{self.first_name[0]}{self.last_name}"
            if User.objects.filter(username=base_username).exists():
                base_username = f"{self.first_name[:2]}{self.last_name}"
                i = 1
                while User.objects.filter(username=f"{base_username}{i}").exists():
                    i += 1
                self.username = f"{base_username}{i}"
            else:
                self.username = base_username
        super().save(*args, **kwargs)

