from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import BlogSerializer, CategorySerializer, CommentSerializer, ViewCountSerializer
from .models import Blog, Category, Comment, ViewCount
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import render, redirect, get_object_or_404
from .pagination import PostLimitOffsetPagination
from taggit.models import Tag

class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
# Create your views here.


class BlogViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):

    serializer_class = BlogSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    pagination_class = PostLimitOffsetPagination
     
    def get_queryset(self):
        queryset = Blog.objects.select_related('category').all()
        category_id = self.request.query_params.get('category_id')

        if category_id is not None:
            queryset = queryset.filter(
                category_id=category_id)

        return queryset
    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):         
            # Set the blog created_by field to the current user
            serializer.validated_data['created_by'] = self.request.user
            # Create the blog object
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
    def tagged(request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        # Filter posts by tag name  
        blogs = Blog.objects.filter(tags=tag)
        context = {
            'tag':tag,
            'blogs':blogs,
        }
        return render(request, context)
    
class CategoryViewSet(GenericViewSet, ListModelMixin,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    
class CommentViewSet(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    
    def post(self, request, slug, serializer, *args, **kwargs):
        post = get_object_or_404(Blog, slug=slug)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

class ViewCountViewSet(GenericViewSet):
    queryset = ViewCount.objects.all()
    serializer_class = ViewCountSerializer

    def get_object(self):
        blog_post_id = self.kwargs['blog_post_id']
        obj, _ = ViewCount.objects.get_or_create(blog_post_id=blog_post_id)
        return obj

    @action(detail=True, methods=['post'],name='increment_viewers')
    def increment_viewers(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_viewers()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)