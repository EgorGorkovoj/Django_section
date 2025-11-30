from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    StringRelatedField,
)

from video.models import Video, VideoFile

User = get_user_model()


class VideoFielSerializer(ModelSerializer):
    class Meta:
        model = VideoFile
        fields = (
            'file',
            'quality',
        )


class VideoRetrieveSerializer(ModelSerializer):
    owner = StringRelatedField()
    video_files = VideoFielSerializer(many=True)

    class Meta:
        model = Video
        fields = (
            'id',
            'owner',
            'name',
            'video_files',
            'total_likes',
            'created_at',
        )


class CreateLikeSerializer(ModelSerializer):
    class Meta:
        fields = (
            'user',
            'video',
        )


class IdListSerializer(Serializer):
    ids = ListField(child=IntegerField())


class StatisticSerializer(ModelSerializer):
    likes_sum = IntegerField()

    class Meta:
        model = User
        fields = ('username', 'likes_sum')
