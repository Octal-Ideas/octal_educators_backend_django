# Importing the models module from Django's database library.
from django.db import models

# This is where we define our Theme model.
class Theme(models.Model):
    # Defining a name field for the theme model which is a character field and can have maximum length of 50 characters.
    name = models.CharField(max_length=50)
    # Defining a css_class field for the theme model which is a character field and can have maximum length of 50 characters.
    css_class = models.CharField(max_length=50)
