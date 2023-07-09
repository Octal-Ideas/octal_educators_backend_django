from djoser import email


class ActivationEmail(email.BaseEmailMessage):
    template_name = 'emails/activation_email.html'