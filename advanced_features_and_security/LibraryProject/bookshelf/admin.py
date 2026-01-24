from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'publication_year')
#     search_fields = ('title', 'author')
#     list_filter = ('publication_year',)

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_super_user', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CustomUser, CustomUserAdmin)