from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note, Reminder
from .forms import NoteForm
import logging

logger = logging.getLogger('notes')


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

from django.utils import timezone

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            print(f'Saved note with ID {note.id}')
            
            remind_at = form.cleaned_data['remind_at']
            email_notification = form.cleaned_data['email_notification']
            
            if remind_at:
                reminder, created = Reminder.objects.get_or_create(
                    note=note,
                    defaults={
                        'remind_at': remind_at,
                        'email_notification': email_notification,
                    }
                )
                if created:
                    logger.info(f'Saved reminder with ID {reminder.id} for note with ID {note.id}')
                else:
                    reminder.remind_at = remind_at
                    reminder.email_notification = email_notification
                    reminder.save()
            else:
                Reminder.objects.filter(note=note).delete()
            
            return redirect('notes:note_list')
    else:
        form = NoteForm()

    context = {
        'form': form,
        'form_title': 'Create Note',
        'form_submit_text': 'Create'
    }
    return render(request, 'notes/note_form.html', context)





@login_required
def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    reminder = Reminder.objects.filter(note=note).first()
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            remind_at = form.cleaned_data['remind_at']
            email_notification = form.cleaned_data['email_notification']
            
            if remind_at:
                if reminder:
                    reminder.remind_at = remind_at
                    reminder.email_notification = email_notification
                    reminder.email_sent = False
                    reminder.save()
                else:
                    Reminder.objects.create(
                        note=note,
                        remind_at=remind_at,
                        email_notification=email_notification,
                        email_sent=False,
                    )
            else:
                if reminder:
                    reminder.delete()
            
            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note, initial={
            'remind_at': reminder.remind_at if reminder else None,
            'email_notification': reminder.email_notification if reminder else False,
        })

    context = {
        'form': form,
        'form_title': 'Update Note',
        'form_submit_text': 'Update'
    }
    return render(request, 'notes/note_form.html', context)

@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
