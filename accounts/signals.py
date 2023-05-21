from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.conf import settings

import six  

User = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=User)
# def send_registration_notification(sender, instance, created, **kwargs):
#     if created:
#         # Generate the email content
#         subject = "Welcome to Our Website!"
#         message = "Thank you for registering with us. We are excited to have you on board!"

#         # Send the email
#         send_mail(subject, message, "noreply@example.com", [instance.email])
        

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (  
            six.text_type(user.pk) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  
        
account_activation_token = TokenGenerator()  