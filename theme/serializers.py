# import the Django Rest Framework serializer module and the Theme model
from rest_framework import serializers
from .models import Theme

# Define a serializer class called ThemeSerializer that inherits from serializers.ModelSerializer
class ThemeSerializer(serializers.ModelSerializer):
    
    # Define an inner class that specifies the metadata for the serializer
    class Meta:
        # specify the model that the serializer should use, which is the Theme model
        model = Theme
        # specify the fields that should be included in the serialized output
        # in this case, the serializer will include the id, name, and css_class fields of the Theme model
        fields = ('id', 'name', 'css_class')
