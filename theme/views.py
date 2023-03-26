from django.shortcuts import render

from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Theme
from .serializers import ThemeSerializer
# Create your views here.

class ThemeList(generics.ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    
    
class ThemeSwitch(APIView):
    def post(self, request, format=None):
        theme_id = request.data.get('theme_id')
        try:
            theme = Theme.objects.get(id=theme_id)
            request.user.theme = theme
            request.user.save()
            return Response({'success': True})
        except Theme.DoesNotExist:
            return Response({'success': False, 'message': 'Theme not found.'}, status=status.HTTP_404_NOT_FOUND)