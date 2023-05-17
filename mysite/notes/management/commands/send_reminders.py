from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from models import Reminder
from profile.models import CustomUser
from datetime import timedelta
from django.conf import settings


class Command(BaseCommand):
    help = 'Sends email reminders for notes'

    def handle(self, *args, **options):
        now = timezone.now()
        reminders = Reminder.objects.filter(remind_at__lte=now, email_notification=True)

        for reminder in reminders:
            note = reminder.note
            user = CustomUser.objects.get(id=note.user_id)  # Assuming note has user_id field
            subject = f'Reminder: {note.title}'
            message = note.content
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]  # Use user's email

            # Send email
            send_mail(subject, message, from_email, recipient_list)

            # If reminder is repeating, calculate the next remind_at time and save
            if reminder.repeat != 'none':
                if reminder.repeat == 'daily':
                    reminder.remind_at += timedelta(days=1)
                elif reminder.repeat == 'weekly':
                    reminder.remind_at += timedelta(weeks=1)
                elif reminder.repeat == 'monthly':
                    reminder.remind_at += timedelta(weeks=4)  # Approximate a month with 4 weeks

                # Save the updated reminder
                reminder.save()

