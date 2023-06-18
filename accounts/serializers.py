from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model

from .models import User


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "role", "email", "username", "phone_number", "first_name","password", "last_name"]
        extra_kwargs = {'password': {'write_only': True}}
