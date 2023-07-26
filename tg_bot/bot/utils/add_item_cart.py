from django.shortcuts import get_object_or_404
from decimal import Decimal
from tg_bot.models import Profile, Product, OrderItem


def add_to_cart(tg_user_id: int, product_id: int, quantity: int):
    """Функция для автоматического добавления товара в корзину покупок"""
    profile = Profile.objects.get(tg_user_id=tg_user_id)  # данные о пользователе
    product = Product.objects.get(id=product_id)  # данные о товаре
    cart = profile.basket()  # Получаем текущий активный заказ пользователя или создаем новый

    # Проверьте, существует ли уже элемент OrderItem для этого продукта в текущем заказе
    order_item, created = OrderItem.objects.get_or_create(product=product, order=cart)

    # Если элемент уже существует, обновите его количество и общую стоимость
    if not created:
        order_item.quantity += quantity
        order_item.save()

    # Иначе, если элемент только что создан, установите количество и общую стоимость
    else:
        order_item.quantity = quantity
        order_item.save()
