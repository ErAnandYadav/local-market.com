from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404


# Create your views here.

class CategoryListAPIView(APIView):
    def get(self, request):
        products = Category.objects.all()
        serializer = CategorySerializer(products, many=True)
        return Response({"products": serializer.data, "message": "Categories", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({"products": serializer.data, "message": "Products", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

class ProductDetailAPIView(APIView):
    def get(self, request):
        try:
            product_id = request.query_params.get("product_id")
            product = Product.objects.get(product_id=product_id)
        except Exception as e:
            return Response({"product":[], "message": "Product not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response({"product": serializer.data, "message": "Product details", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        