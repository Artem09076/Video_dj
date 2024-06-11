"""This module include model serializers."""
from rest_framework import serializers

from .models import Comment, Video


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for video model.

    Args:
        serializers: HyperlinkedModelSerializer
    """

    class Meta:
        """Meta class for VideoSerializer."""

        model = Video
        fields = ['name', 'video_file', 'during', 'date_publication']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializers for model comment.

    Args:
        serializers: HyperlinkedModelSerializer
    """

    class Meta:
        """Meta class for CommentSerializer."""

        model = Comment
        fields = ['id', 'text', 'date_publication']
