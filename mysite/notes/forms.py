from django import forms
from .models import Note, Reminder

class NoteForm(forms.ModelForm):
    remind_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),)
    email_notification = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, reminder_initial=None, **kwargs):
        super().__init__(*args, **kwargs)
        if reminder_initial:
            self.fields['remind_at'].initial = reminder_initial.get('remind_at')
            self.fields['email_notification'].initial = reminder_initial.get('email_notification')

    class Meta:
        model = Note
        fields = ['title', 'content', 'color']

    # def save(self, commit=True):
    #     if commit:
    #         instance = super().save(commit=True)
    #     else:
    #         instance = super().save(commit=False)
    #
    #     if self.cleaned_data['remind_at']:
    #         reminder, created = Reminder.objects.get_or_create(
    #             note=instance,
    #             defaults={
    #                 'remind_at': self.cleaned_data['remind_at'],
    #                 'email_notification': self.cleaned_data['email_notification'],
    #             }
    #         )
    #         if not created:
    #             reminder.remind_at = self.cleaned_data['remind_at']
    #             reminder.email_notification = self.cleaned_data['email_notification']
    #             if commit:
    #                 reminder.save()
    #     else:
    #         Reminder.objects.filter(note=instance).delete()
    #
    #     return instance

