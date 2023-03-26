from django.db import models


# Create your models here.

class Theme(models.Model):
    name = models.CharField(max_length=50)
    css_class = models.CharField(max_length=50)
