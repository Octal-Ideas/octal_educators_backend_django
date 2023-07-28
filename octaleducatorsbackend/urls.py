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
from django.urls import path, include,  re_path
from django.conf import settings
from django.conf.urls.static import static
from payment.views import Makepayment


# DRF YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "Octal Ideas Admin"
admin.site.site_title = "Octal Ideas Admin Portal"
admin.site.index_title = "Welcome to Octal Ideas Educator"

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.jwt")),
    path("api/v1/", include("djoser.social.urls")),
    
    path('oauth/', include('social_django.urls', namespace='social')),
  
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('blog.urls')),
    path('api/v1/', include('theme.urls')),
    path('api/v1/', include('course.urls')),
    path('api/v1/', include('search.urls')),
    path('api/v1/', include('lead.urls')),
    path('api/v1/', include('notification.urls')),
    path('api/v1/', include('subscriber.urls')),

    path('api/v1/lnm_stkpush/', Makepayment.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Octal Ideas Admin"
admin.site.site_title = "Octal Ideas Admin Portal"
admin.site.index_title = "Welcome to Octal Ideas Educator"
