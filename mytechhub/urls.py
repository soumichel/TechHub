from django.urls import path
from . import views

urlpatterns = [
    path('', views.teste, name='home'),
    path('testeparametros/', views.testeparametros, name='testeparametros')
]
