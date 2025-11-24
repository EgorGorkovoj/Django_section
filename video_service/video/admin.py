from django.contrib import admin

from .models import Like, Video, VideoFile


class ApiVideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'is_published',
        'total_likes',
        'created_at',
    )
    search_fields = ('owner__first_name', 'name')
    list_filter = ('name',)
    list_display_links = ('owner',)


class ApiVideoFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'video',
        'file',
        'quality',
    )
    search_fields = ('video__name',)
    list_filter = ('video', 'quality')
    list_display_links = ('video',)


class ApiLikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'video',
    )
    search_fields = (
        'user__first_name',
        'video__name',
    )
    list_filter = ('user', 'video')
    list_display_links = ('user', 'video')


admin.site.register(Video, ApiVideoAdmin)
admin.site.register(VideoFile, ApiVideoFileAdmin)
admin.site.register(Like, ApiLikeAdmin)
