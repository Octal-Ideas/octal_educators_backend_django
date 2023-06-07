# Importing the path module from Django's urls library.
from django.urls import path

# Importing the views module from this directory.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
)

# from dj_rest_auth.registration.views import (
#     ResendEmailVerificationView,
#     VerifyEmailView,
# )
from .views import UserList, convert_lead_to_student_view, CustomRegisterView, password_reset_confirm_redirect, email_confirm_redirect

# Creating URL patterns for our themes.
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view(), name='user-list'),
#     path("register/verify-email/", VerifyEmailView.as_view(),
#          name="rest_verify_email"),
#     path("register/resend-email/", ResendEmailVerificationView.as_view(),
#          name="rest_resend_email"),
#     path("account-confirm-email/<str:key>/",
#          email_confirm_redirect, name="account_confirm_email"),
#     path("account-confirm-email/", VerifyEmailView.as_view(),
#          name="account_email_verification_sent"),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('passwordReset/', PasswordResetView.as_view(), name='password_reset'),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path('convert-lead-to-student/', convert_lead_to_student_view,
         name='convert-lead-to-student'),
]
