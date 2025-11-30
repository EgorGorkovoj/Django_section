from django.contrib.auth import get_user_model
from django.db.models import F, OuterRef, Subquery, Sum

User = get_user_model()


class StatisticQuery:
    def statistic_like_subquery(self, queryset):
        likes_sum = (
            queryset.filter(owner=OuterRef('id'))
            .values('owner')
            .annotate(likes_sum=Sum('total_likes'))
            .values('total_likes')
        )
        users = (
            User.objects.values('username')
            .annotate(likes_sum=Subquery(likes_sum))
            .order_by('-likes_sum')
        )
        return users

    def statistic_like_group_by(self, queryset):
        return (
            queryset.annotate(username=F('owner__username'))
            .values('username')
            .annotate(likes_sum=Sum('total_likes'))
            .order_by('-total_likes')
        )


statistic_query = StatisticQuery()
