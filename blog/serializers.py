from rest_framework import serializers
from .models import Blog, Category, Tag, Comment,ViewCount



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')

# Serializes the Tag model
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

# Serializes the Comment model
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',  'author')
        read_only_fields =('date_posted','modified_at', 'pub_date')
        
class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    time_since_published = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ('id', 'title', 'thumbnail', 'description',
                  'slug', 'category', 'tags', 'comments',"language","photographer", "caption","time_since_published",)
        read_only_fields = ('created_by', 'created_at', 'modified_at')
        
    def get_time_since_published(self, obj):
        return obj.whenpublished()
        
class ViewCountSerializer(serializers.ModelSerializer):
    blog_post = serializers.SlugRelatedField(slug_field='slug', queryset=Blog.objects.all())
    
    class Meta:
        model = ViewCount
        fields = ('id', 'blog_post', 'count')