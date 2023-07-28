from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import asyncio

from .bot.utils.send_message_all_users import send_message_to_all_users


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

    def basket(self):
        """
        Получение корзины пользователя.
        Корзиной будет считаться тот Orders, который еще не оплачен (такой заказ у пользователя может быть только один).
        """
        # Проверяем, есть ли у пользователя незавершенный заказ (с payment_status=False)
        existing_cart = self.orders.filter(payment_status=False).first()

        if existing_cart:
            # Если есть, то возвращаем его
            return existing_cart
        else:
            # Если нет, то создаем новый заказ
            new_cart = Order(profile=self)
            new_cart.save()
            return new_cart


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название категории', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория'
                                 )
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
    name = models.CharField(max_length=64, verbose_name='Название товара', unique=True)
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)], verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField(verbose_name='Адрес')
    payment_status = models.BooleanField(verbose_name='Статус оплаты', default=False)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость всего заказа', default=0)
    payment_datetime = models.DateTimeField(verbose_name='Дата и время оплаты', blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        if self.payment_status and not self.payment_datetime:
            # Если заказ оплачен, но дата/время оплаты еще не установлены, устанавливаем текущее время
            self.payment_datetime = timezone.now()

        self.total_cost = self.order_items.aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0
        if not self.payment_status:
            # Есть ли уже заказ с payment_status=False для этого профиля
            existing_order = Order.objects.filter(profile=self.profile, payment_status=False).first()
            if existing_order and existing_order != self:
                raise ValidationError("Для каждого профиля разрешен только один заказ с payment_status=False.")
        super().save(*args, **kwargs)

    def __str__(self):
        return ("\n".join([str(order_item) for order_item in self.order_items.all()]) +
                f'\n\nОбщая сумма:     {self.total_cost} руб.')


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Название товара',
                                related_name='order_items'
                                )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара', validators=[MinValueValidator(1)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт. по {self.product.price} руб."


class TelegramMessage(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    start_date_time = models.DateTimeField(verbose_name='Дата/время начала рассылки', auto_now_add=True)
    end_date_time = models.DateTimeField(verbose_name='Дата/время завершения рассылки', blank=True, null=True)
    send_status = models.BooleanField(verbose_name='Статус завершения отправки', default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def save(self, *args, **kwargs):
        # if not self.send_status:
        #     asyncio.run(send_message_to_all_users(str(self.text)))
        if self.send_status and not self.end_date_time:
            self.end_date_time = timezone.now()

        super().save(*args, **kwargs)
