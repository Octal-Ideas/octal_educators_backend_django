from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id", "email", "phone_number",
                  "first_name", "last_name", "course", "location","class_type"]
        read_only_fields = ('created_by', 'created_at',
                            'modified_at', 'status', 'priority')
