import uuid
from django.db import models
from django.conf import settings
# Create your models here.


    # Define Department model with fields as per requirements
    # id field is UUIDField and is a primary key and is autogenerated
    # name field is a CharField with max length 255
    # modified_at field is DateField with auto_now attribute set to True to update modified_at whenever object is updated
    # created_by field is a ForeignKey to User model with related_name "departments" and on_delete attribute set to CASCADE to delete departments when User object is deleted
    # created_at field is a DateTimeField with auto_now_add attribute set to True to auto populate created_at whenever a new object is created

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="departments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_time = models.CharField(max_length=50)

    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="teachers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    # Define the fields for the Course model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    prerequisites = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # Add a cover image for the Course
    cover = models.ImageField(upload_to='courses/')

    # Define a teacher for the Course
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    # Define the pricing for the Course
    price_all = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    price_per = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    # Define the relationship with Lecture model
    lectures = models.ManyToManyField(Lecture)
    
    # Define the timestamps for the Course model
    modified_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="blogs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Set the default ordering for the Course model
        ordering = ["-created_at"]

    def __str__(self):
        # Return the course name as a string representation of the Course model
        return self.course_name


class Lecture(models.Model):
    # Define the fields for the Lecture model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()

    # Define the relationship with Course model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        # Return the title as a string representation of the Lecture model
        return self.title