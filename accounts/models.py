# Import required packages
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# from .signals import send_registration_notification

from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField

# Custom user manager


class UserManager(BaseUserManager):

    # Method to create a regular user
    def create_user(self, email, phone_number, first_name, last_name, username=None, password=None, **extra_fields):
        # Check if user email is provided
        if not email:
            raise ValueError('Users must have an email address')

        # Normalize user email
        email = self.normalize_email(email)

        # Generate username
        if not username or self.model.objects.filter(username=username).exists():
            # If first name and last name is given, create a username
            if first_name and last_name:
                username = f"{first_name[0].upper()}{last_name.lower()}"

                # Check if username already exists
                username_exists = True
                i = 1
                while username_exists:
                    try:
                        self.model.objects.get(username=username)
                    except self.model.DoesNotExist:
                        username_exists = False
                    else:
                        i += 1
                        if i > 999:
                            username = f"{first_name[:2].upper()}{last_name.lower()}{i}"
                        else:
                            username = f"{first_name[0].upper()}{last_name.lower()}{i}"
            # If first name and last name is not given, fall back to email address
            else:
                username = email.split('@')[0]

                # Check if username already exists
                username_exists = True
                i = 1
                while username_exists:
                    try:
                        self.model.objects.get(username=username)
                    except self.model.DoesNotExist:
                        username_exists = False
                    else:
                        i += 1
                        if i > 999:
                            username = f"{username}{i}"
                        else:
                            username = f"{username}{i}"

        # Create and save the user
        user = self.model(email=email, username=username, phone_number=phone_number,
                          first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create a superuser
    def create_superuser(self, email, phone_number, first_name, last_name, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        # extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, phone_number=phone_number, first_name=first_name, last_name=last_name, username=username, **extra_fields)

# User model


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('blogger', 'Blogger'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = CloudinaryField(
        'image', upload_preset='octalideas', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='blogger')
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=200, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(
        'self', symmetrical=False, related_name='my_subscribers')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name",
                       "phone_number", "username", "role", "avatar"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def get_role(self):
        return self.role

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are superusers
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are superusers
        return self.is_admin
    # Connect the signal handler
# post_save.connect(send_registration_notification, sender=User)
