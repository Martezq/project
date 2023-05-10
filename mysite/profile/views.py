from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm, ReminderSettingsFormSet
from notes.models import Note, Reminder


@login_required
def profile(request):
    user = request.user
    
    reminder_settings = {}
    for color, _ in Note.COLOR_CHOICES:
        reminder_settings[color] = {
            'repeat': user.reminder_intervals.get(f'repeat_{color}', 'none'),
            'remind_before': user.reminder_intervals.get(f'remind_before_{color}', 0),
        }

    context = {
        'user': user,
        'reminder_settings': reminder_settings,
    }
    return render(request, 'profile/profile.html', context)


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        reminder_settings_formset = ReminderSettingsFormSet(request.POST, prefix='reminder_settings')

        if profile_form.is_valid() and reminder_settings_formset.is_valid() and reminder_settings_formset.management_form.is_valid():
            profile_form.save()


            reminder_intervals = user.reminder_intervals
            for form in reminder_settings_formset:
                if form.is_valid() and form.has_changed():
                    color = form.cleaned_data['color']
                    repeat = form.cleaned_data['repeat']
                    remind_before = form.cleaned_data['remind_before']
                    reminder_intervals[f'repeat_{color}'] = repeat
                    reminder_intervals[f'remind_before_{color}'] = remind_before

            user.reminder_intervals = reminder_intervals
            user.save()

            return redirect('profile:profile')

    else:
        profile_form = UserProfileForm(instance=user.userprofile)
        reminder_settings_initial = []

        for color, _ in Note.COLOR_CHOICES:
            repeat_key = f'repeat_{color}'
            remind_before_key = f'remind_before_{color}'
            reminder_settings_initial.append({
                'color': color,
                'repeat': user.reminder_intervals.get(repeat_key, None),
                'remind_before': user.reminder_intervals.get(remind_before_key, None),
            })

        reminder_settings_formset = ReminderSettingsFormSet(prefix='reminder_settings', initial=reminder_settings_initial)

    context = {
        'profile_form': profile_form,
        'reminder_settings_formset': reminder_settings_formset,
    }
    return render(request, 'profile/edit_profile.html', context)


