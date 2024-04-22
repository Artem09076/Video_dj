# Generated by Django 5.0.2 on 2024-04-19 17:40

import django.db.models.deletion
import uuid
import video_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "date_publication",
                    models.DateTimeField(
                        validators=[video_app.models.check_date],
                        verbose_name="date publication",
                    ),
                ),
                ("comment_text", models.TextField(verbose_name="full_name")),
                (
                    "count_likes",
                    models.PositiveIntegerField(blank=True, verbose_name="count likes"),
                ),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
                "db_table": '"video_data"."comments"',
                "ordering": ["date_publication"],
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user_name",
                    models.TextField(max_length=100, verbose_name="user name"),
                ),
                (
                    "date_registrated",
                    models.DateTimeField(
                        validators=[video_app.models.check_date],
                        verbose_name="date registrated",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": '"video_data"."users"',
                "ordering": ["date_registrated"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "date_publication",
                    models.DateTimeField(
                        validators=[video_app.models.check_date],
                        verbose_name="date publication",
                    ),
                ),
                (
                    "name_video",
                    models.TextField(max_length=100, verbose_name="name video"),
                ),
                ("during", models.PositiveIntegerField(verbose_name="during")),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="video_app.comment",
                        verbose_name="comment",
                    ),
                ),
            ],
            options={
                "verbose_name": "video",
                "verbose_name_plural": "videos",
                "db_table": '"video_data"."videos"',
                "ordering": ["date_publication"],
            },
        ),
        migrations.CreateModel(
            name="UserVideo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="video_app.user",
                        verbose_name="user",
                    ),
                ),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="video_app.video",
                        verbose_name="video",
                    ),
                ),
            ],
            options={
                "verbose_name": "relationship user video",
                "verbose_name_plural": "relationships user video",
                "db_table": '"video_data"."user_video"',
                "unique_together": {("user", "video")},
            },
        ),
        migrations.AddField(
            model_name="user",
            name="videos",
            field=models.ManyToManyField(
                through="video_app.UserVideo",
                to="video_app.video",
                verbose_name="videos",
            ),
        ),
    ]
