from django.urls import path
from .views import ThemeListCreateAPIView

urlpatterns = [
    path('theme/', ThemeListCreateAPIView.as_view(), name='theme'),
]
