from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle 

from .throttles import AccountsRateThrottle
from .models import User
from .serializers import UserSerializer




# Creating a view for the UserList
class UserList(APIView):
    # Specifying permission classes
    permission_classes = [IsAdminUser | AllowAny]
    throttle_classes = [UserRateThrottle, AccountsRateThrottle]

    def get(self, request):
        # Checking if the user is an admin
        if not request.user.is_staff:
            # Returning an error message if not authorized
            return Response({'error': 'Only admins can view users.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieving all users from the database
        queryset = User.objects.all()
        # Serializing the retrieved data
        serializer = UserSerializer(queryset, many=True)
        # Returning the serialized data as response
        return Response(serializer.data, status=status.HTTP_200_OK)

# Customizing the token serializer to add custom claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    throttle_classes = [UserRateThrottle, AccountsRateThrottle]
    
    @classmethod
    def get_token(cls, user):
        # Generating token using the parent class method
        token = super().get_token(user)

        # Adding custom claims
        token["email"] = user.email,
        token['username'] = user.username
        # ...

        # Returning the updated token
        return token

# Customizing the token view to use the custom serializer
class MyTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [UserRateThrottle, AccountsRateThrottle]
    serializer_class = MyTokenObtainPairSerializer
    