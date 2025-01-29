from django.contrib import admin
from .models import User, SupplierProfile, Category, Product, Order, OrderItem

# Registro do modelo User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_supplier', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Registro do modelo SupplierProfile (perfil de fornecedor)
@admin.register(SupplierProfile)
class SupplierProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'address', 'user')
    search_fields = ('company_name', 'phone')

# Registro do modelo Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Registro do modelo Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'supplier', 'created_at')
    search_fields = ('name',)
    list_filter = ('category', 'supplier')

# Registro do modelo Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    search_fields = ('user__username', 'status')

# Registro do modelo OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__created_at',)
    