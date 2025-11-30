from core.logger import logger
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import F
from video.models import Like, Video

User = get_user_model()


class LikeQuery:
    def __init__(self, video: Video, user: User):  # type: ignore
        self.video = video
        self.user = user

    def _update_like(self, value: int):
        self.video.total_likes = F('total_likes') + value
        self.video.save(update_fields=['total_likes'])

    def like(self):
        try:
            with transaction.atomic():
                Like.objects.create(user=self.user, video=self.video)
                self._update_like(value=1)
                logger.info('Лайк успешно создан!')
        except IntegrityError:
            logger.warning('Лайк уже существует (IntegrityError)')
            return False
        return True

    def remove_like(self):
        try:
            with transaction.atomic():
                like = (
                    self.user.likes.all()
                    .filter(video=self.video)
                    .select_for_update(skip_locked=True)
                    .first()
                )

                if like is None:
                    logger.info('Лайка не существует!')
                    return False

                like.delete()
                self._update_like(value=-1)
                logger.info('Лайк успешно удален!')
                return True
        except IntegrityError:
            logger.error('Ошибка при удалении лайка!')
            return False
