from django.contrib import admin

from .models import Profile, Category, Subcategory, Product


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
    list_display = ('name', 'subcategory', 'description', 'image')
