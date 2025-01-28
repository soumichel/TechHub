from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import techhub, register_product, user_orders, ProtectedView

urlpatterns = [
    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # View protegida para testes
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    
    # Página principal
    path('techhub/', techhub, name='techhub'),

    # API de gerenciamento
    path('api/register-product/', register_product, name='register_product'),
    path('api/user-orders/', user_orders, name='user_orders'),
]
