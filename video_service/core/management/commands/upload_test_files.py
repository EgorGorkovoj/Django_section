import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from video.models import Video, VideoFile

User = get_user_model()


class Command(BaseCommand):
    help = """
    Создает тестовых пользователей, видеоролики в БД и файлы формата .mp4
    в директорию media/test_videos/
    """

    def handle(self, *args, **options):
        users_to_create = []
        for i in range(10000):
            users_to_create.append(
                User(username=f'test_user_{i}', email=f'user{i}@example.com', is_active=True)
            )
        User.objects.bulk_create(users_to_create, batch_size=2000)

        users = list(User.objects.all())

        self.stdout.write(self.style.SUCCESS(f'Создано {len(users)} пользователей.'))

        videos_to_create = []
        video_files_to_create = []

        base_dir = settings.MEDIA_ROOT / 'test_videos'
        os.makedirs(base_dir, exist_ok=True)

        for i in range(100000):
            owner = random.choice(users)
            video = Video(owner=owner, name=f'Test video №{i}', is_published=True)
            videos_to_create.append(video)

        Video.objects.bulk_create(videos_to_create, batch_size=2000)

        qualities = [
            VideoFile.QualityChoices.HD,
            VideoFile.QualityChoices.FHD,
            VideoFile.QualityChoices.UHD,
        ]

        created_videos = Video.objects.order_by('-id')[:100000]

        for video in created_videos:
            for quality in qualities:
                filename = f'video_{video.id}_{quality}.mp4'
                filepath = os.path.join(base_dir, filename)

                # Создаю пустой mp4-файл.
                with open(filepath, 'wb') as f:
                    # Формат MP4 (ISO Base Media File Format, ISO/IEC 14496-12) состоит из боксов.
                    f.write(b'\x00\x00\x00\x20ftypisom')  # Минимальный box header

                relative_path = f'test_videos/{filename}'

                file_obj = VideoFile(
                    video=video,
                    file=relative_path,
                    quality=quality,
                )
                video_files_to_create.append(file_obj)

        VideoFile.objects.bulk_create(video_files_to_create, batch_size=2000)

        self.stdout.write(self.style.SUCCESS('Готово — 100000 видео и mp4 файлов созданы.'))
