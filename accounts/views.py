from django.shortcuts import render

# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.http import HttpResponse
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.is_active = False
#             user.save()
#             # to get the domain of the current site
#             current_site = get_current_site(request)
#             mail_subject = 'Activation link has been sent to your email'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = serializer.validated_data['email']
#             email = EmailMessage(
#                 mail_subject,
#                 message,
#                 to=[to_email]
#             )
#             email.send()
#             return Response('Please confirm your email address to complete the registration')
#     else:
#         serializer = UserSerializer()
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
