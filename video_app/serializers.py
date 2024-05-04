from rest_framework import serializers
from .models import Video, Comment



class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ["name", "video_file", 'during', "date_publication"]
    



class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "count_likes", "date_publication"]

