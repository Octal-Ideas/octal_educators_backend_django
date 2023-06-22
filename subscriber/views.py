from .models import Subscriber
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SubscriberSerializer

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.permissions import ReadOnlyOrAuthenticated
from notification.utils import create_notification


class SubscriberViewSet(viewsets.ViewSet):
    serializer_class = SubscriberSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

    # Action for subscribing to a user's content
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        user = request.user
        subscription_id = request.data.get('subscription')

        # Check if the subscription ID exists
        try:
            subscription_user = User.objects.get(id=subscription_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid subscription ID'}, status=400)

        if user == subscription_user:
            return Response({'message': 'Cannot subscribe to your own user account'}, status=400)

        subscriber, created = Subscriber.objects.get_or_create(user=user)

        if subscription_user in subscriber.subscription.all():
            # Already subscribed, so unsubscribe
            subscriber.subscription.remove(subscription_user)
            subscription_user.subscribers.remove(user)
            notification = create_notification(
                request=request, type_of_notification='unsubscribe', subscribe_id=subscription_user)
            return Response({'message': 'Unsubscribed successfully'}, status=200)
        else:
            # Subscribe
            subscriber.subscription.add(subscription_user)
            subscription_user.subscribers.add(user)
            serializer = self.serializer_class(subscriber)
            notification = create_notification(
                request=request, type_of_notification='subscribe', subscribe_id=subscription_user)
            return Response(serializer.data, status=200)

    # Action for getting the users to whom the logged-in user has subscribed
    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        # try:
        subscriber = request.user.subscriber
        subscribed_users = subscriber.get_subscribed_users()
        serializer = self.serializer_class(subscribed_users, many=True)
        return Response(serializer.data, status=200)
        # except:
        # return Response({'message': 'you have not subscribed to any content'}, status=400)

    # Action for getting the users who have subscribed to the logged-in user's content
    # !not working
    @action(detail=False, methods=['get'])
    def subscribers(self, request):
        user = request.user
        subscribed_users = user.subscribers.all()  # Updated code
        serializer = self.serializer_class(subscribed_users, many=True)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['get'])
    def total_subscribers(self, request):
        user = request.user
        total_subscribers = user.subscribers.count()  # Updated code
        return Response({'total_subscribers': total_subscribers}, status=200)
