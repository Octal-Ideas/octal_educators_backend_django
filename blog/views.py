from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import BlogSerializer, CategorySerializer, CommentSerializer, ViewCountSerializer
from .models import Blog, Category, Comment, ViewCount
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
# Create your views here.


class BlogViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin
):

    serializer_class = BlogSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
     
    def get_queryset(self):
        queryset = Blog.objects.select_related('category').all()
        category_id = self.request.query_params.get('category_id')

        if category_id is not None:
            queryset = queryset.filter(
                category_id=category_id)

        return queryset
    def perform_create(self, serializer):
        serializer.save(created_by =self.request.user)
    
class CategoryViewSet(GenericViewSet, ListModelMixin,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CommentViewSet(GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


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