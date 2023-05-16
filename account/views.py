from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action, api_view

from .throttles import AccountsRateThrottle
from .models import User
from .serializers import UserSerializer

from lead.models import Lead
from lead.serializers import LeadSerializer


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


@api_view(['POST'])
def convert_lead_to_student_view(request):
    # Get the ID of the Lead object from the request data
    lead_id = request.data.get('lead_id')

    try:
        # Convert the Lead object to a Student object
        new_student = convert_lead_to_student(lead_id)

        # Serialize the new Student object and return it as a response
        serializer = LeadSerializer(new_student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Lead.DoesNotExist:
        # Return a 404 error if the Lead object with the given ID does not exist
        return Response(status=status.HTTP_404_NOT_FOUND)


def convert_lead_to_student(lead_id):
    # Get the Lead object with the given ID
    lead = Lead.objects.get(id=lead_id)
    password = make_password(User.objects.make_random_password())
    # Create a new Student object with the same data as the Lead object
    student = User.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone_number=lead.phone_number,
        role='student',
        password=password,
    )

    # Delete the Lead object
    lead.delete()

    # Send an email to the student with their temporary password
    # and instructions on how to reset their password upon logging in
    # todo send_password_email(student.email, password)

    # print(student.email, password)
    # Return the new Student object
    return student
