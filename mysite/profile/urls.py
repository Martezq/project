from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.index, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
