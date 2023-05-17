from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from PIL import Image
from django.db.models import JSONField
import os
import uuid


def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_pics', new_filename)

class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False)
    reminder_intervals = JSONField(default=dict)



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to=unique_filename)
    email = models.EmailField('Email', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        default_image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', self.image.field.default)
        if self.image.path != default_image_path:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        
