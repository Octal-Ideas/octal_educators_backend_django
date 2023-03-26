from django.contrib import admin

# Register your models here.
from .models import Blog,Category, Comment,ViewCount

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ViewCount)