from rest_framework import serializers
from apps.accounts.serializers import ThemeSerializer
from .models import *

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'theme']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'image']

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['user_id', 'rating', 'review', 'created_at']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    ratings = ProductRatingSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'availability_type',
            'retail_price',
            'wholesale_price',
            'minimum_wholesale_quantity',
            'feature_image',
            'discount',
            'city',
            'category',
            'sizes',
            'colors',
            'variants',
            'delivery_time',
            'images',
            'ratings'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True)
    ratings = ProductRatingSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum([r.rating for r in ratings]) / ratings.count(), 2)
        return None


