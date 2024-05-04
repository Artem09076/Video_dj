from django.contrib import admin
from .models import User, Video, Comment, UserVideo


class UserVideoInline(admin.TabularInline):
    model = UserVideo
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class UserInline(admin.TabularInline):
    model = User
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 2


admin.site.register([Comment, UserVideo])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = (UserVideoInline,)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    model = Video
    inlines = (UserVideoInline, CommentInline)
