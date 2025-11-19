from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib.auth.mixins import UserPassesTestMixin
# 2.  загальний клас для перевірки прав суперкористувача ↓↓↓
class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Цей міксин перевіряє, чи є поточний користувач суперкористувачем.
    Якщо ні - повертає помилку 403 (Forbidden).
    """
    def test_func(self):
        return self.request.user.is_superuser

# === PRODUCTS ===

class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort')

        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'category':
            queryset = queryset.order_by('category__name', 'name')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

# ↓↓↓ 3. Додайте 'SuperuserRequiredMixin' до класів нижче ↓↓↓

class ProductCreateView(SuperuserRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

class ProductUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class ProductDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('products')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# === CATEGORIES ===

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/categories.html'
    context_object_name = 'categories'
    paginate_by = 10

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

# ↓↓↓ 4. Також захищаємо керування категоріями ↓↓↓

class CategoryCreateView(SuperuserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_form.html'

class CategoryUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class CategoryDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Category
    template_name = 'shop/category_confirm_delete.html'
    success_url = reverse_lazy('categories')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'