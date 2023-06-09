from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm
from django.shortcuts import render, get_object_or_404


def workout_view(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('hiit:workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'hiit/workout_form.html', {'form': form})

def workout_edit(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('hiit:workout_list')
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'hiit/workout_form.html', {'form': form})

def workout_delete(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    if request.method == 'POST':
        workout.delete()
        return redirect('hiit:workout_list')
    return render(request, 'hiit/workout_delete.html', {'workout': workout})

def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'hiit/workout_list.html', {'workouts': workouts})


def workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    return render(request, 'hiit/workout.html', {'workout': workout})
