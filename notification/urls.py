from django.urls import path
from .import views

app_name = "notification"

# Define urlpatterns
urlpatterns = [
    path('notify', views.notification, name="notify"),
    path('subscribe', views.subscription, name="subscribe"),
    path('unsubscribe', views.unsubscription, name="unsubscribe"),
    
]