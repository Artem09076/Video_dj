from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone
from django.core.exceptions import ValidationError


def get_datetime() -> datetime:
    return datetime.now(timezone.utc)

def check_date(date: datetime) -> None:
    if date > get_datetime():
        raise ValidationError('О вы из будущего')


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class DatePublicationMixin(models.Model):
    date_publication = models.DateTimeField(
        _('date publication'), null=False, blank=False, validators=[check_date])

    class Meta:
        abstract = True




MAX_LENGHT_NAME = 100


class Video(UUIDMixin, DatePublicationMixin):
    name = models.TextField(
        _('name video'), null=False, blank=False, max_length=MAX_LENGHT_NAME)
    during = models.PositiveIntegerField(_('during'), null=False, blank=False)

    
    def __str__(self) -> str:
        return f'{self.name}: {self.during}'

    class Meta:
        db_table = '"video_data"."videos"'
        ordering = ['date_publication']
        verbose_name = _('video')
        verbose_name_plural = _('videos')

class Comment(UUIDMixin, DatePublicationMixin):
    text = models.TextField(_('comment text'), null=False, blank=False)
    count_likes = models.PositiveIntegerField(
        _('count likes'), null=False, blank=True)
    
    video = models.ForeignKey(Video, verbose_name=_('video'), on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return f'{self.text}: {self.count_likes}'

    class Meta:
        db_table = '"video_data"."comments"'
        ordering = ['date_publication']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

class User(UUIDMixin):
    user_name = models.TextField(
        _('user name'), null=False, blank=False,  max_length=MAX_LENGHT_NAME)
    date_registrated = models.DateTimeField(
        _('date registrated'), null=False, blank=False, validators=[check_date])

    videos = models.ManyToManyField(
        Video, verbose_name=_('videos'), through='UserVideo')

    def __str__(self) -> str:
        return f'{self.user_name}: {self.date_registrated.time().isoformat()}'

    class Meta:
        db_table = '"video_data"."users"'
        ordering = ['date_registrated']
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserVideo(UUIDMixin):
    user = models.ForeignKey(User, verbose_name=_(
        'user'), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_(
        'video'), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.user_name}: {self.video.name}'

    class Meta:
        db_table = '"video_data"."user_video"'
        unique_together = (
            ('user', 'video'),
        )
        verbose_name = _('relationship user video')
        verbose_name_plural = _('relationships user video')
