# Generated by Django 5.0.6 on 2024-06-16 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("video_app", "0002_remove_comment_count_likes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["-date_publication"],
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
            },
        ),
        migrations.AlterModelOptions(
            name="video",
            options={
                "ordering": ["-date_publication"],
                "verbose_name": "video",
                "verbose_name_plural": "videos",
            },
        ),
    ]
