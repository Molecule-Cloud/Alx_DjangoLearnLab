from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom User Registtration to access in Admin Panel

class CustomUserAdmin(UserAdmin):

    model  = CustomUser

    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_active', 'date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('bio', 'profile_picture', 'followers')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (('Profile Info', {'fields': ('bio', 'profile_picture')
        }),
    )
    readonly_fields = ['followers_count', 'created_at', 'updated_at']
    search_fields = ['username', 'email', 'bio']
    ordering = ['-date_joined']

admin.site.register(CustomUser, CustomUserAdmin)