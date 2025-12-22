from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from shop.models import Product
from .serializers import ProductSerializer

# 1. Отримання списку (GET) та Додавання (POST)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] 

# 2. Отримання одного (GET), Оновлення (PUT/PATCH), Видалення (DELETE)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug' 
    permission_classes = [IsAuthenticated]