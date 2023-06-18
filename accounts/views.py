from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import permission_classes, api_view




# from .signals import account_activation_token
from .throttles import AccountsRateThrottle
from .models import User
from .serializers import UserSerializer

from lead.models import Lead



@api_view(['POST'])
@permission_classes([IsAdminUser])
def convert_lead_to_student_view(request):
    # Get the ID of the Lead object from the request data
    lead_id = request.data.get('lead_id')

    try:
        # Convert the Lead object to a Student object
        new_student = convert_lead_to_student(lead_id)

        # Serialize the new Student object and return it as a response
        # serializer = LeadSerializer(new_student)
        message = 'Student successfully created'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Lead.DoesNotExist:
        # Return a 404 error if the Lead object with the given ID does not exist
        return Response(status=status.HTTP_404_NOT_FOUND)


def convert_lead_to_student(lead_id):
    # Get the Lead object with the given ID
    lead = Lead.objects.get(id=lead_id)
    # Create a new Student object with the same data as the Lead object
    student = User.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone_number=lead.phone_number,
        role='student',
    )
    # Generate a random password
    password = User.objects.make_random_password()

    # Set the password for the new student
    student.set_password(password)
    student.save()

    # Delete the Lead object
    lead.delete()

    # Send an email to the student with their temporary password
    # and instructions on how to reset their password upon logging in
    # todo send_password_email(student.email, password)

    print(student.email, password)
    # Return the new Student object
    return student
