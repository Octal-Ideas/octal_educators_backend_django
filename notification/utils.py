from blog.models import Blog
from subscriber.models import Subscriber
from .models import Notification

from .models import Notification

from blog.models import Blog
from subscriber.models import Subscriber


def create_notification(request, type_of_notification, blog_id=None, subscribe_id=None):
    created_for = None
    is_read = False  # Set the initial value of is_read to False

    if type_of_notification == 'blog_like':
        body = f'{request.user.username} liked one of your blogs!'
        blog = Blog.objects.get(pk=blog_id)
        created_for = blog.created_by
    elif type_of_notification == 'blog_comment':
        body = f'{request.user.username} commented on one of your blogs!'
        blog = Blog.objects.get(pk=blog_id)
        created_for = blog.created_by
    elif type_of_notification == 'new_blog':
        blog = Blog.objects.get(pk=blog_id)
        created_for = Subscriber.objects.filter(user=request.user).values_list('user', flat=True)
        body = f'{request.user.username} added a blog!'
    elif type_of_notification == 'subscribe':
        # subscribe = Subscriber.objects.get(pk=subscribe_id)
        print("subscribed to subscriber")
        created_for = subscribe_id
        body = f'{subscribe_id.username} subscribed to your channel!'
    elif type_of_notification == 'unsubscribe':
        # unsubscribe = Subscriber.objects.get(pk=subscribe_id)
        print("unsubscribed to subscriber")
        created_for = subscribe_id
        body = f'{subscribe_id.username} unsubscribed to your channel!'

    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        blog_id=blog_id,
        created_for=created_for,
        is_read=is_read,  # Set the value of is_read
    )
    
    

    return notification
