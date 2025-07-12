from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import Theme
import uuid

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    warehouse_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)  # e.g., "S", "M", "L", "XL", "XXL"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)  # e.g., "Red", "Blue", "Black"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    AVAILABILITY_CHOICES = (
        ('retail', 'Retail Only'),
        ('wholesale', 'Wholesale Only'),
        ('both', 'Both Retail and Wholesale'),
    )

    name = models.CharField(max_length=200, null=True)
    availability_type = models.CharField(
        max_length=10,
        choices=AVAILABILITY_CHOICES,
        default='both',
        help_text="Select if the product is available for retail, wholesale, or both."
    )

    # Retail fields
    retail_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )

    # Wholesale fields
    wholesale_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    minimum_wholesale_quantity = models.PositiveIntegerField(null=True, blank=True)

    feature_image = models.ImageField(upload_to='product_images/')
    discount = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Discount percentage",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    city = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", null=True)

    variants = models.JSONField(null=True, blank=True, help_text="Optional variants for the product")
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in minutes", null=True)

    # Link products to warehouses using a Many-to-Many field through the Inventory model
    warehouses = models.ManyToManyField(Warehouse, through='Inventory', related_name="products")
    sizes = models.ManyToManyField(Size, related_name="products", null=True, blank=True)
    colors = models.ManyToManyField(Color, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        """
        Ensure retail price and wholesale price are set correctly based on availability type.
        """
        from django.core.exceptions import ValidationError

        if self.availability_type in ['retail', 'both'] and not self.retail_price:
            raise ValidationError("Retail price is required for retail products.")

        if self.availability_type in ['wholesale', 'both'] and not self.wholesale_price:
            raise ValidationError("Wholesale price is required for wholesale products.")


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True)
    image = models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class Inventory(models.Model):
    inventory_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], null=True)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f"{self.product.name} at {self.warehouse.name} - {self.stock} units"

class ProductRating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE, null=True)
    user_id = models.UUIDField(null=True) 
    rating = models.PositiveSmallIntegerField(null=True)  # e.g. 1 to 5
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('product', 'user_id') 

    def __str__(self):
        return f"{self.product.name} - {self.rating}★"