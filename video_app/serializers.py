from rest_framework import serializers
from .models import Video, Comment, User


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ["name", "video_file", 'during', "date_publication"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "count_likes", "date_publication"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user", "videos"]
