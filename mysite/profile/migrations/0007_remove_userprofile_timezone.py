# Generated by Django 4.2 on 2023-05-27 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_userprofile_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timezone',
        ),
    ]
