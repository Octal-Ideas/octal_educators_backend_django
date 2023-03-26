# Importing the path module from Django's urls library.
from django.urls import path

# Importing the views module from this directory.
from .import views

# Creating URL patterns for our themes.
urlpatterns = [
    # This is the URL pattern for listing all themes.
    path('themes/', views.ThemeList.as_view(), name='theme-list'),

    # This is the URL pattern for switching between different themes.
    path('themes/switch/', views.ThemeSwitch.as_view(), name='theme-switch'),
]
