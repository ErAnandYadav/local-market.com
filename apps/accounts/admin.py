from django.contrib import admin
from .models import Theme
# Register your models here.

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_color', 'secondary_color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)