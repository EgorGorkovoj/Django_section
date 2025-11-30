from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from service.like_query import LikeQuery
from service.staticstic_query import statistic_query
from service.video_query import video_query
from video.models import Video
from video.serializers import IdListSerializer, StatisticSerializer, VideoRetrieveSerializer


class VideoViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Video.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return VideoRetrieveSerializer

        if self.action in ('statistics_subquery', 'statistics_group_by'):
            return StatisticSerializer
        raise NotImplementedError

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset.prefetch_related('video_files').order_by('-created_at')

        if self.action in ('retrieve', 'list'):
            return video_query.is_published(queryset)

        return video_query.is_published(queryset, user=self.request.user)

    @extend_schema(
        responses={status.HTTP_201_CREATED: None, status.HTTP_204_NO_CONTENT: None},
    )
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def likes(self, request, *args, **kwargs):
        like_object = LikeQuery(video=self.get_object(), user=request.user)

        if request.method == 'POST':
            like_object.like()
            return Response(status=status.HTTP_201_CREATED)

        like_object.remove_like()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={status.HTTP_200_OK: IdListSerializer},
    )
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            IsAdminUser,
        ],
    )
    def ids(self, request, *args, **kwargs):
        videos = self.get_queryset().values_list('id', flat=True)
        return Response(videos, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_200_OK: StatisticSerializer},
    )
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            IsAdminUser,
        ],
        url_path='statistics-subquery',
    )
    def statistics_subquery(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        video = video_query.is_published(queryset)
        statistic = statistic_query.statistic_like_subquery(video)
        serializer = self.get_serializer(statistic, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_200_OK: StatisticSerializer},
    )
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            IsAdminUser,
        ],
        url_path='statistics-group-by',
    )
    def statistics_group_by(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        video = video_query.is_published(queryset)
        statistic = statistic_query.statistic_like_group_by(video)
        serializer = self.get_serializer(statistic, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
