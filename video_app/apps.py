"""This module include VideoAppConfig."""
from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    """Config module for video app.

    Args:
        AppConfig: django config app
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_app'
