from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_supplier = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",  # Evita conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",  # Evita conflito
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({'Fornecedor' if self.is_supplier else 'Comprador'})"


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier")
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name  # Exibe o nome do fornecedor


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  # Exibe o nome da categoria


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Fornecedor: {self.supplier.name}, Categoria: {self.category.name})"


# Carrinho de Compras (Cart)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("Pending", "Pendente"), ("Completed", "Finalizado")], default="Pending")

    def __str__(self):
        return f"Carrinho de {self.user.username}"

# Item do Carrinho (CartItem)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Carrinho de {self.cart.user.username})"


# Pedido (Order)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=50, choices=[
        ("Pending", "Pendente"),
        ("Processing", "Em Processamento"),
        ("Completed", "Concluído"),
        ("Cancelled", "Cancelado"),
    ], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - Status: {self.get_status_display()}"

    def total(self):
        return sum(item.subtotal for item in self.items.all())


# Item de Pedido (OrderItem)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Pedido {self.order.id})"
