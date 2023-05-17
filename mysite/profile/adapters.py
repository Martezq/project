from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import send_mail



class AccountAdapter(DefaultAccountAdapter):
    # def send_mail(self, template_prefix, email, context):
        # Customize the email sending process, e.g., using Django's email sending functions
    pass
