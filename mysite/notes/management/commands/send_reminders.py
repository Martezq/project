from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from ...models import Reminder

class Command(BaseCommand):
    help = 'Sends email reminders for notes'

    def handle(self, *args, **options):
        now = timezone.now()
        reminders = Reminder.objects.filter(remind_at__lte=now, email_notification=True)

        for reminder in reminders:
            note = reminder.note
            subject = f'Reminder: {note.title}'
            message = note.content
            from_email = 'your_email_address'
            recipient_list = ['recipient@example.com']

