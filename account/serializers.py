from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'username', 'phone_number', 'first_name','password', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     print(validated_data )

    #     password = validated_data.pop('password')
    #     if 'confirm_password' in validated_data:
    #         confirm_password = validated_data.pop('confirm_password')
    #         if password != confirm_password:
    #             raise serializers.ValidationError("Passwords do not match")
        
    #     user = User.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user

    
    # def validate(self, data):
    #     # Custom validation logic
    #     if 'password' in data and 'confirm_password' in data:
    #         if data['password'] != data['confirm_password']:
    #             raise serializers.ValidationError("Passwords do not match")
    #         del data['confirm_password']
    #     return data




