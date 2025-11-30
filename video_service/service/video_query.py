from django.db.models import Q


class VideoQuery:
    def is_published(self, video_queryset, user=None):
        if user is not None and user.is_authenticated:
            return video_queryset.filter(Q(is_published=True) | Q(owner=self.user))
        return video_queryset.filter(is_published=True)


video_query = VideoQuery()
