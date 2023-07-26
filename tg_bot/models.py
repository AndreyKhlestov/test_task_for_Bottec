from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Sum


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

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название товара')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items',)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт. по {self.product.price} руб."
