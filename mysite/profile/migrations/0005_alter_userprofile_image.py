# Generated by Django 4.2 on 2023-05-22 17:03

from django.db import migrations, models
import profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='profile_pics/default.png', upload_to=profile.models.unique_filename),
        ),
    ]
