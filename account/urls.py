# Importing the path module from Django's urls library.
from django.urls import path

# Importing the views module from this directory.


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserList

# Creating URL patterns for our themes.
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view(), name='user-list'),
]
