from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Category
from .forms import ProductForm, CategoryForm

# PRODUCTS
# shop/views.py

class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Отримуємо базовий набір об'єктів
        queryset = super().get_queryset()
        # Отримуємо параметр сортування з URL-адреси
        sort_by = self.request.GET.get('sort')

        if sort_by == 'price_asc':
            # Сортуємо за ціною: від дешевших до дорожчих
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            # Сортуємо за ціною: від дорожчих до дешевших
            queryset = queryset.order_by('-price')
        elif sort_by == 'category':
            # Сортуємо за назвою категорії
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

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('products')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# CATEGORIES
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

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_form.html'

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/category_confirm_delete.html'
    success_url = reverse_lazy('categories')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
