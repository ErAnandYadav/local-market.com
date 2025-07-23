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

class SubCategoryListAPIView(APIView):
    def get(self, request):
        category_id = request.query_params.get("category_id")
        products = SubCategory.objects.filter(category__category_id=category_id)
        serializer = SubCategorySerializer(products, many=True)
        return Response({"subcategories": serializer.data, "message": "Subcategories", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

class BrandListAPIView(APIView):
    def get(self, request):
        products = Brand.objects.all()
        serializer = BrandSerializer(products, many=True)
        return Response({"brands": serializer.data, "message": "Brands", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

class ProductListAPIView(APIView):
    def get(self, request):
        sub_category_id = request.query_params.get("sub_category_id")
        user_lat = request.query_params.get("user_lat")
        user_long = request.query_params.get("user_long")

        # Step 1: Validate required parameters
        if not user_lat or not user_long:
            return Response(
                {"message": "Latitude and longitude are required", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_lat = float(user_lat)
            user_long = float(user_long)
        except ValueError:
            return Response(
                {"message": "Latitude and longitude must be valid float values", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Step 2: Filter warehouses within 10km
            nearby_warehouses = []
            all_warehouses = Warehouse.objects.all()
            for warehouse in all_warehouses:
                if warehouse.latitude and warehouse.longitude:
                    distance = haversine(user_lat, user_long, warehouse.latitude, warehouse.longitude)
                    if distance <= 10:
                        nearby_warehouses.append(warehouse.warehouse_id)

            if not nearby_warehouses:
                return Response(
                    {"message": "No nearby warehouses found within 10 km", "product": [], "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK
                )

            # Step 3: Filter products available in those warehouses
            products_query = Product.objects.filter(
                warehouses__warehouse_id__in=nearby_warehouses
            )
            if sub_category_id:
                products_query = products_query.filter(sub_category_id=sub_category_id)

            products = products_query.distinct()

            serializer = ProductSerializer(products, many=True)
            return Response(
                {
                    "product": serializer.data,
                    "message": "Products within 10km",
                    "status": status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": f"Something went wrong: {str(e)}", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductDetailAPIView(APIView):
    def get(self, request):
        try:
            product_id = request.query_params.get("product_id")
            product = Product.objects.get(product_id=product_id)
        except Exception as e:
            return Response({"product":[], "message": "Product not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        return Response({"product-details": serializer.data, "message": "Product details", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        