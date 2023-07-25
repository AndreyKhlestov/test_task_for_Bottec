from django.db import models


class Profile(models.Model):
    tg_user_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в Telegram',
        unique=True,
    )
    name = models.CharField(
        max_length=32,
        verbose_name='Имя пользователя'
    )

    def __str__(self) -> str:
        return f'#{self.tg_user_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название категории', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    name = models.CharField(max_length=64, verbose_name='Название подкатегории', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory,
                                    on_delete=models.CASCADE,
                                    related_name='products',
                                    verbose_name='Подкатегория'
                                    )
    name = models.CharField(max_length=64, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
