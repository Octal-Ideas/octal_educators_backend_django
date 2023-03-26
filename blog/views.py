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
    # Custom permission class that allows read access to anyone, but only allows
    # authenticated users to modify the data
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

# Viewset for the Blog model
class BlogViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):
    # Sets the serializer class and permission class to be used by this viewset
    serializer_class = BlogSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    pagination_class = PostLimitOffsetPagination
     
    def get_queryset(self):
        # Returns all Blog objects and filters based on the category_id query parameter if it exists
        queryset = Blog.objects.select_related('category').all()
        category_id = self.request.query_params.get('category_id')

        if category_id is not None:
            queryset = queryset.filter(
                category_id=category_id)

        return queryset

    def perform_create(self, serializer):
        # When a new Blog object is created, sets the created_by field to the current user
        if serializer.is_valid(raise_exception=True):         
            serializer.validated_data['created_by'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
    @action(detail=True, methods=['get'])
    def tagged(self, request, pk=None):
        # Filters Blog objects by the given tag name
        tag = get_object_or_404(Tag, slug=pk)
        blogs = Blog.objects.filter(tags=tag)
        # Returns a rendered template with the filtered Blog objects
        context = {
            'tag':tag,
            'blogs':blogs,
        }
        return render(request, 'blog/tagged.html', context)

# Viewset for the Category model
class CategoryViewSet(GenericViewSet, ListModelMixin):
    # Sets the queryset, serializer class, and permission class to be used by this viewset
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAuthenticated]

# Viewset for the Comment model
class CommentViewSet(GenericViewSet):
    # Sets the queryset, serializer class, and permission class to be used by this viewset
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    
    def post(self, request, slug, serializer, *args, **kwargs):
        # When a new Comment object is created, sets the created_by and post fields to the current user and the specified Blog object respectively
        post = get_object_or_404(Blog, slug=slug)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user, post=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

# Viewset for the ViewCount model
class ViewCountViewSet(GenericViewSet):
    # Sets the queryset and serializer class to be used by this viewset
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