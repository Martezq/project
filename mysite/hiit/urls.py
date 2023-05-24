from django.urls import path
from . import views

app_name = 'hiit'

urlpatterns = [
    path('new/', views.workout_view, name='new_workout'),
    path('list/', views.workout_list, name='workout_list'),
    path('workout/<int:workout_id>', views.workout, name='workout')
]
