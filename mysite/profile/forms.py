from django import forms
from .models import UserProfile
from django.forms import formset_factory
from notes.models import Note
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image', 'timezone']



class ReminderSettingsForm(forms.Form):
    color = forms.ChoiceField(choices=Note.COLOR_CHOICES, label='Color')
    repeat = forms.ChoiceField(choices=CustomUser.REPEAT_CHOICES, initial='none', label='Repeat')
    remind_before = forms.IntegerField(initial=0, label='Remind Before (minutes)', required=False)

ReminderSettingsFormSet = forms.formset_factory(ReminderSettingsForm, extra=1, max_num=len(Note.COLOR_CHOICES))
