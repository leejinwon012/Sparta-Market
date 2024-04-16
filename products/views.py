from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_detail.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail')  # 등록 후 목록 페이지로 이동
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


def product_delete(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        product.delete()
    return redirect('product_detail')


def product_update(request, pk):
    # 데이터베이스에서 해당 제품을 가져옴
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail')
    else:
        # GET 요청에서는 제품 객체를 사용하여 폼을 초기화
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'form': form, 'product': product})
