from rest_framework import serializers
from .models import Subscriber

from accounts.models import User
from notification.views import notification


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'user', 'subscribers', 'content_owner']
        read_only_fields = ['id', 'user', 'subscribers', 'content_owner']

    def create(self, validated_data):
        user = self.context['request'].user
        
        content_owner_id = self.context.get('content_owner_id')

        if content_owner_id:
            content_owner = User.objects.get(id=content_owner_id)
        else:
            raise serializers.ValidationError("Content owner ID is required.")

        if not content_owner.is_authenticated:
            raise serializers.ValidationError("Invalid content owner.")

        if not content_owner.can_receive_subscriptions:
            raise serializers.ValidationError(
                "Content owner cannot receive subscriptions.")

        if content_owner == user:
            raise serializers.ValidationError(
                "You cannot subscribe to your own content.")

        # Check if the subscriber already exists
        subscriber, created = Subscriber.objects.get_or_create(
            user=user, content_owner=content_owner)

        if created:
            # Add the user to the subscribers list of the content owner
            content_owner.subscribers.add(user)
            print(user)
            # Create a notification for the subscription
            notifications = notification(
                self.context['request'], 'subscribe', subscribe_id=content_owner_id
            )

        return subscriber
