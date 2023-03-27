# Importing render function from Django's shortcut module.
from django.shortcuts import render

# Importing generics and status from rest_framework library
from rest_framework import generics, status

# Importing Response and APIView from rest_framework.views library
from rest_framework.response import Response
from rest_framework.views import APIView

# Importing our theme model and its serializer to define views.
from .models import Theme
from .serializers import ThemeSerializer

# This is where we define our views.
class ThemeList(generics.ListAPIView):
    # queryset to get all the themes.
    queryset = Theme.objects.all()
    # The serializer class to serialize our data and return JSON response.
    serializer_class = ThemeSerializer
    
    
class ThemeSwitch(APIView):
    # This is the POST method which changes the theme for a user.
    def post(self, request, format=None):
        # Getting the theme_id from the request data.
        theme_id = request.data.get('theme_id')
        try:
            # Retrieving the theme object with corresponding id.
            theme = Theme.objects.get(id=theme_id)
            # Changing the user's theme to the selected one.
            request.user.theme = theme
            request.user.save()
            # Return success if everything worked as expected.
            return Response({'success': True})
        except Theme.DoesNotExist:
            # If theme is not found for a given id then return an error message with 404 status code.
            return Response({'success': False, 'message': 'Theme not found.'}, status=status.HTTP_404_NOT_FOUND)
