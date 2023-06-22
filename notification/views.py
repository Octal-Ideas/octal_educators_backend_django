from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        """
        Retrieve unread notifications for the authenticated user.
        """
        # Get all the unread notifications for the authenticated user
        received_notifications = request.user.notifications.filter(
            is_read=False)

        # Serialize the notifications to convert them into a JSON format
        serializer = NotificationSerializer(received_notifications, many=True)

        # Return the serialized notifications as the API response
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def read_notification(self, request, pk):
        """
        Mark a notification as read.
        """
        # Find the notification with the specified primary key (pk) that belongs to the authenticated user
        notification = Notification.objects.filter(
            created_for=request.user).get(pk=pk)

        # Update the "is_read" field of the notification to mark it as read
        notification.is_read = True
        notification.save()

        # Return a response indicating that the notification has been marked as read
        return Response({'message': 'Notification read'})
