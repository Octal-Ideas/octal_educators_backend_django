from django.contrib import admin

# Register your models here.
from .models import Department,Teacher,Course,Lecture

admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Lecture)