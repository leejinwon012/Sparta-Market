from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'market.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = product.liked_by.filter(id=request.user.id).exists()
    return render(request, 'product_detail.html', {'product': product, 'is_liked': is_liked})


@login_required
def product_like(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if request.user in product.liked_by.all():
            product.liked_by.remove(request.user)
        else:
            product.liked_by.add(request.user)
    # POST 요청이 아니면 그냥 제품 상세 페이지로 리디렉션합니다.
    return redirect('products:product_detail', pk=pk)


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # 현재 사용자가 작성자인 경우에만 수정 가능
    if request.user == product.author:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('products:product_list')
        else:
            form = ProductForm(instance=product)
        return render(request, 'product_update.html', {'form': form, 'product': product})
    else:
        # 작성자가 아닌 경우에는 수정 권한이 없으므로 상세 정보 페이지로 리디렉션
        return redirect('products:product_detail', pk=pk)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # 현재 사용자가 작성자인 경우에만 삭제 가능
    if request.user == product.author:
        if request.method == 'POST':
            product.delete()
            return redirect('products:product_list')
        return render(request, 'product_confirm_delete.html', {'product': product})
    else:
        # 작성자가 아닌 경우에는 삭제 권한이 없으므로 상세 정보 페이지로 리디렉션
        return redirect('products:product_detail', pk=pk)
