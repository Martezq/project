from django import forms
from .models import UserProfile
from django.forms import formset_factory
from notes.models import Note, Reminder


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'email']



class ReminderSettingsForm(forms.Form):
    color = forms.ChoiceField(choices=Note.COLOR_CHOICES, label='Color')
    repeat = forms.ChoiceField(choices=Reminder.REPEAT_CHOICES, initial='none', label='Repeat')
    remind_before = forms.IntegerField(initial=0, label='Remind Before (minutes)', required=False)

ReminderSettingsFormSet = forms.formset_factory(ReminderSettingsForm, extra=1, max_num=len(Note.COLOR_CHOICES))
