from django.urls import path
from . import views

app_name = 'products'  # 네임스페이스 설정

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/like/', views.product_like, name='product_like'),
]
