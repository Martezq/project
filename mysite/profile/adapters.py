from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model


class AccountAdapter(DefaultAccountAdapter):

    def confirm_email(self, request, email_address):
        super().confirm_email(request, email_address)
        User = get_user_model()
        user = User.objects.get(email=email_address.email)
        user.email_verified = True
        user.save()

