from django.db import models
# from django.contrib.auth import get_user_model


class Profile(models.Model):
    tg_user_id = models.IntegerField(
        verbose_name='ID пользователя в Telegram'
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )

    def __str__(self) -> str:
        return f'#{self.tg_user_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
