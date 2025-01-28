from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem, SupplierProfile, User
from .serializers import ProductSerializer, OrderSerializer, SupplierProfileSerializer, UserCreateSerializer


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
        context["produtos"] = Product.objects.filter(supplier=user.supplier)
    else:
        context["pedidos"] = Order.objects.filter(user=user)

    return HttpResponse(render(request, template, context))

@api_view(['POST'])
def register_supplier(request):
    """Registro de novos fornecedores"""
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Salva o usuário
        user = serializer.save()

        # Definir o usuário como fornecedor
        user.is_supplier = True
        user.save()

        # Criar o perfil de fornecedor
        SupplierProfile.objects.create(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def create_or_update_supplier_profile(request):
    """Criação ou atualização do perfil de fornecedor"""
    
    if not request.user.is_supplier:
        return Response({"detail": "Apenas fornecedores podem criar ou atualizar seu perfil."}, status=403)

    try:
        profile = SupplierProfile.objects.get(user=request.user)
    except SupplierProfile.DoesNotExist:
        profile = None

    if profile:
        serializer = SupplierProfileSerializer(profile, data=request.data, partial=True)
    else:
        serializer = SupplierProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED if not profile else status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    order_data = {'user': user, 'status': 'Pending'}
    order_serializer = OrderSerializer(data=order_data)

    if order_serializer.is_valid():
        order = order_serializer.save()
        for item_data in request.data.get('items', []):
            try:
                product = Product.objects.get(id=item_data['product_id'])
                OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price=product.price, subtotal=product.price * item_data['quantity'])
            except Product.DoesNotExist:
                return Response({"detail": f"Produto com ID {item_data['product_id']} não encontrado."}, status=404)

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """Atualização do status de um pedido existente."""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"detail": "Pedido não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if order.user != request.user and not request.user.is_staff:
        return Response({"detail": "Você não tem permissão para alterar o status deste pedido."}, status=status.HTTP_403_FORBIDDEN)

    valid_statuses = ["Pending", "Completed", "Cancelled"]
    new_status = request.data.get('status')

    if new_status not in valid_statuses:
        return Response({"detail": "Status inválido. Use 'Pending', 'Completed' ou 'Cancelled'."}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()

    return Response({"detail": f"Status do pedido atualizado para '{new_status}'."}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    """Atualiza os detalhes de um produto do fornecedor"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Produto não encontrado."}, status=404)

    if product.supplier.user != request.user:
        return Response({"detail": "Você não tem permissão para editar este produto."}, status=403)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    """Deleta um produto do fornecedor"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Produto não encontrado."}, status=404)

    if product.supplier.user != request.user:
        return Response({"detail": "Você não tem permissão para excluir este produto."}, status=403)

    product.delete()
    return Response({"detail": "Produto deletado com sucesso."}, status=204)
