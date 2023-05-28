from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from pytz import timezone as pytz_timezone
from notes.models import Reminder
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import get_current_timezone
import pytz
import logging
from django.db import DatabaseError


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends email reminders for notes'

    def handle(self, *args, **options):
        try:
            reminders = Reminder.objects.filter(email_notification=True)
        except DatabaseError as e:
            logger.error(f"Database error when fetching reminders: {e}")
            return
        
        for reminder in reminders:
            note = reminder.note
            user = note.user
            user_timezone = pytz.timezone(user.userprofile.timezone)

            now = timezone.now().astimezone(user_timezone) 

            reminder_time = reminder.remind_at
            reminder_time_user_tz = reminder_time.astimezone(user_timezone)
           
            tz_offset = reminder_time_user_tz.utcoffset()

            reminder_time_user_tz -= tz_offset

            repeat_key = f'repeat_{note.color}'
            remind_before_key = f'remind_before_{note.color}'
            repeat_choice = user.reminder_intervals.get(repeat_key, 'none')
            remind_before = user.reminder_intervals.get(remind_before_key, 0)

            if remind_before is None:
                remind_before = 0

            if now >= reminder_time_user_tz - timedelta(minutes=remind_before):
                subject = f'Reminder: {note.title}'
                message = note.content
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list)

                try:
                    if repeat_choice != 'none':
                        if repeat_choice == 'daily':
                            reminder.remind_at += timedelta(days=1)
                        elif repeat_choice == 'weekly':
                            reminder.remind_at += timedelta(weeks=1)

                        reminder.save()
                except DatabaseError as e:
                    logger.error(f"Database error when saving reminder: {e}")


