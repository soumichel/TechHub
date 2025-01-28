from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Página principal
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Rota para login e autenticação
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Outras páginas
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register-supplier/', TemplateView.as_view(template_name='register-supplier.html'), name='register_supplier'),
    path('create-product/', TemplateView.as_view(template_name='create-product.html'), name='create_product'),
    path('create-order/', TemplateView.as_view(template_name='create-order.html'), name='create_order'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

