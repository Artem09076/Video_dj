from django.contrib import admin
from .models import User, Video, Comment, UserVideo

class UserVideoInline(admin.TabularInline):
    model = UserVideo
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

admin.site.register([UserVideo, Comment])

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = (UserVideoInline, )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    model = Video
    inlines = (UserVideoInline, CommentInline)

