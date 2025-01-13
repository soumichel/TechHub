from django.contrib import admin
from .models import User, Supplier, Category, Product, Order, OrderItem

# Registrar os modelos no admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_supplier', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_supplier', 'is_staff', 'is_active')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'user')
    search_fields = ('name', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'supplier', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('supplier', 'category')
    ordering = ('-created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__created_at',)
    
