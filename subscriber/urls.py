from django.urls import path
from .views import (
    SubscriberCreateView,
    SubscriberRetrieveDestroyView,
    SubscriberListView,
    TotalSubscriberView,
)

urlpatterns = [
    path('subscribe/', SubscriberCreateView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', SubscriberRetrieveDestroyView.as_view(), name='unsubscribe'),
    path('subscribers/', SubscriberListView.as_view(), name='subscribers'),
    path('total-subscribers/', TotalSubscriberView.as_view(), name='total_subscribers'),
]
