from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.techhub, name='techhub'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('order-history/', views.order_history, name='order_history'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('create-order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.view_order, name='view_order'),
    path('simulate-payment/<int:order_id>/', views.simulate_payment, name='simulate_payment'),

    # Gerenciamento de Produtos para Fornecedores
    path('product-list/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]
