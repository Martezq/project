from django.db import models
from django.conf import settings

class Note(models.Model):
    COLOR_CHOICES = [
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='green')

class Reminder(models.Model):

    REPEAT_CHOICES = [
        ('none', 'Not set'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    note = models.OneToOneField('notes.Note', on_delete=models.CASCADE)
    remind_at = models.DateTimeField()
    email_notification = models.BooleanField(default=False)
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    remind_before = models.PositiveIntegerField(default=0)

