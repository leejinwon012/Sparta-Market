from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
]