from django.db import models
from colorfield.fields import ColorField

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Theme Name")
    primary_color = ColorField(default='#000000', help_text="Primary Color")
    secondary_color = ColorField(default='#FFFFFF', help_text="Secondary Color")
    background_color = ColorField(default='#F0F0F0', help_text="Background Color")
    text_color = ColorField(default='#000000', help_text="Text Color")
    button_color = ColorField(default='#007BFF', help_text="Button Background Color")
    button_text_color = ColorField(default='#FFFFFF', help_text="Button Text Color")
    font_family = models.CharField(max_length=100, default="Arial", help_text="Font Family")
    is_active = models.BooleanField(default=False, help_text="Set Active Theme")

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate all other themes
            Theme.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
