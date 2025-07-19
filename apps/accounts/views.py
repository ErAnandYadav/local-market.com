from django.shortcuts import render
from rest_framework import status
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Theme
from .serializers import ThemeSerializer

class ThemeListCreateAPIView(APIView):
    def get(self, request):
        themes = Theme.objects.filter(is_active=True)
        serializer = ThemeSerializer(themes, many=True)
        return Response({"themes": serializer.data, "message": "Product details", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)