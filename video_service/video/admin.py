from django.contrib import admin
from django.utils.html import format_html

from .models import Like, Video, VideoFile


class VideoFileInline(admin.TabularInline):
    model = VideoFile
    extra = 0
    fields = ('file', 'quality')
    readonly_fields = ('file',)


class ApiVideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'is_published',
        'total_likes',
        'created_at',
        'video_files_list',
    )
    search_fields = ('owner__first_name', 'name')
    list_filter = (
        'name',
        'owner',
    )
    list_display_links = ('name',)
    inlines = [
        VideoFileInline,
    ]

    @admin.display(description='Видео файлы')
    def video_files_list(self, obj):
        files = obj.video_files.all()
        if not files:
            return '-'
        links = []
        for f in files:
            links.append(format_html('<a href="{}" target="_blank">{}</a>', f.file.url, f.quality))
        return format_html('<br>'.join(links))


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
