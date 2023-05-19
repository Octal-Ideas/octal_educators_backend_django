# Importing the path module from Django's urls library.
from django.urls import path

# Importing the views module from this directory.


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserList, convert_lead_to_student_view, activate,signup

# Creating URL patterns for our themes.
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view(), name='user-list'),
    #  path('signup/', signup, name='signup'),
    # path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    
    path('convert-lead-to-student/', convert_lead_to_student_view, name='convert-lead-to-student'),
]
