from decimal import Decimal
from tg_bot.models import Profile, Product, OrderItem


def add_to_cart(tg_user_id: int, product_id: int, quantity: int):
    """Функция для добавления товара в корзину покупок"""
    order = Profile.objects.get(tg_user_id=tg_user_id).basket()  # данные о корзине
    product = Product.objects.get(id=product_id)  # данные о товаре

    # Проверьте, существует ли уже элемент OrderItem для этого продукта в текущем заказе
    order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

    # Если элемент уже существует, обновите его количество и общую стоимость
    if not created:
        order_item.quantity += quantity
        order_item.save()
        order.save()

    # Иначе, если элемент только что создан, установите количество и общую стоимость
    else:
        order_item.quantity = quantity
        order_item.save()
        order.save()


def del_product(tg_user_id: int, product_name: str):
    """Функция для удаления товара из корзины покупок"""
    order = Profile.objects.get(tg_user_id=tg_user_id).basket()  # данные о корзине
    product = Product.objects.get(name=product_name)  # данные о товаре, который хотим удалить

    order_item = OrderItem.objects.get(product=product, order=order)
    order_item.delete()
    order.save()
    return order
