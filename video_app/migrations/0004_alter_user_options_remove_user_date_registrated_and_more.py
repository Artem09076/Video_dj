# Generated by Django 5.0.2 on 2024-04-29 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video_app", "0003_video_video_file"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.RemoveField(
            model_name="user",
            name="date_registrated",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_name",
        ),
        migrations.AddField(
            model_name="user",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
