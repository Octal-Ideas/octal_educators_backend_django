from djoser import email

from django.contrib.auth.tokens import default_token_generator


from djoser import utils
from djoser.conf import settings

class SignUpActivationEmail(email.BaseEmailMessage):
    template_name = 'emails/activation_email.html'
    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context
