from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at', 'slug')
    list_filter = ('category', 'created_at')
    search_fields = ('name',)
    list_editable = ('price',)  # редагування price прямо в списку
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    list_editable = ()
    prepopulated_fields = {"slug": ("name",)}
