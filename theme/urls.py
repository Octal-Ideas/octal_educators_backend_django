from django.urls import path
# from theme.views import ThemeList, ThemeSwitch
from .import views


urlpatterns = [
    path('themes/', views.ThemeList.as_view(), name='theme-list'),
    path('themes/switch/', views.ThemeSwitch.as_view(), name='theme-switch'),
]
