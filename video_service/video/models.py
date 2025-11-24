from core.constants import DefaultFieldConstants, LengthFieldConstants
from django.contrib.auth.models import User
from django.db import models


def get_upload_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Video(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='videos', verbose_name='Владелец'
    )
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False)
    name = models.CharField(
        verbose_name='Название', max_length=LengthFieldConstants.VIDEO_NAME_LENGTH
    )
    total_likes = models.PositiveIntegerField(
        verbose_name='Количество лайков', default=DefaultFieldConstants.TOTAL_LIKES_VIDEO
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    class QualityChoices(models.TextChoices):
        HD = '720p', 'HD (720p)'
        FHD = '1080p', 'Full HD (1080p)'
        UHD = '4K', 'Ultra HD (4K)'

    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='video_files', verbose_name='Видео'
    )
    file = models.FileField(verbose_name='Файл', upload_to=get_upload_path)
    quality = models.CharField(
        verbose_name='Качество',
        max_length=LengthFieldConstants.VIDEO_FILE_QUALITY_LENGTH,
        choices=QualityChoices.choices,
    )

    class Meta:
        verbose_name = 'Видеофайл'
        verbose_name_plural = 'Видеофайлы'

    def __str__(self):
        return self.file


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь'
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='likes', verbose_name='Видео'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='unique_user_video_like')
        ]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user.first_name} лайкнул {self.video.name}'
