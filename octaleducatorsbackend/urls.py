"""octaleducatorsbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

admin.site.site_header = "Octal Ideas Admin"
admin.site.site_title = "Octal Ideas Admin Portal"
admin.site.index_title = "Welcome to Octal Ideas Educator"

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
     path('accounts/', include('allauth.urls')),


    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('blog.urls')),
    path('api/v1/', include('theme.urls')),
    path('api/v1/', include('course.urls')),
    path('api/v1/', include('search.urls')),
    path('api/v1/', include('lead.urls')),
    
     path('api/v1/', include('subscriber.urls')),
    



    path('', schema_view),
    path('ckeditor/', include('ckeditor_uploader.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Octal Ideas Admin"
admin.site.site_title = "Octal Ideas Admin Portal"
admin.site.index_title = "Welcome to Octal Ideas Educator"
