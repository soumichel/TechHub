from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import User, Order, Cart, CartItem, Product
from .forms import CustomUserCreationForm, ProductForm

# Registro de usuário
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_supplier = form.cleaned_data["is_supplier"]  # Define se é fornecedor
            user.save()
            login(request, user)  # Loga automaticamente após o cadastro
            return redirect("techhub")  # Redireciona para a página principal
    else:
        form = CustomUserCreationForm()

    return render(request, "auth/register.html", {"form": form})

# Página inicial protegida
@login_required
def techhub(request):
    return HttpResponse("Bem-vindo ao TechHub!")

# Atualização de perfil
@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        # Atualizando informações do fornecedor, se aplicável
        if user.is_supplier:
            user.supplier.phone = request.POST.get('phone', user.supplier.phone)
            user.supplier.address = request.POST.get('address', user.supplier.address)
            user.supplier.save()

        return redirect('profile')

    return render(request, 'auth/update_profile.html', {'user': user})

# Histórico de Pedidos
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Buscar pedidos do usuário logado
    return render(request, 'auth/order_history.html', {'orders': orders})

# Adicionar produto ao carrinho
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, status='Pending')

    # Verificar se o item já existe no carrinho
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # Se já existir, aumente a quantidade
    cart_item.price = product.price
    cart_item.save()

    return redirect('view_cart')

# Visualizar o carrinho de compras
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, status='Pending').first()
    if cart:
        cart_items = cart.items.all()
    else:
        cart_items = []
    return render(request, 'auth/view_cart.html', {'cart_items': cart_items})

# Criar pedido a partir do carrinho
@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user, status='Pending').first()
    if not cart:
        return redirect('view_cart')

    # Criar um novo pedido
    order = Order.objects.create(user=request.user, status='Pending')

    # Adicionar itens do carrinho para o pedido
    for cart_item in cart.items.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity,
                                 price=cart_item.price)

    # Atualizar o status do carrinho
    cart.status = 'Completed'
    cart.save()

    return redirect('view_order', order_id=order.id)

# Visualizar pedido
@login_required
def view_order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'auth/view_order.html', {'order': order})

# Simular pagamento
@login_required
def simulate_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.user == request.user and order.status != 'Completed':
        order.status = 'Completed'  # Simulando o pagamento
        order.save()

    return redirect('view_order', order_id=order.id)

# Adicionar produto (para fornecedores)
@login_required
def add_product(request):
    if not request.user.is_supplier:
        return HttpResponse("Acesso negado", status=403)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = request.user  # Associar o produto ao fornecedor logado
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'auth/add_product.html', {'form': form})

# Editar produto (para fornecedores)
@login_required
def edit_product(request, product_id):
    if not request.user.is_supplier:
        return HttpResponse("Acesso negado", status=403)

    product = get_object_or_404(Product, id=product_id)

    if product.supplier != request.user:
        return HttpResponse("Acesso negado", status=403)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'auth/edit_product.html', {'form': form, 'product': product})

# Excluir produto (para fornecedores)
@login_required
def delete_product(request, product_id):
    if not request.user.is_supplier:
        return HttpResponse("Acesso negado", status=403)

    product = get_object_or_404(Product, id=product_id)

    if product.supplier != request.user:
        return HttpResponse("Acesso negado", status=403)

    product.delete()
    return redirect('product_list')

# Listar produtos (para fornecedores)
@login_required
def product_list(request):
    if not request.user.is_supplier:
        return HttpResponse("Acesso negado", status=403)

    products = Product.objects.filter(supplier=request.user)
    return render(request, 'auth/product_list.html', {'products': products})
