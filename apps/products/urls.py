from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products-details/', ProductDetailAPIView.as_view(), name='product-detail'),
]
