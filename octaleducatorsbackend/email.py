from djoser import email
class ActivationEmail(email.ActivationEmail):
    template_name = 'emails/activation_email.html'
