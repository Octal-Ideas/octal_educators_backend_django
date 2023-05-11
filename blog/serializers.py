from rest_framework import serializers
from .models import Blog, Category, Comment, ViewCount

# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',  'author', 'post')
        read_only_fields =('date_posted','modified_at', 'pub_date')

# Serializer for the Blog model
class BlogSerializer( serializers.ModelSerializer):
    # Serializes the comments for the Blog
    comments = CommentSerializer(many=True, read_only=True)
    # Serializer method to get the time since the blog was published
    time_since_published = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        # Fields to serialize
        fields = "__all__"
        # Fields that are read-only
        read_only_fields = ('created_by', 'created_at', 'modified_at')
        
    def get_time_since_published(self, obj):
        # Call the whenpublished() method to get the time since published
        return obj.whenpublished()
    
    def validate_title(self, value):
        # Validate the length of the title
        if len(value) > 100:
            return serializers.ValidationError("Max title length is 100 characters")
        return value
    
    def validate_description(self, value):
        # Validate the length of the description
        if len(value) > 200:
            return serializers.ValidationError(
                "Max description length is 200 characters"
            )
        return value

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    # Serializes the blogs for the Category
    blogs = BlogSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'title', 'blogs')

# Serializer for the ViewCount model
class ViewCountSerializer(serializers.ModelSerializer):
    # Serializer to get the blog post slug
    blog_post = serializers.SlugRelatedField(slug_field='slug', queryset=Blog.objects.all())
    
    class Meta:
        model = ViewCount
        fields = ('id', 'blog_post', 'count')
