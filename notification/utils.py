# from .models import Notification

# from blog.models import Blog
# from subscriber.models import Subscriber

# # create_notification(request, 'blog_like', 'lskjf-j12l3-jlas-jdfa', 'lskjf-j12l3-jlas-jdfa')


# def create_notification(request, type_of_notification, blog_id=None, subscribe_id=None):
#     created_for = None

#     if type_of_notification == 'blog_like':
#         body = f'{request.user.name} liked one of your blog!'
#         blog = Blog.objects.get(pk=blog_id)
#         created_for = blog.created_by
#     elif type_of_notification == 'blog_comment':
#         body = f'{request.user.name} commented on one of your blog!'
#         blog = Blog.objects.get(pk=blog_id)
#         created_for = blog.created_by
#     elif type_of_notification == 'new_blog':
#         blog = Blog.objects.get(pk=blog_id)
#         created_for = blog.created_by
#         body = f'{request.user.name} sent you a friend request!'
#     elif type_of_notification == 'subscribe':
#         subscribe = Subscriber.objects.get(pk=subscribe_id)
#         created_for = subscribe.created_by
#         body = f'{request.user.name} subscribed to your channel!'
#     elif type_of_notification == 'runsubscribe':
#         unsubscribe = Subscriber.objects.get(pk=subscribe_id)
#         created_for = unsubscribe.content_owner
#         body = f'{request.user.name} rejected your friend request!'

#     notification = Notification.objects.create(
#         body=body,
#         type_of_notification=type_of_notification,
#         created_by=request.user,
#         blog_id=blog_id,
#         created_for=created_for
#     )

#     return notification