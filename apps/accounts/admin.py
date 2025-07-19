from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import *
# Register your models here.

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'secondary_color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'profile_image_tag')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.profile_image.url)
        return "-"
    profile_image_tag.short_description = 'Profile Image'

admin.site.register(User, UserAdmin)
admin.site.register(Address)