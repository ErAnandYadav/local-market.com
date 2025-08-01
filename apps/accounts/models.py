from django.db import models
from colorfield.fields import ColorField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='media/profile_images/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Address(models.Model):
    ADDRESS_TYPES = [
        ('home', 'Home'),
        ('work', 'Work'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)  # Full name
    phone = models.CharField(max_length=15)  # 10-digit mobile number
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)  # Optional
    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    address_line = models.TextField(help_text="Address (Area and Street)")
    city = models.CharField(max_length=50, verbose_name="City/District/Town")
    state = models.CharField(max_length=50, verbose_name="State")
    landmark = models.CharField(max_length=100, blank=True, null=True)  # Optional
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"


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


