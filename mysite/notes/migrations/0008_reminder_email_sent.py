# Generated by Django 4.2 on 2023-05-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_remove_reminder_user_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
