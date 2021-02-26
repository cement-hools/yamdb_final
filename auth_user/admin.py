from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username',
        'role',
        'description',
        'first_name',
        'last_name',
        'email',
        'password',
        'confirmation_code')
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
