from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


@login_required
def techhub(request):
    """Página principal para usuários logados."""
    user = request.user
    template = 'techhub.html'
    context = {
        "nome_empresa": "TechHub",
        "slogan": "O lugar perfeito para encontrar seus periféricos!",
        "usuarioativo": user.is_active,
        "perfil": "Fornecedor" if user.is_supplier else "Usuário Comum",
        "mensagem": (
            "Bem-vindo à área do fornecedor! Aqui você pode gerenciar seus produtos."
            if user.is_supplier
            else "Bem-vindo à TechHub! Aqui você pode explorar produtos e gerenciar seus pedidos."
        ),
    }

    if user.is_supplier:
        # Listar produtos do fornecedor.
        context["produtos"] = Product.objects.filter(supplier=user.supplier)
    else:
        # Listar pedidos do usuário comum.
        context["pedidos"] = Order.objects.filter(user=user)

    return HttpResponse(render(request, template, context))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_product(request):
    """Registro de novos produtos para fornecedores via API."""
    if not request.user.is_supplier:
        return Response({"detail": "Apenas fornecedores podem registrar produtos."}, status=403)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(supplier=request.user.supplier)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_orders(request):
    """Listagem de pedidos do usuário logado."""
    user = request.user
    if user.is_supplier:
        return Response({"detail": "Fornecedores não têm acesso a pedidos pessoais."}, status=403)

    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Criação de um novo pedido pelo usuário logado."""

    user = request.user
    if user.is_supplier:
        return Response({"detail": "Fornecedores não podem criar pedidos."}, status=403)

    # Criação do pedido
    order = Order.objects.create(user=user, status="Pending")

    # Adicionar itens ao pedido
    for item_data in request.data.get('items', []):
        product = Product.objects.get(id=item_data['product_id'])
        quantity = item_data['quantity']
        price = product.price

        # Criar o item de pedido
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price,
            subtotal=price * quantity
        )

    # Serializar o pedido
    order_serializer = OrderSerializer(order)

    return Response(order_serializer.data, status=201)
