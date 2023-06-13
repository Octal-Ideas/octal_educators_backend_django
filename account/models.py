import uuid
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField 


class UserManager(BaseUserManager):
    #Method to create a regular user
    def _create_user(self, email, phone_number, username, password, **extra_fields):
        # Check if user email and password is provided
        if not email:
            raise ValueError("Users must have an email")
        if not password:
            raise ValueError("Password must be provided")

        # Normalize user email
       
        email = self.normalize_email(email)
        # Create and save the user
        user = self.model(email=email, username=username,phone_number=phone_number,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_admin',False)
        extra_fields.setdefault('is_subscribed',False)
        return self._create_user( **extra_fields)
    
    # Method to create a superuser
    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_subscribed',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user( **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
     
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('blogger', 'Blogger'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=ROLES, default='blogger')
    avatar = CloudinaryField('image',upload_preset='octalideas', blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "phone_number","last_name","role"]

    def __str__(self):
        return self.email
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    