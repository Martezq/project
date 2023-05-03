from django.contrib import admin
from .models import Note, Reminder

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('user', 'created_at')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('note', 'remind_at', 'email_notification')
    list_filter = ('email_notification', 'remind_at')
