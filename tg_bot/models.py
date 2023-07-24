from django.db import models


class Profile(models.Model):
    tg_user_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в Telegram',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )

    def __str__(self) -> str:
        return f'#{self.tg_user_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
