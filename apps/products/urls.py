from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, SubCategoryListAPIView, BrandListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('sub-categories/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('brands/', BrandListAPIView.as_view(), name='brand-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products-details/', ProductDetailAPIView.as_view(), name='product-detail'),
]
