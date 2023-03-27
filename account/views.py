from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsAdmin, IsTeacher, IsParent, IsStudent, IsBlogger




class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | (IsAuthenticated & (IsTeacher | IsParent | IsStudent))]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


# class BlogList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated, IsBlogger]
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer

# class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsBlogger]
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer