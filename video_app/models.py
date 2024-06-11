"""This module include models db."""
from datetime import datetime
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_minio_backend import MinioBackend, iso_date_prefix


def check_date(date: datetime) -> None:
    """Check date.

    Args:
        date (datetime): date

    Raises:
        ValidationError: raise if date more then current date
    """
    if date > timezone.now():
        raise ValidationError(_('Date must be less or equal than current date'))


class UUIDMixin(models.Model):
    """Mixin with uuid field.

    Args:
        models: Model
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Meta class for UUIDMixin."""

        abstract = True


class DatePublicationMixin(models.Model):
    """Date publication mixin.

    Args:
        models: Model
    """

    date_publication = models.DateTimeField(
        _('date publication'), null=False, blank=False, validators=[check_date], auto_now_add=True,
    )

    class Meta:
        """Meta class for DatePublicationMixin."""

        abstract = True


MAX_LENGHT_NAME = 100
FILE_EXTENSION = ('mp4',)


class Video(UUIDMixin, DatePublicationMixin):
    """Video model.

    Args:
        UUIDMixin: mixin with uuid fields
        DatePublicationMixin: mixin with data publication fields
    """

    name = models.TextField(
        _('name video'), null=False, blank=False, max_length=MAX_LENGHT_NAME,
    )
    video_file = models.FileField(
        _('video'),
        blank=True,
        null=True,
        validators=[FileExtensionValidator(FILE_EXTENSION)],
        storage=MinioBackend(bucket_name='djangob'),
        upload_to=iso_date_prefix,
    )
    cover_video_file = models.ImageField(
        _('cover video'),
        blank=True,
        null=True,
        storage=MinioBackend(bucket_name='djangob'),
        upload_to=iso_date_prefix)
    during = models.PositiveIntegerField(_('during'), null=False, blank=False)
    user = models.ForeignKey('CustomUser', verbose_name=_('user'),
                             on_delete=models.CASCADE, null=True)
    description = models.TextField(_('discription video'), null=True, blank=True, max_length=1000)

    def __str__(self) -> str:
        """Str method.

        Returns:
            string with name and during of video
        """
        return f'{self.name}: {self.during}'

    class Meta:
        """Meta class for Video."""

        db_table = '"video_data"."videos"'
        ordering = ['-date_publication']
        verbose_name = _('video')
        verbose_name_plural = _('videos')


class Comment(UUIDMixin, DatePublicationMixin):
    """Comment model.

    Args:
        UUIDMixin: mixin with uuid fields
        DatePublicationMixin: mixin with data publication fields
    """

    text = models.TextField(_('text'), null=True, blank=False)
    video = models.ForeignKey(
        Video, verbose_name=_('video'), on_delete=models.CASCADE, null=True,
    )
    user = models.ForeignKey('CustomUser', verbose_name=_('user'),
                             on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        """Magic str method.

        Returns:
            Comment text
        """
        return self.text

    class Meta:
        """Meta class for Comment."""

        db_table = '"video_data"."comments"'
        ordering = ['-date_publication']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class CustomUser(UUIDMixin):
    """Custom user model.

    Args:
        UUIDMixin: mixin with uuid fields
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=False,
    )

    def __str__(self) -> str:
        """Magic str method.

        Returns:
            Username
        """
        return self.user.username

    class Meta:
        """Meta class for CustomUser."""

        db_table = '"video_data"."users"'
        verbose_name = _('user')
        verbose_name_plural = _('users')
