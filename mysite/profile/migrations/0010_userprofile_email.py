# Generated by Django 4.2 on 2023-05-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0009_remove_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
    ]
