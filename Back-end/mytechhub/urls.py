from django.urls import path
from . import views

urlpatterns = [
    path('techhub/', views.techhub, name='techhub'),
]
