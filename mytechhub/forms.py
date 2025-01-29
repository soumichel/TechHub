from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    is_supplier = forms.BooleanField(required=False, label="Fornecedor")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_supplier")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']  # Definindo quais campos o fornecedor pode preencher