import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from video.models import Video, VideoFile

User = get_user_model()


class Command(BaseCommand):
    help = """
           Удаляет тестовые видеоролики из БД, тестовых пользователей,
           связанные файлы из test_videos/
           """

    def handle(self, *args, **options):
        base_dir = settings.MEDIA_ROOT / 'test_videos'

        self.stdout.write(self.style.WARNING('Начинаю удаление тестовых файлов и записей...'))

        # Удаление физических файлов.
        if base_dir.exists():
            shutil.rmtree(base_dir, ignore_errors=True)
            self.stdout.write(self.style.SUCCESS('Директория test_videos удалена.'))
        else:
            self.stdout.write('Папка test_videos не существует — пропускаю удаление файлов.')

        videofile = VideoFile.objects.filter(file__startswith='test_videos/')
        count_vf = videofile.count()
        videofile.delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено VideoFile: {count_vf}'))

        video = Video.objects.filter(video_files__isnull=True, name__startswith='Test video')
        count_v = video.count()
        video.delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено Video: {count_v}'))

        user = User.objects.filter(username__startswith='test_user_')
        count_user = user.count()
        user.delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено Users: {count_user}'))

        self.stdout.write(self.style.SUCCESS('Очистка завершена!'))
