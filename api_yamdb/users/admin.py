from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'date_joined', 'is_active', 'is_staff'
    )
    search_fields = ('username',)
    list_filter = ('role', 'is_active')
    empty_value_display = '-пусто-'
    fields = [
        ('username', 'role'),
        ('first_name', 'last_name'),
        'bio',
        ('is_staff', 'is_active'),
    ]


admin.site.register(User, UserAdmin)
