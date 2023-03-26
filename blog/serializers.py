from rest_framework import serializers
from .models import Blog, Category, Comment,ViewCount
from taggit.serializers import (TagListSerializerField, TaggitSerializer)



# Serializes the Comment model
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',  'author', 'post')
        read_only_fields =('date_posted','modified_at', 'pub_date')
        
class BlogSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    time_since_published = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    class Meta:
        model = Blog
        fields = ('id', 'title', 'thumbnail', 'description',
                  'slug', 'category', 'tags', 'comments',"language","photographer", "caption","time_since_published",)
        read_only_fields = ('created_by', 'created_at', 'modified_at')
        
    def get_time_since_published(self, obj):
        return obj.whenpublished()
    
    def validate_title(self, value):
        if len(value) > 100:
            return serializers.ValidationError("Max title length is 100 characters")
        return value
    
    def validate_description(self, value):
        if len(value) > 200:
            return serializers.ValidationError(
                "Max description length is 200 characters"
            )
        return value
    
class CategorySerializer(serializers.ModelSerializer):
    blogs = BlogSerializer(many = True)
    class Meta:
        model = Category
        fields = ('id', 'title','blogs')
        
class ViewCountSerializer(serializers.ModelSerializer):
    blog_post = serializers.SlugRelatedField(slug_field='slug', queryset=Blog.objects.all())
    
    class Meta:
        model = ViewCount
        fields = ('id', 'blog_post', 'count')