from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    warm_up_duration = models.PositiveIntegerField()
    high_intensity_duration = models.PositiveIntegerField()
    recovery_duration = models.PositiveIntegerField()
    number_of_intervals = models.PositiveIntegerField() 
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
