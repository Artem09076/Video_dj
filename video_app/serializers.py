from rest_framework import serializers
from .models import Video, Comment, User


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'name_video', 'comment', 'date_publication']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'count_likes', 'date_publication']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_name', 'date_registrated', 'videos']

