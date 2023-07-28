import asyncio
from django.contrib import admin

from .models import Profile, Category, Subcategory, Product, Order, OrderItem, TelegramMessage
from .bot.utils.send_message_all_users import send_message_to_all_users


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tg_user_id', 'name')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если редактируется существующий объект
            return self.readonly_fields + ('tg_user_id', 'name')
        return self.readonly_fields


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'total_cost', 'payment_status', 'payment_datetime')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_cost', 'quantity')


@admin.register(TelegramMessage)
class TelegramMessagesAdmin(admin.ModelAdmin):
    list_display = ('text', 'send_status', 'start_date_time', 'end_date_time')
    readonly_fields = ('send_status', 'start_date_time', 'end_date_time')
    list_filter = ('start_date_time',)
    search_fields = ('text',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если объект уже существует (редактирование)
            return self.readonly_fields + ('text', 'send_status', 'start_date_time', 'end_date_time')
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj:  # Если объект уже существует (редактирование)
            return False
        return super().has_change_permission(request, obj)

