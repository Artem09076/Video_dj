"""This module register video app model."""
from django.contrib import admin

from .models import Comment, CustomUser, Video


class CommentInline(admin.TabularInline):
    """Inline for comment model.

    Args:
        admin: TabularInline
    """

    model = Comment
    extra = 1


class UserInline(admin.TabularInline):
    """Inline for user model.

    Args:
        admin: TabularInline
    """

    model = CustomUser
    extra = 1


class VideoInline(admin.TabularInline):
    """Inline for video model.

    Args:
        admin: TabularInline
    """

    model = Video
    extra = 2


admin.site.register([Comment])


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Register CustomUser to admin.

    Args:
        admin: ModelAdmin
    """

    model = CustomUser
    inlines = (VideoInline,)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Register Video to admin.

    Args:
        admin: ModelAdmin
    """

    model = Video
    inlines = (CommentInline, )
