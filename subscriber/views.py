from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Subscriber
from .serializers import SubscriberSerializer




class SubscriberCreateView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriberSerializer

    # def perform_create(self, serializer):
    #     # Automatically set the user field to the authenticated user
    #     serializer.save(user=self.request.user)
    #     # Add the user to the subscribers list of the content owner
    #     content_owner_id = self.request.data.get('content_owner_id')
    #     if content_owner_id:
    #         content_owner = User.objects.get(pk=content_owner_id)
    #         content_owner.subscriber.subscribers.add(self.request.user)
    #         notification = create_notification(
    #             self.request, 'subscribe', subscribe_id=content_owner_id)


class SubscriberRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to unsubscribe."}, status=status.HTTP_403_FORBIDDEN)


class SubscriberListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Subscriber.objects.all()
        else:
            return Subscriber.objects.filter(content_owner=user)


class TotalSubscriberView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            total_subscribers = Subscriber.objects.count()
            return Response({"total_subscribers": total_subscribers})
        else:
            return Response({"error": "You are not authorized to view the total subscribers."}, status=status.HTTP_403_FORBIDDEN)
