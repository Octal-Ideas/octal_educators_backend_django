from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import (
    UserCreateView, UserDeleteView, UserDetailView, UserViewSet, 
    UserListCreateAPIView, UserViewSet,
    PasswordResetView, PasswordResetConfirmView,
    SetPasswordView, ActivationView,
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/', UserCreateView.as_view(), name='user_create'),
    path('auth/users/me/', UserViewSet.as_view({'get': 'me'}), name='user_me'),
    path('auth/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('auth/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('auth/users/', UserListCreateAPIView.as_view(), name='user_list_create'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/set/', SetPasswordView.as_view(), name='password_set'),
    path('auth/activate/', ActivationView.as_view(), name='activate'),
]
