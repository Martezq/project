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


