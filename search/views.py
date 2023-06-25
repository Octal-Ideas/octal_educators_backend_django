from django.shortcuts import render

from django.views.generic import ListView
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer

from blog.models import Blog,Category
from blog.serializers import BlogSerializer,CategorySerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def search(request):
    data = request.data
    query = data['query']

    users = User.objects.filter(username__icontains=query)
    users_serializer = UserSerializer(users, many=True)

    posts = Blog.objects.filter(description__icontains=query)
    posts_serializer = BlogSerializer(posts, many=True)
    categories = Category.objects.filter(title__icontains=query)
    categories_serializer = CategorySerializer(categories, many=True)

    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'categories': categories_serializer.data
    }, safe=False)
