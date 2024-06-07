from django.contrib import admin
from django.conf.global_settings import AUTH_USER_MODEL
from .models import Comment, CustomUser, Video




class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class UserInline(admin.TabularInline):
    model = CustomUser
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 2


admin.site.register([Comment])


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    inlines = (VideoInline,)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    model = Video
    inlines = (CommentInline, )
