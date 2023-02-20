from rest_framework import serializers
from .models import Blog, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


        
class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Blog
        fields = ('id', 'title', 'thumbnail', 'description',
                  'slug', 'category')
        read_only_fields = ('created_by', 'created_at', 'modified_at')