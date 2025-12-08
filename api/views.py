from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from shop.models import Product
from .serializers import ProductSerializer

# 1. Отримання списку (GET) та Додавання (POST)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Дозволяємо читати всім, а додавати тільки авторизованим (Крок 16)
    permission_classes = [IsAuthenticated] 

# 2. Отримання одного (GET), Оновлення (PUT/PATCH), Видалення (DELETE)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug' # Ми використовуємо slug в URL
    permission_classes = [IsAuthenticated]