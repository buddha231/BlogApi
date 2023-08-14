from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active', 'date_joined')
    readonly_fields = ('id',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
