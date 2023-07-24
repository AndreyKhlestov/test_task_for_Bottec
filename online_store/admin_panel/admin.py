from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tg_user_id', 'name')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если редактируется существующий объект
            return self.readonly_fields + ('tg_user_id', 'name')
        return self.readonly_fields
