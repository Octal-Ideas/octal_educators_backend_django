from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'username', 'phone_number', 'first_name','password', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}



