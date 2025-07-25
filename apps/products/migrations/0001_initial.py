# Generated by Django 5.2.4 on 2025-07-20 17:05

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_alter_user_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brand_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='media/brand_icons/')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('warehouse_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('address', models.TextField(null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='media/category_icons/')),
                ('theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.theme')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('availability_type', models.CharField(choices=[('retail', 'Retail Only'), ('wholesale', 'Wholesale Only'), ('both', 'Both Retail and Wholesale')], default='both', help_text='Select if the product is available for retail, wholesale, or both.', max_length=10)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_wholesale_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('feature_image', models.ImageField(upload_to='media/product_images/')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, help_text='Discount percentage', max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('city', models.CharField(max_length=100, null=True)),
                ('variants', models.JSONField(blank=True, help_text='Optional variants for the product', null=True)),
                ('delivery_time', models.PositiveIntegerField(help_text='Delivery time in minutes', null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.brand')),
                ('colors', models.ManyToManyField(blank=True, null=True, related_name='products', to='products.color')),
                ('sizes', models.ManyToManyField(blank=True, null=True, related_name='products', to='products.size')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('stock', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.warehouse')),
            ],
            options={
                'unique_together': {('product', 'warehouse')},
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='media/product_images/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('subcategory_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='media/sub_category_icons/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='warehouses',
            field=models.ManyToManyField(related_name='products', through='products.Inventory', to='products.warehouse'),
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.UUIDField(null=True)),
                ('rating', models.PositiveSmallIntegerField(null=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='products.product')),
            ],
            options={
                'unique_together': {('product', 'user_id')},
            },
        ),
    ]
