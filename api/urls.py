from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]