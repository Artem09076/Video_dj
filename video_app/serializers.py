from rest_framework import serializers

from .models import Comment, Video


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ["name", "video_file", "during", "date_publication"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "date_publication"]
