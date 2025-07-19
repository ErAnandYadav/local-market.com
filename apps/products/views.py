from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from utils.utils import haversine

class CategoryListAPIView(APIView):
    def get(self, request):
        products = Category.objects.all()
        serializer = CategorySerializer(products, many=True)
        return Response({"categories": serializer.data, "message": "Categories", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
class ProductListAPIView(APIView):
    def get(self, request):
        category_id = request.query_params.get("category_id")
        user_lat = request.query_params.get("user_lat")
        user_long = request.query_params.get("user_long")

        if not user_lat or not user_long:
            return Response({"message": "Latitude and longitude are required", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        user_lat = float(user_lat)
        user_long = float(user_long)

        # Step 1: Filter warehouses within 10km
        nearby_warehouses = []
        for warehouse in Warehouse.objects.all():
            if warehouse.latitude and warehouse.longitude:
                distance = haversine(user_lat, user_long, warehouse.latitude, warehouse.longitude)
                print("Distance:", distance)
                if distance <= 10:
                    nearby_warehouses.append(warehouse.warehouse_id)

        # Step 2: Filter products via M2M through Inventory
        if category_id:
            products = Product.objects.filter(category__category_id=category_id, warehouses__warehouse_id__in=nearby_warehouses).distinct()
        else:
            products = Product.objects.filter(warehouses__warehouse_id__in=nearby_warehouses).distinct()

        serializer = ProductSerializer(products, many=True)
        return Response({
            "product": serializer.data,
            "message": "Products within 10km",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class ProductDetailAPIView(APIView):
    def get(self, request):
        try:
            product_id = request.query_params.get("product_id")
            product = Product.objects.get(product_id=product_id)
        except Exception as e:
            return Response({"product":[], "message": "Product not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response({"product-details": serializer.data, "message": "Product details", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        