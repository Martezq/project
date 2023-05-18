from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model


class AccountAdapter(DefaultAccountAdapter):

    def confirm_email(self, request, email_address):
        # Confirm the email using the parent class method
        super().confirm_email(request, email_address)

        # Get the user associated with the confirmed email
        User = get_user_model()
        user = User.objects.get(email=email_address.email)

        # Set email_verified field to True and save the user
        user.email_verified = True
        user.save()

