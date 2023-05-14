from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Lead
from .serializers import LeadSerializer

from .pagination import LeadLimitOffsetPagination
# Create your views here.


class LeadViewSet(viewsets.ModelViewSet):
     # Sets the queryset, serializer class, and permission class to be used by this viewset
    serializer_class = LeadSerializer
    pagination_class = LeadLimitOffsetPagination
    def get_queryset(self):
        # Returns all Lead objects and filters based on the user if they are not an admin
        user = self.request.user
        if user.is_staff:
            queryset = Lead.objects.all()
        else:
            queryset = Lead.objects.filter(created_by=user)
        return queryset
    
    def get_permissions(self):
        # Returns the list of permissions that this view requires
        if self.action in ['list','update', 'partial_update', 'destroy'] :
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Sets the created_by field on the Lead object to the current user
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
